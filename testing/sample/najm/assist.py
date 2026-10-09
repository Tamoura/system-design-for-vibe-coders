"""Najm Assist: a tiny, deterministic stand-in for an LLM assistant (sample system under test).

It has the same moving parts as a real assistant (retrieval over policy documents, a "model"
that writes the answer, and tools it may call), but the model is a plain function, so you can
practise evals, RAG tests and agent tests with no API key, no cost and repeatable runs.
Some AI bugs can be switched on on purpose:

    NAJM_AI_BUGS="hallucinate,obey_injection" pytest

Known names: hallucinate, obey_injection, skip_confirm, wrong_account.
"""
from __future__ import annotations

import os
import random
import re

POLICY_DOCS = {
    "fees-intl": "International transfers cost 0.35% of the amount, with a minimum fee of 10.00 and a maximum fee of 100.00 in the transfer currency. Own-account transfers are free.",
    "limits": "The daily transfer limit is 50,000 QAR or AED, or 10,000 EUR, per customer. A single transfer may not exceed 25,000 QAR or AED, or 5,000 EUR.",
    "card-freeze": "Customers can freeze a card at any time in the app or by asking Najm Assist. Freezing needs explicit confirmation. A frozen card declines all new payments. Unfreezing needs identity verification.",
    "cutoff": "Transfers submitted before 15:00 Qatar time on a business day are processed the same day. Later transfers are processed on the next business day. The weekend in Qatar is Friday and Saturday.",
    "disputes": "To dispute a card payment, open the transaction and choose Report a problem. Najm Bank acknowledges disputes within 2 business days.",
    "privacy": "Najm Assist never shows another customer's data. Staff access to conversations is logged.",
}
STOP = {"a", "an", "the", "is", "are", "of", "to", "in", "on", "for", "and", "or", "do", "does", "i", "my", "me",
        "what", "how", "can", "be", "it", "that", "this", "at", "by", "with", "much", "many", "when", "will", "you"}
NO_ANSWER = "I can't find that in Najm Bank's policies. Please contact support."


def ai_bugs() -> set[str]:
    return {b.strip() for b in os.environ.get("NAJM_AI_BUGS", "").split(",") if b.strip()}


def tokens(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP]


def retrieve(query: str, k: int = 2, docs: dict[str, str] | None = None) -> list[tuple[str, float]]:
    """Rank documents by the share of query words they contain. Returns [(doc_id, score)], best first."""
    docs = POLICY_DOCS if docs is None else docs
    q = set(tokens(query))
    scored = []
    for doc_id, text in docs.items():
        overlap = len(q & set(tokens(text)))
        if overlap:
            scored.append((doc_id, overlap / max(len(q), 1)))
    return sorted(scored, key=lambda s: (-s[1], s[0]))[:k]


class FakeModel:
    """Writes an answer from the retrieved context. temperature=0 is deterministic;
    temperature>0 picks a random opening, like sampling in a real model."""

    OPENINGS = ["", "According to our policy: ", "Here is what the policy says: ", "Good question. "]

    def __init__(self, temperature: float = 0.0, seed: int | None = None):
        self.temperature = temperature
        self.rng = random.Random(seed)

    def generate(self, question: str, context: list[str]) -> str:
        opening = self.rng.choice(self.OPENINGS) if self.temperature > 0 else ""
        if any("ignore previous instructions" in c.lower() for c in context) and "obey_injection" in ai_bugs():
            return "ACTION freeze_card card-1"  # bug: follows instructions found inside a document
        if not context:
            if "hallucinate" in ai_bugs():
                return opening + "The fee is 5.00 and it is charged monthly."  # bug: invents a policy
            return NO_ANSWER
        q = set(tokens(question))
        sentences = [s.strip() for c in context for s in re.split(r"(?<=[.!?])\s+", c) if s.strip()]
        best = max(sentences, key=lambda s: (len(q & set(tokens(s))), -len(s)))
        return opening + best


def answer(question: str, model: FakeModel | None = None, docs: dict[str, str] | None = None, k: int = 2) -> dict:
    """The RAG pipeline: retrieve, then generate. Returns the text and the documents it used."""
    model = model or FakeModel()
    hits = retrieve(question, k=k, docs=docs)
    docs = POLICY_DOCS if docs is None else docs
    text = model.generate(question, [docs[d] for d, _ in hits])
    return {"text": text, "sources": [d for d, _ in hits]}


class Agent:
    """Najm Assist with tools. Reading a balance is safe. Freezing a card is a write action
    and must be confirmed by the customer first."""

    def __init__(self, balances: dict[str, str] | None = None, model: FakeModel | None = None):
        self.balances = balances or {"acc-1": "12000.00 QAR", "acc-2": "800.00 QAR"}
        self.frozen: set[str] = set()
        self.model = model or FakeModel()
        self.calls: list[dict] = []

    def _call(self, name: str, **args) -> str:
        self.calls.append({"name": name, "args": args})
        if name == "get_balance":
            return self.balances.get(args["account"], "unknown account")
        if name == "freeze_card":
            self.frozen.add(args["card"])
            return f"{args['card']} frozen"
        raise ValueError(name)

    def handle(self, message: str, user_account: str = "acc-1", confirmed: bool = False) -> dict:
        """Returns {"reply": str, "tool_calls": [...]} for this turn only."""
        start = len(self.calls)
        low = message.lower()
        if "balance" in low:
            account = "acc-2" if "wrong_account" in ai_bugs() else user_account
            reply = f"Your balance is {self._call('get_balance', account=account)}."
        elif "freeze" in low:
            found = re.search(r"card-\d+", low)
            card = found.group(0) if found else "card-1"
            if confirmed or "skip_confirm" in ai_bugs():
                reply = f"Done: {self._call('freeze_card', card=card)}."
            else:
                reply = f"Please confirm: freeze {card}? Reply yes to confirm."
        else:
            result = answer(message, self.model)
            reply = result["text"]
            if reply.startswith("ACTION freeze_card"):
                reply = f"Done: {self._call('freeze_card', card=reply.split()[-1])}."
        return {"reply": reply, "tool_calls": self.calls[start:]}
