# labs/m11/contracts.py
"""Lab 11.2: the hand-off contracts. Every message between two agents is one of these models, validated by the supervisor."""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid")         # a field nobody agreed on is a breach


class Brief(Contract):                                # supervisor -> researcher
    question: str = Field(min_length=10, max_length=300)


class Finding(Contract):
    source: str = Field(pattern=r"^[a-z0-9-]+$")      # a policy id, such as laptop-requests
    quote: str = Field(min_length=10, max_length=600)  # copied word for word from that policy


class Notes(Contract):                                # researcher -> writer
    findings: list[Finding] = Field(max_length=5)
    gaps: list[str]                                   # what the policies do not say; often empty


class Draft(Contract):                                # writer -> reviewer (the solo agent too)
    answer: str = Field(min_length=20, max_length=1200)
    citations: list[str] = Field(min_length=1)        # an answer with no source is not an answer


class Review(Contract):                               # reviewer -> supervisor
    verdict: Literal["approve", "revise"]
    issues: list[str]

    @model_validator(mode="after")
    def revise_needs_reasons(self):
        if self.verdict == "revise" and not self.issues:
            raise ValueError("a revise verdict must list at least one issue")
        return self


def check_notes(notes: Notes, seen: dict[str, str]) -> None:
    """What a schema cannot hold. `seen` is what the search tool really returned: the ground truth for every quote."""
    for f in notes.findings:
        if " ".join(f.quote.split()) not in " ".join(seen.get(f.source, "").split()):
            raise ValueError(f"the quote for {f.source!r} is not word for word in a policy the search returned")


def check_citations(draft: Draft, allowed: set[str]) -> None:
    stray = sorted(set(draft.citations) - allowed)
    if stray:
        raise ValueError(f"the draft cites {stray}, which are not among the sources it was given")


def describe(e: ValueError) -> str:
    """A broken contract as one line the offending agent can act on (a pydantic ValidationError is a ValueError)."""
    if isinstance(e, ValidationError):
        return "; ".join(f"{'.'.join(map(str, x['loc'])) or 'reply'}: {x['msg']}" for x in e.errors())
    return str(e)
