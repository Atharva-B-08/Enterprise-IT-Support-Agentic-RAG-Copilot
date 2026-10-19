#!/usr/bin/env python3
"""Header-based chunker for the Nimbus IT support corpus.

Usage:  python3 chunk_docs.py [data_dir] [output.jsonl]

- Splits markdown on ## headings (### sub-headings stay inside their section) and
  keeps the heading path as context. Runbooks/KB articles with only a # title become one chunk.
- Never splits inside a table; oversized sections are split on blank lines.
- Carries YAML frontmatter (doc_id, status, published...) into every chunk's metadata,
  so your retriever can filter out `status: superseded` documents.
- Turns each past ticket (JSONL) into one chunk.
"""
import json
import re
import sys
from pathlib import Path

MAX_CHARS = 1500

DATA_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else DATA_DIR / "chunks.jsonl"


def parse_frontmatter(text):
    meta = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
            text = text[end + 4:].lstrip("\n")
    return meta, text


def split_blocks(body):
    """Split a section body into blocks, keeping tables and lists together."""
    blocks, cur = [], []
    for line in body.splitlines():
        if line.strip() == "":
            if cur:
                blocks.append("\n".join(cur))
                cur = []
        else:
            cur.append(line)
    if cur:
        blocks.append("\n".join(cur))
    return blocks


def pack(blocks):
    """Group blocks into pieces no larger than MAX_CHARS (a single block may exceed it)."""
    pieces, cur = [], ""
    for b in blocks:
        if cur and len(cur) + len(b) + 2 > MAX_CHARS:
            pieces.append(cur)
            cur = b
        else:
            cur = f"{cur}\n\n{b}" if cur else b
    if cur:
        pieces.append(cur)
    return pieces


def chunk_markdown(path):
    raw = path.read_text(encoding="utf-8")
    meta, text = parse_frontmatter(raw)
    doc_id = meta.get("doc_id") or path.stem
    title = meta.get("title") or path.stem
    status = meta.get("status", "active")

    # Walk lines, tracking heading path
    sections = []  # (heading_path, body_lines)
    path_stack = {}
    cur_path, cur_lines = [title], []
    in_code = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
        m = None if in_code else re.match(r"^(#{1,3})\s+(.*)", line)
        if m and len(m.group(1)) == 2:
            # Split only on ## headings; ### sub-headings stay inside the body so
            # small subsections are not turned into tiny, context-poor chunks.
            if cur_lines:
                sections.append((cur_path, cur_lines))
            cur_path = [title, m.group(2).strip()]
            cur_lines = []
            continue
        cur_lines.append(line)
    if cur_lines:
        sections.append((cur_path, cur_lines))

    chunks = []
    for hpath, lines in sections:
        body = "\n".join(lines).strip()
        if len(body) < 40:  # skip empty headings / table of contents stubs
            continue
        if body.lstrip().startswith("1. [") and "#" in body[:80]:  # table of contents
            continue
        for i, piece in enumerate(pack(split_blocks(body))):
            context = " > ".join(hpath)
            chunks.append({
                "text": f"{context}\n\n{piece}",
                "metadata": {
                    "source_file": str(path.relative_to(DATA_DIR)),
                    "doc_id": doc_id,
                    "title": title,
                    "section": hpath[-1],
                    "section_path": hpath,
                    "part": i,
                    "status": status,
                    "published": meta.get("published", ""),
                    "category": meta.get("category", ""),
                    "type": "document",
                },
            })
    return chunks


def chunk_tickets(path):
    chunks = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        t = json.loads(line)
        text = (
            f"Ticket {t['ticket_id']}: {t['title']}\n"
            f"Category: {t['category']} | Priority: {t['priority']}\n"
            f"Problem: {t['description']}\n"
            f"Resolution: {t['resolution']}"
        )
        chunks.append({
            "text": text,
            "metadata": {
                "source_file": str(path.relative_to(DATA_DIR)),
                "doc_id": t["ticket_id"],
                "title": t["title"],
                "section": "ticket",
                "section_path": [t["ticket_id"]],
                "part": 0,
                "status": "active",
                "published": "",
                "category": t["category"],
                "related_docs": t.get("related_docs", []),
                "security_incident": t.get("security_incident", False),
                "type": "ticket",
            },
        })
    return chunks


def main():
    all_chunks = []
    for md in sorted(DATA_DIR.rglob("*.md")):
        if "eval" in md.parts:
            continue
        all_chunks.extend(chunk_markdown(md))
    for tj in sorted((DATA_DIR / "tickets").glob("*.jsonl")):
        all_chunks.extend(chunk_tickets(tj))

    with OUT.open("w", encoding="utf-8") as f:
        for i, c in enumerate(all_chunks):
            c["id"] = f"chunk-{i:04d}"
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    sizes = [len(c["text"]) for c in all_chunks]
    by_type = {}
    for c in all_chunks:
        by_type[c["metadata"]["type"]] = by_type.get(c["metadata"]["type"], 0) + 1
    print(f"Wrote {len(all_chunks)} chunks to {OUT}")
    print(f"By type: {by_type}")
    print(f"Chars per chunk: min={min(sizes)} avg={sum(sizes)//len(sizes)} max={max(sizes)}")
    superseded = sum(1 for c in all_chunks if c["metadata"]["status"] == "superseded")
    print(f"Chunks from superseded docs (filter these out at query time): {superseded}")


if __name__ == "__main__":
    main()
