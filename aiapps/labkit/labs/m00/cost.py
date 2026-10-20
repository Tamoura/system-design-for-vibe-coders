# labs/m00/cost.py
"""Turn token counts into money and project a pilot's bill. No price is hard-coded: copy the current prices
from the price page into PRICE_IN_PER_MTOK and PRICE_OUT_PER_MTOK (per million tokens), then for example:
  python labs/m00/cost.py --system 1500 --user 60 --answer 250 --turns 6 --conversations 450 --weeks 4"""
import argparse
import os


def call_cost(tokens_in: int, tokens_out: int, price_in: float, price_out: float) -> float:
    """One API call: tokens x price per million tokens."""
    return (tokens_in * price_in + tokens_out * price_out) / 1_000_000


def conversation_tokens(system: int, user: int, answer: int, turns: int) -> tuple[int, int]:
    """Total (input, output) tokens for one chat. Every call resends the system prompt and the whole history:
    call t sends  system + t user messages + (t-1) answers  and receives one answer."""
    return sum(system + t * user + (t - 1) * answer for t in range(1, turns + 1)), turns * answer


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for name, default in [("system", 1500), ("user", 60), ("answer", 250), ("turns", 6), ("conversations", 450), ("weeks", 4)]:
        ap.add_argument(f"--{name}", type=int, default=default)
    a = ap.parse_args()
    t_in, t_out = conversation_tokens(a.system, a.user, a.answer, a.turns)
    n = a.conversations * a.weeks
    print(f"one conversation: in={t_in} out={t_out} tokens;  pilot: {t_in * n:,} in, {t_out * n:,} out over {n:,} conversations")
    p_in, p_out = os.environ.get("PRICE_IN_PER_MTOK"), os.environ.get("PRICE_OUT_PER_MTOK")
    if p_in and p_out:
        one = call_cost(t_in, t_out, float(p_in), float(p_out))
        print(f"cost: {one:.5f} per conversation, {one * n:,.2f} for the pilot; budget at x2: {2 * one * n:,.2f}")
    else:
        print("set PRICE_IN_PER_MTOK and PRICE_OUT_PER_MTOK from the current price page to see money")
