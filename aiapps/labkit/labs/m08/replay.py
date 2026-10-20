# labs/m08/replay.py
"""Lab 8.2: read a trace as a story.   python labs/m08/replay.py m08_trace.jsonl [RUN_ID]"""
import json
import sys
from collections import defaultdict


def load(path):
    runs = defaultdict(list)
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                e = json.loads(line)
                runs[e["run"]].append(e)
    return runs


def story(events):
    out = []
    for e in events:
        kind = e["event"]
        if kind == "start":
            out.append(f"run {e['run']}: {e['goal']}   (limits: {e['max_steps']} steps, {e['token_budget']} tokens, {e['timeout_s']} s)")
        elif kind == "model":
            out.append(f"  step {e['step']}  model {e['stop_reason']:<9} in={e['input_tokens']} out={e['output_tokens']} total={e['total_tokens']}  {e['ms']} ms")
        elif kind == "model_error":
            out.append(f"  step {e['step']}  model ERROR {e['error']} status={e['status']}  {e['ms']} ms")
        elif kind == "tool":
            what = f"REFUSED ({e['refused']})" if "refused" in e else f"{e['result_chars']} chars, {'ERROR' if e['is_error'] else 'ok'}, {e['ms']} ms"
            out.append(f"          tool  {e['tool']} {json.dumps(e['input'])} -> {what}")
        elif kind == "stop":
            out.append("  DONE" if e["reason"] == "done" else f"  STOPPED by {e['reason']}: {e['why']} -> handed to a person")
            out.append(f"  {e['step']} steps, {e['tokens']} tokens, {e['seconds']} s")
    if not any(e["event"] == "stop" for e in events):
        out.append("  NO STOP LINE: the process died or was killed here")
    return "\n".join(out)


if __name__ == "__main__":
    runs = load(sys.argv[1])
    wanted = sys.argv[2:3] or list(runs)
    print("\n\n".join(story(events) for run_id, events in runs.items() if run_id in wanted))
