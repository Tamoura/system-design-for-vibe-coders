# labs/m14/demo.py
"""Lab 14.2: twelve questions through the router, the retry layer and the cost layer, written to usage.jsonl. Offline with the mock.
  python labs/m14/demo.py && python labs/m14/report.py usage.jsonl --resolved 9"""
import json
from pathlib import Path

import anthropic
import cost
from reliable import Reliable
from router import TIERS, answer_with_escalation

DATA = Path(__file__).resolve().parents[2] / "labkit" / "data"
QUESTIONS = [(r["question"], r["relevant"]) for r in map(json.loads, (DATA / "m04_questions.jsonl").read_text().splitlines())]
QUESTIONS += [("Compare the remote work and VPN rules for tickets 4471 4472 4473", ["remote-work", "vpn"]), ("What is the weather in Doha?", [])]


def main() -> None:
    pipe = Reliable(cost.Tracked(anthropic.Anthropic(max_retries=0), budget=1.0), fallback=TIERS[1])
    for i, (question, docs) in enumerate(QUESTIONS):
        body = "".join(f'<document id="{d}">{(DATA / "policies" / f"{d}.md").read_text()}</document>' for d in docs) + question

        def ask(model, body=body, convo=f"c{i // 2}"):                  # two questions per conversation
            resp = pipe.create(model=model, max_tokens=1024, output_config={"effort": "low"}, convo=convo,
                               messages=[{"role": "user", "content": body}])
            return next((b.text for b in resp.content if b.type == "text"), "")
        text, tried = answer_with_escalation(ask, question)
        print(f"{tried[-1]:<18} tried {len(tried)}  {question[:40]:<40} -> {text[:40]}")


if __name__ == "__main__":
    main()
