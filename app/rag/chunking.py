"""Corpus-aware chunking for the IT support knowledge base.

- Markdown files are split on `##` headings (`###` sub-headings stay inside their
  section) and each chunk is prefixed with "<doc title> > <section>" so the embedding
  keeps its context. Tables are never split; oversized sections are split on blank lines.
- YAML frontmatter (doc_id, status, published, category) becomes chunk metadata.
- Past tickets (tickets/*.jsonl) become one chunk per ticket.
- Every chunk gets a stable `chunk_id`, so re-ingesting overwrites instead of duplicating.
"""
import json
import re
from pathlib import Path

from langchain_core.documents import Document

MAX_CHARS = 1500


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    meta: dict = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].strip().splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    meta[key.strip()] = value.strip()
            text = text[end + 4:].lstrip("\n")
    return meta, text


def _split_blocks(body: str) -> list[str]:
    blocks, current = [], []
    for line in body.splitlines():
        if line.strip() == "":
            if current:
                blocks.append("\n".join(current))
                current = []
        else:
            current.append(line)
    if current:
        blocks.append("\n".join(current))
    return blocks


def _pack(blocks: list[str]) -> list[str]:
    pieces, current = [], ""
    for block in blocks:
        if current and len(current) + len(block) + 2 > MAX_CHARS:
            pieces.append(current)
            current = block
        else:
            current = f"{current}\n\n{block}" if current else block
    if current:
        pieces.append(current)
    return pieces


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "section"


def chunk_markdown_file(path: Path, root: Path) -> list[Document]:
    meta, text = _parse_frontmatter(path.read_text(encoding="utf-8"))
    doc_id = meta.get("doc_id") or path.stem
    title = meta.get("title") or path.stem

    sections: list[tuple[str, list[str]]] = []
    heading, lines, in_code = title, [], False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
        match = None if in_code else re.match(r"^##\s+(.*)", line)
        if match:
            sections.append((heading, lines))
            heading, lines = match.group(1).strip(), []
        else:
            lines.append(line)
    sections.append((heading, lines))

    docs: list[Document] = []
    for heading, body_lines in sections:
        body = "\n".join(body_lines).strip()
        if len(body) < 40 or heading.lower() == "table of contents":
            continue
        for part, piece in enumerate(_pack(_split_blocks(body))):
            docs.append(Document(
                page_content=f"{title} > {heading}\n\n{piece}",
                metadata={
                    "chunk_id": f"{_slug(doc_id)}::{_slug(heading)}::{part}",
                    "source_file": path.relative_to(root).as_posix(),
                    "doc_id": doc_id,
                    "title": title,
                    "section": heading,
                    "part": part,
                    "status": meta.get("status", "active"),
                    "published": meta.get("published", ""),
                    "category": meta.get("category", ""),
                    "type": "document",
                },
            ))
    return docs


def chunk_ticket_file(path: Path, root: Path) -> list[Document]:
    docs: list[Document] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        t = json.loads(line)
        docs.append(Document(
            page_content=(
                f"Ticket {t['ticket_id']}: {t['title']}\n"
                f"Category: {t['category']} | Priority: {t['priority']}\n"
                f"Problem: {t['description']}\n"
                f"Resolution: {t['resolution']}"
            ),
            metadata={
                "chunk_id": f"ticket::{_slug(t['ticket_id'])}::0",
                "source_file": path.relative_to(root).as_posix(),
                "doc_id": t["ticket_id"],
                "title": t["title"],
                "section": "ticket",
                "part": 0,
                "status": "active",
                "published": "",
                "category": t["category"],
                "related_docs": t.get("related_docs", []),
                "security_incident": bool(t.get("security_incident", False)),
                "type": "ticket",
            },
        ))
    return docs


def load_kb_chunks(kb_dir: Path) -> list[Document]:
    """Load every markdown file and past ticket under kb_dir as chunked Documents."""
    kb_dir = Path(kb_dir)
    docs: list[Document] = []
    for md in sorted(kb_dir.rglob("*.md")):
        docs.extend(chunk_markdown_file(md, kb_dir))
    tickets_dir = kb_dir / "tickets"
    if tickets_dir.is_dir():
        for jsonl in sorted(tickets_dir.glob("*.jsonl")):
            docs.extend(chunk_ticket_file(jsonl, kb_dir))

    ids = [d.metadata["chunk_id"] for d in docs]
    duplicates = {i for i in ids if ids.count(i) > 1}
    if duplicates:
        raise ValueError(f"Duplicate chunk ids (check repeated headings): {sorted(duplicates)}")
    return docs
