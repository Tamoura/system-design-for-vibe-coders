"""A toy embedding function for offline RAG labs. It is NOT a semantic model.

It hashes words into a fixed-size vector (a "bag of hashed words"), so texts that share words are
close, and texts that share meaning but no words are not. That is enough to see chunking,
retrieval, hybrid search and citations work end to end with no download and no API key; use a
real embedding model for real quality."""
from __future__ import annotations

import hashlib
import math
import re

DIM = 2048
STOP = {"the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "is", "are", "be", "by", "with", "at", "as", "it", "that", "this", "how", "do", "does",
        "i", "my", "me", "we", "our", "you", "your", "can", "what", "when", "will", "not", "must", "may", "should", "if", "so", "from", "have", "has", "who", "which"}


def embed(text: str) -> list[float]:
    vec = [0.0] * DIM
    for w in re.findall(r"[a-z0-9]+", text.lower()):
        if w in STOP:
            continue
        h = int(hashlib.md5(w.encode()).hexdigest(), 16)
        vec[h % DIM] += 1.0
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


try:  # Chroma plug-in, only when chromadb is installed
    from chromadb import Documents, EmbeddingFunction, Embeddings

    class HashEmbedding(EmbeddingFunction):
        def __init__(self) -> None:
            pass

        def __call__(self, input: Documents) -> Embeddings:
            return [embed(t) for t in input]

        @staticmethod
        def name() -> str:
            return "course-hash-embedding"

        def get_config(self) -> dict:
            return {}

        @staticmethod
        def build_from_config(config: dict) -> "HashEmbedding":
            return HashEmbedding()
except Exception:  # pragma: no cover
    HashEmbedding = None  # type: ignore
