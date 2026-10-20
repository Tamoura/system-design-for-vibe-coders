# labs/m13/guardrails.py
"""Lab 13.1: guardrails are plain code between "asked" and "done"."""
import html
import json
import re
import time
from dataclasses import dataclass, field
from urllib.parse import urlparse

# A speed bump, not a wall: it misses "Summer2026! is my password".
PII = {"secret": r"(?i)\b(?:password|passcode|pwd)\s*(?:is|=|:)\s*\S+", "card": r"\b(?:\d[ -]?){13,16}\b"}


def mask_pii(text):
    """Return the clean text and the kinds found: kinds are safe to log, values are not."""
    kinds = []
    for kind, pattern in PII.items():
        text, n = re.subn(pattern, f"[{kind} removed]", text)
        kinds += [kind] * n
    return text, kinds


def check_output(text, html_out=False):
    """Last stop before a screen: drop other hosts' links (a markdown image leaks with no click), mask, encode."""
    found = []

    def link(m):
        host = urlparse(m.group(0).rstrip(".,")).hostname or ""
        if host == "najm.example" or host.endswith(".najm.example"):
            return m.group(0)
        found.append("link:" + host)
        return "[link removed]"

    text, kinds = mask_pii(re.sub(r"(?i)(?<![\w/])(?:https?:)?//[^\s)\]]+", link, text))     # any case, and //host links
    return (html.escape(text) if html_out else text), found + kinds


@dataclass
class Rule:
    mode: str                  # "read" or "write"
    scope: str                 # the USER must hold it: the agent never has more than the user
    params: tuple              # the only arguments allowed: a closed schema
    max_calls: int = 10        # calls per conversation (a gateway adds per-minute limits)
    owner_arg: str = ""        # must name a ticket the user owns
    self_arg: str = ""         # must name the user, never someone else
    approval: bool = False     # a person approves the exact call first
    untrusted: bool = False    # the result is text strangers can write: reading it taints the session


@dataclass
class Session:
    user: str                  # from the login, never from a tool argument
    scopes: frozenset
    owns: set                  # ticket ids this user owns
    said: str = ""
    tainted: bool = False
    calls: dict = field(default_factory=dict)


NAJM_DESK_V1 = {               # the permissions matrix (lesson 6.2) as reviewed data, plus this lab's two comment tools. No send_email: v1 has no outward channel.
    "search_policies": Rule("read", "policies:read", ("query",), untrusted=True),
    "get_ticket_status": Rule("read", "tickets:read", ("ticket_id",), owner_arg="ticket_id"),
    "get_ticket_notes": Rule("read", "tickets:read", ("ticket_id",), owner_arg="ticket_id", untrusted=True),
    "add_comment": Rule("write", "tickets:comment", ("ticket_id", "text"), max_calls=5, owner_arg="ticket_id"),
    "request_unlock": Rule("write", "unlock:request", ("employee", "reason"), max_calls=2, self_arg="employee", approval=True),
}


def screen(s, name, args):
    """What a person reads before saying yes, built from the real arguments: a model's own summary can be steered."""
    return (f"{s.user} wants {name} {json.dumps(args, sort_keys=True)}\n  in their words: {s.said[:80]!r}\n"
            f"  untrusted text read in this chat: {'YES, take care' if s.tainted else 'no'}\n  default: NO.  approve? [y/N]")


class Gate:
    def __init__(self, rules=NAJM_DESK_V1, approve=lambda text: False, skip=()):
        self.rules, self.approve, self.skip, self.log = rules, approve, set(skip), []

    def check(self, s, name, args):
        """Return (ok, layer, reason). Cheap layers first; `skip` is for experiments."""
        r = self.rules.get(name)
        layers = [("allowlist", not r, f"{name!r} is not a tool this agent has")]
        if r:
            strings = all(isinstance(v, str) for v in args.values())
            layers += [("scope", r.scope not in s.scopes, f"you lack the scope {r.scope}"),
                       ("params", set(args) != set(r.params) or not strings, f"{name} takes exactly {list(r.params)}"),
                       ("owner", bool(r.owner_arg) and str(args.get(r.owner_arg)) not in s.owns
                        or bool(r.self_arg) and str(args.get(r.self_arg)).lower() != s.user, "not found for you"),
                       ("rate", len(s.calls.get(name, [])) >= r.max_calls, "too many calls"),
                       ("taint", r.mode == "write" and s.tainted, "this chat read text others wrote")]
        for layer, objects, why in layers:
            if layer not in self.skip and objects:
                return self._done(s, name, args, False, layer, why)
        if r and r.approval and "approval" not in self.skip and not self.approve(screen(s, name, args)):     # a person is asked last
            return self._done(s, name, args, False, "approval", "no person approved it")
        s.calls.setdefault(name, []).append(args)
        return self._done(s, name, args, True, "", "")

    def _done(self, s, name, args, ok, layer, why):
        """One audit row per decision, masked and clipped: the log must not become the leak."""
        self.log.append({"seq": len(self.log) + 1, "ts": round(time.time(), 3), "user": s.user, "tool": name,
                         "args": {k: mask_pii(str(v))[0][:60] for k, v in args.items()},
                         "decision": "allow" if ok else "refuse", "layer": layer, "reason": why})
        return ok, layer, why
