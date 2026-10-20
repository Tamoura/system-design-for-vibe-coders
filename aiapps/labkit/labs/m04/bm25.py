# labs/m04/bm25.py
"""Lexical search (BM25) and hybrid search (reciprocal rank fusion) over the chunks of rag.py.
  python labs/m04/bm25.py "What are the working from home rules?"      # vector, BM25, hybrid, then the answer"""
import re
import sys

from rank_bm25 import BM25Okapi

import rag


def tokens(text):
    """Lowercase words and numbers without stop words. No stemming: 'working' does not match 'work'."""
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in rag.STOP]


def bm25_search(question, k=3, where=None):
    """Score the visible chunks by exact words. Filter FIRST, then score: hidden chunks must not shape the scores."""
    pool = [c for c in rag.CHUNKS if all(c[field] == value for field, value in (where or {}).items())]
    if not pool:
        return []
    scores = BM25Okapi([tokens(c["text"]) for c in pool]).get_scores(tokens(question))    # rebuilt per call: fine at 34 chunks
    ranked = sorted(zip(scores, pool), key=lambda pair: -pair[0])[:k]
    return [{"id": c["id"], "doc": c["doc"], "text": c["text"], "score": round(float(s), 3)} for s, c in ranked if s > 0]


def rrf(rankings, k=60):
    """Reciprocal rank fusion: a chunk at rank r in a list earns 1 / (k + r); its points from all lists are added.
    Only ranks count, because BM25 scores and cosine similarities are on different scales."""
    fused = {}
    for ranking in rankings:
        for rank, hit in enumerate(ranking, start=1):
            fused.setdefault(hit["id"], {**hit, "score": 0.0})["score"] += 1 / (k + rank)
    return sorted(fused.values(), key=lambda h: -h["score"])


def hybrid_search(question, k=3, where=None, depth=10):
    """Fuse the vector top-`depth` with the BM25 top-`depth`. If neither finds anything, nothing comes back."""
    fused = rrf([rag.retrieve(question, depth, where), bm25_search(question, depth, where)])
    return [{**h, "score": round(h["score"], 4)} for h in fused[:k]]


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "What are the working from home rules?"
    for name, search in (("vector", rag.retrieve), ("bm25", bm25_search), ("hybrid", hybrid_search)):
        print(f"--- {name}")
        for h in search(q, 3, None):
            print(f'{h["score"]:7.3f}  {h["id"]:<20}{h["text"][:40]}…')
    print("--- answer from the hybrid hits")
    print(rag.answer(q, hybrid_search(q)))
