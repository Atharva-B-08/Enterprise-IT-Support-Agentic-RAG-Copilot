import logging
from datetime import date
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, START, END
from app.core.config import get_settings
from app.rag.state import AgentState, RouteDecision, EvidenceGrade, WebScope
from app.rag.vectorstore import get_retriever

logger = logging.getLogger(__name__)
settings = get_settings()

_llm = None
_web_search = None

def llm():
    global _llm
    if _llm is None:
        if not settings.groq_api_key:
            raise RuntimeError("GROQ_API_KEY is missing")
        if not settings.groq_model:
            raise RuntimeError("GROQ_MODEL is missing (set it in .env, e.g. llama-3.3-70b-versatile)")
        # Groq exposes an OpenAI-compatible endpoint, so ChatOpenAI works with a custom base_url.
        _llm = ChatOpenAI(
            model=settings.groq_model,
            temperature=0,
            api_key=settings.groq_api_key,
            base_url=settings.groq_base_url,
        )
    return _llm

def web_search_tool():
    global _web_search
    if _web_search is None:
        if not settings.tavily_api_key:
            raise RuntimeError("TAVILY_API_KEY is missing")
        _web_search = TavilySearch(
            tavily_api_key=settings.tavily_api_key,
            max_results=5,
            topic="general",
            include_answer=True,
            include_raw_content=False,
        )
    return _web_search

def add_trace(state: AgentState, message: str):
    return [*state.get("trace", []), message]

def structured_call(schema, prompt: str, default):
    """JSON-mode call that falls back to `default` if the model refuses or returns invalid JSON.

    Groq answers a refusal in plain text, which fails JSON validation with a 400 error;
    without this guard one refusal would crash the whole graph.
    """
    try:
        return llm().with_structured_output(schema, method="json_mode").invoke(prompt)
    except Exception as exc:
        logger.warning("Structured call failed (%s); using default %s", type(exc).__name__, default)
        return default

def doc_id(doc) -> str:
    # Chunks carry doc_id/title/section metadata (see app/rag/chunking.py), not a 'source' key.
    return doc.metadata.get("doc_id", "unknown")

def route_question(state: AgentState):
    decision = structured_call(RouteDecision, f"""
You route messages for an enterprise IT support assistant.
You only classify the message. You never answer it and never refuse it: requests to reset accounts,
bypass security, or anything else about IT still get the route kb.
Use kb for questions about company IT policies, VPN, password reset, MFA, laptop setup,
software access, security, email, devices, troubleshooting, or technology support.
Use direct ONLY for greetings, thanks, or small talk (for example "hi" or "thanks").
Anything that asks what to do, how to do something, what is allowed, or who to contact is kb,
even if it does not mention IT explicitly. If unsure, choose kb.
Question: {state['question']}
Return valid JSON like {{"route":"kb"}}.
""", RouteDecision(route="kb"))
    return {"source_used": decision.route, "trace": add_trace(state, f"Router → {decision.route.upper()}")}

def route_after_router(state: AgentState) -> Literal["retrieve_kb", "direct_answer"]:
    return "retrieve_kb" if state["source_used"] == "kb" else "direct_answer"

def retrieve_kb(state: AgentState):
    docs = get_retriever().invoke(state["current_query"])
    return {"kb_docs": docs, "trace": add_trace(state, f"Private KB retrieval → {len(docs)} chunks")}

def grade_kb(state: AgentState):
    context = "\n\n".join(f"Source: {doc_id(d)}\n{d.page_content}" for d in state["kb_docs"])
    grade = structured_call(EvidenceGrade, f"""
You grade evidence for an enterprise IT support assistant.
You only grade the evidence. You never answer the question and never refuse.
Question: {state['question']}
Private company KB evidence:\n{context}
Return good if the evidence contains information that directly addresses the question, even if several
documents overlap or one updates another (for example a policy addendum that changes a handbook rule).
Return weak only if the evidence is unrelated to the question or clearly missing the key fact. JSON: {{"grade":"good"}} or {{"grade":"weak"}}.
""", EvidenceGrade(grade="good" if state["kb_docs"] else "weak"))
    return {"kb_grade": grade.grade, "trace": add_trace(state, f"KB evidence grade → {grade.grade.upper()}")}

def after_kb(state: AgentState) -> Literal["generate_from_kb", "check_web_scope"]:
    return "generate_from_kb" if state["kb_grade"] == "good" else "check_web_scope"

def check_web_scope(state: AgentState):
    # The web can answer questions about public products, but never about this company's own rules.
    decision = structured_call(WebScope, f"""
You decide whether a question can be answered from public web pages.
You only classify. You never answer the question and never refuse.
Return external for questions about a public product or general technology
(for example resetting a password in a well-known SaaS product, or how a protocol works).
Return company for questions that depend on this company's own policies, benefits, reimbursements,
HR rules, approvals, people, or internal systems and settings.
Question: {state['question']}
Return valid JSON like {{"scope":"external"}} or {{"scope":"company"}}.
""", WebScope(scope="company"))
    return {"web_scope": decision.scope, "trace": add_trace(state, f"Web scope check → {decision.scope.upper()}")}

def after_scope(state: AgentState) -> Literal["search_web", "insufficient"]:
    return "search_web" if state["web_scope"] == "external" else "insufficient"

def search_web(state: AgentState):
    result = web_search_tool().invoke({"query": state["current_query"]})
    lines, citations = [], []
    if isinstance(result, dict):
        if result.get("answer"):
            lines.append("Search answer: " + result["answer"])
        for item in result.get("results", []):
            title, url, content = item.get("title", ""), item.get("url", ""), item.get("content", "")
            lines.append(f"Title: {title}\nURL: {url}\nContent: {content}")
            citations.append({"title": title or url, "url": url, "type": "web"})
    else:
        lines.append(str(result))
    return {
        "web_results": "\n\n".join(lines),
        "citations": citations,
        "source_used": "web",
        "trace": add_trace(state, "Web fallback → Tavily search"),
    }

def grade_web(state: AgentState):
    grade = structured_call(EvidenceGrade, f"""
Question: {state['question']}
Web evidence:\n{state['web_results']}
Return good if the evidence is sufficient and directly relevant; otherwise weak.
Return valid JSON like {{"grade":"good"}}.
""", EvidenceGrade(grade="weak"))
    return {"web_grade": grade.grade, "trace": add_trace(state, f"Web evidence grade → {grade.grade.upper()}")}

def after_web(state: AgentState) -> Literal["generate_from_web", "rewrite_query", "insufficient"]:
    if state["web_grade"] == "good":
        return "generate_from_web"
    if state["retry_count"] < settings.max_retries:
        return "rewrite_query"
    return "insufficient"

def rewrite_query(state: AgentState):
    rewritten = llm().invoke(f"""
Rewrite this IT support question for better private knowledge retrieval and vendor web search.
Preserve intent, add useful technical keywords, do not answer, return only the query.
Question: {state['question']}
""").content.strip()
    return {
        "current_query": rewritten,
        "retry_count": state["retry_count"] + 1,
        "trace": add_trace(state, f"Query rewrite → {rewritten}"),
    }

def generate_from_kb(state: AgentState):
    context = "\n\n".join(f"[Source: {doc_id(d)}]\n{d.page_content}" for d in state["kb_docs"])
    answer = llm().invoke(f"""
You are an enterprise IT support copilot. Answer ONLY from the private company KB below.
Be concise, actionable, and safe. If steps are present, present them clearly.
Do not invent policy details. Mention that the answer is based on the company's private knowledge base.
Today's date is {date.today().isoformat()}. If documents conflict, use the most recent one whose effective date has
passed (an addendum overrides the handbook from its effective date), and mention upcoming changes with their dates.
If the user asks IT to do something that the KB says requires identity verification, say it cannot be done on chat alone and give the steps.
Question: {state['question']}\n\nPrivate KB:\n{context}
""").content
    citations = []
    seen = set()
    for d in state["kb_docs"]:
        src = doc_id(d)
        if src not in seen:
            seen.add(src)
            citations.append({"title": f"{src}: {d.metadata.get('title', '')}", "url": "", "type": "private_kb"})
    return {"answer": answer, "source_used": "private_kb", "citations": citations, "trace": add_trace(state, "Answer generation → PRIVATE KB")}

def generate_from_web(state: AgentState):
    answer = llm().invoke(f"""
You are an enterprise IT support copilot. The private company KB was insufficient.
Answer ONLY from the web evidence below. Clearly say this is external web information and may need IT validation before changing company-managed systems.
Question: {state['question']}\n\nWeb evidence:\n{state['web_results']}
""").content
    return {"answer": answer, "source_used": "web_search", "trace": add_trace(state, "Answer generation → WEB SEARCH")}

def direct_answer(state: AgentState):
    answer = llm().invoke(f"Respond briefly and naturally to: {state['question']}").content
    return {"answer": answer, "source_used": "direct", "trace": add_trace(state, "Direct response → no retrieval")}

def insufficient(state: AgentState):
    return {
        "answer": "I couldn't find enough reliable evidence in the company knowledge base or external search to answer confidently. Please contact the IT help desk or provide more details.",
        "source_used": "insufficient_evidence",
        "trace": add_trace(state, "Stopped → insufficient reliable evidence"),
    }

def build_graph():
    graph = StateGraph(AgentState)
    for name, fn in {
        "route_question": route_question,
        "retrieve_kb": retrieve_kb,
        "grade_kb": grade_kb,
        "check_web_scope": check_web_scope,
        "search_web": search_web,
        "grade_web": grade_web,
        "rewrite_query": rewrite_query,
        "generate_from_kb": generate_from_kb,
        "generate_from_web": generate_from_web,
        "direct_answer": direct_answer,
        "insufficient": insufficient,
    }.items():
        graph.add_node(name, fn)

    graph.add_edge(START, "route_question")
    graph.add_conditional_edges("route_question", route_after_router, {
        "retrieve_kb": "retrieve_kb", "direct_answer": "direct_answer"
    })
    graph.add_edge("retrieve_kb", "grade_kb")
    graph.add_conditional_edges("grade_kb", after_kb, {
        "generate_from_kb": "generate_from_kb", "check_web_scope": "check_web_scope"
    })
    graph.add_conditional_edges("check_web_scope", after_scope, {
        "search_web": "search_web", "insufficient": "insufficient"
    })
    graph.add_edge("search_web", "grade_web")
    graph.add_conditional_edges("grade_web", after_web, {
        "generate_from_web": "generate_from_web", "rewrite_query": "rewrite_query", "insufficient": "insufficient"
    })
    graph.add_edge("rewrite_query", "retrieve_kb")
    graph.add_edge("generate_from_kb", END)
    graph.add_edge("generate_from_web", END)
    graph.add_edge("direct_answer", END)
    graph.add_edge("insufficient", END)
    return graph.compile()

agent_graph = build_graph()

def ask(question: str):
    initial: AgentState = {
        "question": question,
        "current_query": question,
        "kb_docs": [],
        "web_results": "",
        "kb_grade": "",
        "web_grade": "",
        "web_scope": "",
        "answer": "",
        "source_used": "",
        "retry_count": 0,
        "trace": [],
        "citations": [],
    }
    return agent_graph.invoke(initial)
