# labs/m10/ticket_server.py
"""Lab 10.2: the Najm Desk ticket system as an MCP server. Identity and scopes come from whoever starts the process, never from
the model: TICKETHUB_USER (default Rayan), TICKETHUB_SCOPES (default "tickets:read"). Scopes: tickets:read = your own tickets (the read
tools always exist), tickets:read:all = any ticket (desk agents), tickets:write = file tickets for you.
  python labs/m10/ticket_server.py    (stdio: a host starts this process)
Never print() to stdout (the protocol channel). The audit log goes to stderr."""
import json
import os
import re
import sys
from pathlib import Path
from typing import Annotated, Literal

from mcp.server.mcpserver import MCPServer      # called FastMCP in mcp 1.x
from mcp.types import ToolAnnotations
from pydantic import Field

DATA = Path(__file__).resolve().parents[2] / "labkit" / "data"
TicketId = Annotated[str, Field(pattern=r"^\d{4,6}$", description="Ticket number, digits only, for example 4471")]
READ = ToolAnnotations(read_only_hint=True, destructive_hint=False, idempotent_hint=True)
WRITE = ToolAnnotations(read_only_hint=False, destructive_hint=False, idempotent_hint=False)


def audit(user: str, tool: str, outcome: str, **fields) -> None:
    """One JSON line per call on stderr: who, which tool, which arguments (ids, enums, the LENGTH of free text; never ticket
    text) and the outcome. The log may say what the caller is not told."""
    print(json.dumps({"user": user, "tool": tool, **fields, "outcome": outcome}), file=sys.stderr, flush=True)


def line(t: dict) -> str:
    return f"Ticket {t['id']}: {t['status']} ({t['category']}, {t['priority']}): {t['summary']}"


def build_server(tickets_file=DATA / "tickets.json", user: str | None = None, scopes: str | None = None) -> MCPServer:
    tickets = json.loads(Path(tickets_file).read_text(encoding="utf-8"))     # a private copy: a write never touches the file
    for tid, owner in json.loads((DATA / "m10_ticket_owners.json").read_text(encoding="utf-8")).items():
        tickets.get(tid, {}).setdefault("requested_by", owner)               # TicketHub would know who raised each ticket
    who = user or os.environ.get("TICKETHUB_USER", "Rayan")
    granted = set((scopes or os.environ.get("TICKETHUB_SCOPES", "tickets:read")).split())
    mcp = MCPServer("tickethub")

    def may_read(t: dict) -> bool:                                           # checked on EVERY ticket: ids are untrusted input
        return "tickets:read:all" in granted or t.get("requested_by", "").lower() == who.lower()

    @mcp.tool(annotations=READ, description=(
        "Look up one IT ticket by its number: status, category, priority and summary. "
        "Call this when the user asks about the progress of a ticket they name. Not for topic searches: use search_tickets."))
    def get_ticket_status(ticket_id: TicketId) -> str:
        t = tickets.get(ticket_id)
        seen = t is not None and may_read(t)
        audit(who, "get_ticket_status", "ok" if seen else "hidden" if t else "missing", ticket_id=ticket_id)   # the log tells them apart
        return line(t) if seen else f"No ticket {ticket_id} found for you"             # the caller gets one reply for both

    @mcp.tool(annotations=READ, description=(
        "Find the user's tickets by topic words. Returns at most five matches, one line each. "
        "Call this when the user describes a problem but gives no ticket number."))
    def search_tickets(query: Annotated[str, Field(min_length=2, max_length=100, description="Topic words, for example: vpn drops")]) -> str:
        words = [w for w in re.findall(r"[a-z0-9]{3,}", query.lower()) if w not in {"find", "ticket", "tickets", "about", "the"}]
        hits = sorted((-sum(w in t["summary"].lower() for w in words), t["id"]) for t in tickets.values() if may_read(t))
        found = [line(tickets[i]) for score, i in hits if score][:5]
        audit(who, "search_tickets", "ok", query_chars=len(query), hits=len(found))
        return "\n".join(found) or "No matching tickets"

    if "tickets:write" in granted:                                           # without the scope this tool does not exist
        @mcp.tool(annotations=WRITE, description=(
            "File a new IT ticket for the signed-in user. Call this ONLY when the user explicitly asks to raise one. "
            "The same title from the same user returns the existing ticket."))
        def create_ticket(title: Annotated[str, Field(min_length=5, max_length=120, description="One line, no personal data")],
                          description: Annotated[str, Field(max_length=1000, description="What happened. No passwords.")],
                          category: Literal["hardware", "access", "network", "software", "security", "other"],
                          priority: Annotated[Literal["P2", "P3", "P4"], Field(description="P1 is set by a person, not offered here")]) -> str:
            same = next((t for t in tickets.values() if t.get("requested_by", "").lower() == who.lower() and t["summary"].lower() == title.lower()), None)
            if same:                                                         # idempotent: a retry must not file twice
                audit(who, "create_ticket", "duplicate", ticket_id=same["id"])
                return f"Ticket {same['id']} already exists: {same['summary']}"
            new_id = str(max(int(i) for i in tickets) + 1)
            tickets[new_id] = {"id": new_id, "status": "Open", "category": category, "summary": title, "priority": priority,
                               "description": description, "requested_by": who}
            audit(who, "create_ticket", "created", ticket_id=new_id, category=category, priority=priority, title_chars=len(title))
            return f"Created ticket {new_id}: {title} ({category}, {priority})"

    @mcp.resource("policy://ticket-priorities", mime_type="text/markdown", description="What P1 to P4 mean and how fast each is answered.")
    def ticket_priorities() -> str:
        return (DATA / "policies" / "ticket-priorities.md").read_text(encoding="utf-8")

    return mcp


if __name__ == "__main__":
    build_server().run()      # stdio; run("streamable-http", host="127.0.0.1", port=9910) would serve HTTP
