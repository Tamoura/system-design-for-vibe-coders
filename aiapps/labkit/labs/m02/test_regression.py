# labs/m02/test_regression.py
"""The eval gate: run it in CI when a prompt file, the model id or the grader changes.
  PROMPT=classify_v3 pytest labs/m02/test_regression.py"""
import os
import re

import run_eval
from promptfile import load_prompt

PROMPT = os.environ.get("PROMPT", "classify_v3")             # the prompt in production, or about to be
THRESHOLD = float(os.environ.get("EVAL_THRESHOLD", "0.85"))  # a little below the dev score you accepted: room for noise
REPS = int(os.environ.get("EVAL_REPS", "1"))                 # 3 on the real API, where nothing freezes the variance


def test_dev_accuracy_stays_above_the_threshold():
    result = run_eval.run(PROMPT, "dev", REPS)               # the gate runs on dev; held_out is for the human decision
    assert result["accuracy"] >= THRESHOLD, f"{result['prompt_version']} scored {result['accuracy']:.0%} on dev"


def test_no_example_is_copied_from_the_eval_set():
    examples = re.findall(r'^Example: "(.+?)" =>', load_prompt(PROMPT).text, re.M)
    tickets = {row["text"].lower() for row in run_eval.load_cases("all")}
    assert not [e for e in examples if e.lower() in tickets], "an example is an eval ticket: the score proves nothing"
