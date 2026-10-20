# labs/m13/pack_check.py
"""Lab 13.2: check a governance pack. A document is evidence only if it is complete, signed and still true.
  python labs/m13/pack_check.py PACK_DIR              a finished pack: no TODO left, every signer approved, tool list matches the rules
  python labs/m13/pack_check.py PACK_DIR --structure  a blank template folder: sections must exist, TODO is allowed
Exit code 0 when there is nothing to fix, 1 otherwise. It checks form and drift. Whether the content is GOOD is for Layla's review."""
import re
import sys
from pathlib import Path

from guardrails import NAJM_DESK_V1

SIGN = "Sign-off"
REQUIRED = {       # file -> (sections it must have, people who must sign it)
    "system_card.md": (["Purpose and scope", "Tools and permissions", "Data and models", "Evaluation results", "Known limits", SIGN], ["Layla", "Noura"]),
    "risk_register.md": (["Risks", SIGN], ["Layla", "Noura", "Hamad"]),
    "dpia_trigger.md": (["Screening questions", "Decision", SIGN], ["Sara"]),
    "change_policy.md": (["What counts as a change", "Review and evaluation", "Rollout and rollback", SIGN], ["Layla", "Noura"]),
    "approval_records.md": (["Approvals", SIGN], ["Noura"]),
    "vendor_assessment.md": (["Provider and models", "Data handling and residency", "Security and compliance evidence", "Continuity and exit", SIGN],
                             ["Layla", "Hamad", "Sara"]),
    "oversight_evidence.md": (["Who oversees what", "Evidence", "Stop and escalation", SIGN], ["Layla", "Hamad"]),
}


def sections(text):
    """{heading: body} for every '## ' heading in a markdown file."""
    parts = re.split(r"^## (.+?)\s*$", text, flags=re.M)
    return {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)}


def check(pack, structure_only=False):
    """Return a list of problems; an empty list is a pass."""
    problems = []
    for name, (wanted, signers) in REQUIRED.items():
        path = Path(pack) / name
        if not path.exists():
            problems.append(f"{name}: missing")
            continue
        found = sections(path.read_text(encoding="utf-8"))
        for title in wanted:
            if title not in found:
                problems.append(f"{name}: no section '{title}'")
            elif not found[title].strip():
                problems.append(f"{name}: section '{title}' is empty")
            elif "TODO" in found[title] and not structure_only:
                problems.append(f"{name}: section '{title}' still has a TODO")
        if structure_only:
            continue
        for who in signers:           # a row like: | Layla | Head of AI Governance | approved | 2026-11-02 |
            if not re.search(rf"^\|\s*{who}\s*\|[^\n]*\|\s*approved\s*\|\s*\d{{4}}-\d{{2}}-\d{{2}}\s*\|", found.get(SIGN, ""), re.M | re.I):
                problems.append(f"{name}: {who} has not approved")
        if name == "system_card.md":  # drift: the card must describe the tool surface the gate really enforces
            said = set(re.findall(r"`(\w+)`", found.get("Tools and permissions", "")))
            if said != set(NAJM_DESK_V1):
                problems.append(f"{name}: tools differ from guardrails.py: {sorted(said ^ set(NAJM_DESK_V1))}")
    return problems


if __name__ == "__main__":
    folders = [a for a in sys.argv[1:] if not a.startswith("--")]
    found_problems = check(folders[0], "--structure" in sys.argv)
    print("\n".join(found_problems) or "nothing to fix")
    sys.exit(1 if found_problems else 0)
