from typing import List, Literal
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langchain_core.documents import Document




class RouteDecision(BaseModel):

    route: Literal["kb", "direct"] = Field(description="The route to take for answering the question: 'kb' for knowledge base, 'direct' for direct answer.")

class EvidenceGrade(BaseModel):
    grade:Literal["good", "weak"] =Field(description="The grade of the evidence: 'good' for reliable evidence, 'weak' for unreliable evidence.")


class WebScope(BaseModel):
    scope: Literal["external", "company"] = Field(description="'external' if public web pages can answer the question (a public product or general technology); 'company' if the answer depends on this company's own policies, benefits, people or systems.")


class AgentState(TypedDict):
    """
    Represents the state of an agent, including its name, description, and associated documents.
    """

    question: str
    current_query: str
    kb_docs: List[Document]
    web_results: str
    kb_grade: str
    web_grade: str
    web_scope: str
    answer: str
    source_used: str
    retry_count: int
    trace: List[str]
    citations: List[dict]