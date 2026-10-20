# labs/m04/compare.py
"""Retrieval only: no answer is generated, so this costs nothing and needs no model.
Vector vs BM25 vs hybrid on the labelled questions, scored by recall@3 and MRR."""
import json

import bm25
import rag

QUESTIONS = rag.KIT / "labkit" / "data" / "m04_questions.jsonl"
METHODS = {"vector": rag.retrieve, "bm25": bm25.bm25_search, "hybrid": bm25.hybrid_search}


def load_questions(path=QUESTIONS):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def first_rank(hits, relevant):
    """Rank (1 = best) of the first chunk that comes from a relevant document, or None."""
    return next((i for i, h in enumerate(hits, 1) if h["doc"] in relevant), None)


def recall_at_k(hits, relevant, k=3):
    """The share of the relevant documents that appear in the top k chunks."""
    return len({h["doc"] for h in hits[:k]} & set(relevant)) / len(relevant)


def evaluate(search, questions, k=3):
    """Run every question through `search` (a function of question, k, where) and score the top k chunks."""
    rows = []
    for q in questions:
        hits = search(q["question"], k, None)
        rows.append({"id": q["id"], "hits": [h["id"] for h in hits], "rank": first_rank(hits, q["relevant"]),
                     "recall": recall_at_k(hits, q["relevant"], k)})
    n = len(rows)
    return {"recall": sum(r["recall"] for r in rows) / n, "mrr": sum(1 / r["rank"] for r in rows if r["rank"]) / n, "rows": rows}


if __name__ == "__main__":
    questions = load_questions()
    runs = {name: evaluate(search, questions) for name, search in METHODS.items()}
    print(f'{"":<9}' + "".join(f"{name:>10}" for name in runs) + "   (rank of the first right chunk, - = missed)")
    for i, q in enumerate(questions):
        print(f'{q["id"]:<9}' + "".join(f'{run["rows"][i]["rank"] or "-":>10}' for run in runs.values()))
    print(f'{"recall@3":<9}' + "".join(f'{run["recall"]:>10.2f}' for run in runs.values()))
    print(f'{"MRR":<9}' + "".join(f'{run["mrr"]:>10.2f}' for run in runs.values()))
    for row in runs["hybrid"]["rows"]:
        if row["rank"] is None:
            print(f'hybrid missed {row["id"]} and returned: {", ".join(row["hits"]) or "nothing"}')
