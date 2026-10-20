# labs/m11/compare.py
"""Lab 11.2: does the team earn its extra calls? Five questions through the team, then one agent.
  python labs/m11/compare.py    (for money, set PRICE_IN_PER_MTOK and PRICE_OUT_PER_MTOK from the price page)"""
import os

from team import Team

TASKS = [("How do I request a new laptop?", "Hardware > New device"), ("I lost my phone: what do I do about MFA?", "Service Desk immediately"),
         ("What is the response time for a P2 ticket?", "within 4 hours"), ("When is the Service Desk open?", "7:00 to 17:00"),
         ("Can I paste customer data into an external AI tool?", "must not")]      # (question, a phrase a right answer contains)
PRICE = [float(os.environ.get(k, 0)) for k in ("PRICE_IN_PER_MTOK", "PRICE_OUT_PER_MTOK")]


def compare():
    total = {"team": [0, 0, 0], "solo": [0, 0, 0]}                              # calls, input tokens, output tokens
    for question, expect in TASKS:
        for mode in total:
            t = Team(question)
            r = t.run() if mode == "team" else t.run_solo()
            row = [t.calls, sum(v[1] for v in t.by_role.values()), sum(v[2] for v in t.by_role.values())]
            total[mode] = [a + b for a, b in zip(total[mode], row)]
            print(f"{question:<54}{mode:<5}{('right' if expect in r.answer else 'wrong') if r.ok else r.reason:<8}calls={row[0]} in={row[1]} out={row[2]}")
    for mode, (calls, tin, tout) in total.items():
        print(f"{mode}: {calls} calls, {tin + tout} tokens" + (f", cost {(tin * PRICE[0] + tout * PRICE[1]) / 1e6:.4f}" if all(PRICE) else ""))
    t, s = total["team"], total["solo"]
    print(f"team / solo: calls x{t[0] / s[0]:.1f}, tokens x{(t[1] + t[2]) / (s[1] + s[2]):.1f}")


if __name__ == "__main__":
    compare()
