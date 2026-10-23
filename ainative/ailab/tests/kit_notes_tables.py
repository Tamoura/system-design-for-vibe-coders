#!/usr/bin/env python3
"""Generate the factual tables of KIT_NOTES.md straight from the base repository's code.

KIT_NOTES.md is the single source of truth for lab writers. Its hand-written text explains; the
parts between ``<!-- BEGIN GENERATED: name -->`` and ``<!-- END GENERATED: name -->`` are produced
here, so a signature or a constant in the notes can never disagree with the code.

    PYTHONPATH=ailab/base/remit/src python tests/kit_notes_tables.py            # print
    PYTHONPATH=ailab/base/remit/src python tests/kit_notes_tables.py --write KIT_NOTES.md

(run from ainative/ailab). tests/test_kit_notes.py fails when the file is out of date.
"""
from __future__ import annotations

import dataclasses
import inspect
import re
import sys
from decimal import Decimal

from ailab import checks as kit_checks, framework as kit_framework, gitutil as kit_gitutil, runner as kit_runner
from najmkit import audit, clock, ids
from remit import (config, corridors, cli, errors, fees, fx, ledger, limits, models, money, notify, screening, service,
                   store)

API: list[tuple[str, object, list[str]]] = [
    ("remit.money", money, ["CURRENCIES", "ROUNDING", "quantize", "Money"]),
    ("remit.corridors", corridors, ["DELIVERY_METHODS", "Corridor", "CORRIDORS", "get_corridor", "corridor_for_code",
                                    "all_corridors", "validate_send"]),
    ("remit.fees", fees, ["FeeTier", "FeeSchedule", "SCHEDULES", "FeeBreakdown", "get_schedule", "explain_fee", "quote_fee"]),
    ("remit.fx", fx, ["QUOTE_TTL", "RateProvider", "StaticRateProvider", "FxQuote", "margin_for", "customer_rate", "fx_quote"]),
    ("remit.limits", limits, ["QATAR_UTC_OFFSET", "QATAR_TZ", "DAILY_EXCEEDED", "MONTHLY_EXCEEDED", "TierLimits", "LIMITS",
                             "HistoryItem", "LimitResult", "limits_for", "to_local", "day_window", "month_window",
                             "check_limits"]),
    ("remit.models", models, ["KYC_TIERS", "LOYALTY_TIERS", "LANGUAGES", "Customer", "Transfer"]),
    ("remit.notify", notify, ["TEMPLATES", "FAILURE_REASONS", "render", "format_money", "format_number", "localize_digits",
                              "failure_reason", "Notification", "Notifier", "InMemoryNotifier", "ConsoleNotifier"]),
    ("remit.service", service, ["Quote", "SendResult", "RemitService"]),
    ("remit.store", store, ["Store"]),
    ("remit.screening  (LEGACY)", screening, ["THRESHOLD", "FUZZY_PERCENT", "MIN_FUZZY_LEN", "MAX_TOKENS", "PARTICLES",
                                              "DEFAULT_WATCHLIST", "Match", "ScreenResult", "tokens", "match_score", "screen",
                                              "screen_names", "load_watchlist"]),
    ("remit.ledger  (LEGACY)", ledger, ["ACCOUNT_PAYOUT", "ACCOUNT_FEE_INCOME", "ACCOUNT_PARTNER", "PARTNER_SHARE",
                                        "customer_account", "post_transfer", "balance", "accounts", "journal", "reset"]),
    ("remit.config", config, ["ENVIRONMENTS", "Config", "load_config"]),
    ("remit.cli", cli, ["main"]),
    ("najmkit.ids", ids, ["new_id", "SequentialIds", "use_generator"]),
    ("najmkit.clock", clock, ["Clock", "SystemClock", "FixedClock", "now", "set_clock", "get_clock", "reset_clock"]),
    ("najmkit.audit", audit, ["ENV_VAR", "configure", "current_path", "log_event", "read_events"]),
]


def public_names(module: object) -> list[str]:
    """Public functions and classes *defined in* ``module``, in source order."""
    return [n for n, v in vars(module).items()
            if not n.startswith("_") and (inspect.isfunction(v) or inspect.isclass(v)) and v.__module__ == module.__name__]


def default_text(value: object) -> str:
    """Readable default values: named constants by name, sentinels as <unset>."""
    if value is kit_gitutil.TOOL_NOISE:
        return "TOOL_NOISE"
    if value is kit_checks.CC_TYPES:
        return "CC_TYPES"
    if type(value) is object:
        return "<unset>"
    return repr(value)


def sig(obj: object, *, drop_self: bool = True, returns: bool = True) -> str:
    """Signature text with annotations as written in the source (no quotes), e.g. ``(amount: Money) -> Money``."""
    try:
        signature = inspect.signature(obj)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return "(...)"
    parts: list[str] = []
    star_done = False
    for param in signature.parameters.values():
        if drop_self and param.name in {"self", "cls"}:
            continue
        text = param.name
        if param.kind is param.VAR_POSITIONAL:
            text = "*" + text
            star_done = True
        elif param.kind is param.VAR_KEYWORD:
            text = "**" + text
        elif param.kind is param.KEYWORD_ONLY and not star_done:
            parts.append("*")
            star_done = True
        if param.annotation is not param.empty:
            text += f": {param.annotation}"
        if param.default is not param.empty:
            text += f" = {default_text(param.default)}"
        parts.append(text)
    ret = signature.return_annotation
    tail = f" -> {ret}" if returns and ret is not inspect.Signature.empty else ""
    return "(" + ", ".join(parts) + ")" + tail


def describe(name: str, obj: object) -> list[str]:
    if inspect.isclass(obj):
        if issubclass(obj, tuple) or obj.__module__ == "typing":
            return [f"{name}"]
        if issubclass(obj, Exception):
            return [f"class {name}({', '.join(b.__name__ for b in obj.__bases__)})"]
        protocol = getattr(obj, "_is_protocol", False)
        if dataclasses.is_dataclass(obj):
            flags = "frozen " if obj.__dataclass_params__.frozen else ""
            lines = [f"class {name}  # {flags}dataclass"]
            for f in dataclasses.fields(obj):
                default = ""
                if f.default is not dataclasses.MISSING:
                    default = f" = {f.default!r}"
                elif f.default_factory is not dataclasses.MISSING:  # type: ignore[misc]
                    default = " = <factory>"
                lines.append(f"    {f.name}: {f.type}{default}")
        elif protocol:
            lines = [f"class {name}  # Protocol"]
            lines += [f"    {attr}: {ann}" for attr, ann in getattr(obj, "__annotations__", {}).items()]
        else:
            lines = [f"class {name}{sig(obj, returns=False)}"]
        for member, value in vars(obj).items():
            if member.startswith("_") or member == "code":
                continue
            if isinstance(value, property):
                ret = inspect.signature(value.fget).return_annotation  # type: ignore[arg-type]
                lines.append(f"    .{member}  # property -> {ret}")
            elif isinstance(value, classmethod):
                lines.append(f"    @classmethod {member}{sig(value.__func__)}")
            elif inspect.isfunction(value):
                lines.append(f"    def {member}{sig(value)}")
        return lines
    if inspect.isfunction(obj):
        return [f"def {name}{sig(obj)}"]
    text = f"{type(obj).__name__}({sorted(obj)!r})" if isinstance(obj, (set, frozenset)) else repr(obj)  # sets: stable order
    if isinstance(obj, dict) and len(text) > 100:
        kinds = type(next(iter(obj.values()))).__name__
        return [f"{name}: dict[str, {kinds}]  # keys: {', '.join(map(str, obj))}"]
    return [f"{name} = {text if len(text) <= 100 else text[:97] + '...'}"]


def kit_api() -> str:
    out = ["```text"]
    extras = {"ailab.framework": ["LAB_START_TAG"], "ailab.gitutil": ["TAG_START", "TOOL_NOISE", "KIT_AUTHOR", "KIT_DATE"],
              "ailab.checks": ["CC_TYPES"], "ailab.runner": []}
    for module in (kit_framework, kit_gitutil, kit_checks, kit_runner):
        out.append(f"# {module.__name__}")
        for name in extras[module.__name__] + public_names(module):
            out += describe(name, getattr(module, name))
        out.append("")
    out.append("```")
    return "\n".join(out)


def signatures() -> str:
    out = ["```text"]
    for title, module, names in API:
        out.append(f"# {title}")
        for name in names:
            out += describe(name, getattr(module, name))
        out.append("")
    out.append("# remit.errors  (all derive from RemitError; each has a stable .code)")
    for name, cls in sorted(vars(errors).items()):
        if inspect.isclass(cls) and issubclass(cls, errors.RemitError) and cls is not errors.RemitError:
            bases = ", ".join(b.__name__ for b in cls.__bases__)
            out.append(f"{name}({bases})  code={cls.code!r}")
    out.append("```")
    return "\n".join(out)


def money_text(m: money.Money) -> str:
    return f"{m.amount:,.2f}"


def constants() -> str:
    L: list[str] = []
    L.append("**Currencies** (`money.CURRENCIES`, all with 2 decimals): " + ", ".join(money.CURRENCIES) + ".")
    L.append("")
    L.append("**Corridors** (`corridors.CORRIDORS`; amounts in QAR; both limits inclusive):")
    L.append("")
    L.append("| Code | min_send | max_send | delivery_methods (first = default) | fee_schedule |")
    L.append("|---|---:|---:|---|---|")
    for c in corridors.all_corridors():
        L.append(f"| {c.code} | {money_text(c.min_send)} | {money_text(c.max_send)} | {', '.join(c.delivery_methods)} | {c.fee_schedule} |")
    L.append("")
    L.append("**Fee schedules** (`fees.SCHEDULES`). Tier chosen by the whole amount, `upto` inclusive; "
             "`raw = amount x percent + flat`; `base = min(max(raw, minimum), cap)`; `total = base + express_surcharge` if express.")
    for s in fees.SCHEDULES.values():
        L.append("")
        L.append(f"`{s.id}`: minimum {s.minimum}, cap {s.cap}, express surcharge {s.express_surcharge} (QAR)")
        L.append("")
        L.append("| Tier | upto (QAR) | percent | flat (QAR) |")
        L.append("|---:|---:|---:|---:|")
        for i, t in enumerate(s.tiers):
            upto = "no limit" if t.upto is None else f"{t.upto:,}"
            L.append(f"| {i} | {upto} | {(t.percent * 100).normalize():f}% | {t.flat} |")
    L.append("")
    L.append("**Fee examples** (computed by `fees.quote_fee`, QAR):")
    L.append("")
    L.append("| Amount | QAR-INR | QAR-INR express | QAR-PKR | QAR-PKR express |")
    L.append("|---:|---:|---:|---:|---:|")
    inr, pkr = corridors.get_corridor("QAR", "INR"), corridors.get_corridor("QAR", "PKR")
    for amount in ["100.00", "150.25", "500.00", "500.01", "1000.00", "2000.00", "2000.01", "10000.00", "10000.01", "20000.00"]:
        a = money.Money(amount, "QAR")
        cells = []
        for corr in (inr, pkr):
            for express in (False, True):
                try:
                    cells.append(money_text(fees.quote_fee(a, corr, express=express)))
                except errors.RemitError:
                    cells.append("-")
        # PKR max_send is 15,000: show the fee anyway (quote_fee does not check corridor limits)
        L.append(f"| {amount} | " + " | ".join(cells) + " |")
    L.append("")
    L.append("(`quote_fee` does not check a corridor's `min_send`/`max_send`; `corridors.validate_send` and the service do.)")
    L.append("")
    L.append("**FX** (`fx.DEFAULT_MID_RATES`, `fx.CORRIDOR_MARGINS`; customer rate = mid x (1 - margin), 4 dp half up; "
             f"quote valid for {int(fx.QUOTE_TTL.total_seconds())} s, expired from `expires_at` onwards):")
    L.append("")
    L.append("| Corridor | mid rate | margin | customer rate | 500.00 QAR buys |")
    L.append("|---|---:|---:|---:|---:|")
    for code, mid in fx.DEFAULT_MID_RATES.items():
        margin = fx.CORRIDOR_MARGINS[code]
        rate = fx.customer_rate(mid, margin)
        buys = money.Money(Decimal("500") * rate, code.split("-")[1])
        L.append(f"| {code} | {mid} | {margin} | {rate} | {money_text(buys)} {buys.currency} |")
    L.append("")
    L.append("**Limits** (`limits.LIMITS`, QAR; allowed when `used + amount <= limit`; windows are Qatar calendar day/month, UTC+3):")
    L.append("")
    L.append("| KYC tier | daily | monthly |")
    L.append("|---|---:|---:|")
    for tier, lim in limits.LIMITS.items():
        L.append(f"| {tier} | {money_text(lim.daily)} | {money_text(lim.monthly)} |")
    L.append("")
    L.append("**Notifications** (`notify.TEMPLATES`): " + ", ".join(f"`{t}` ({'/'.join(sorted(v))})" for t, v in notify.TEMPLATES.items())
             + ". Failure reasons (`notify.FAILURE_REASONS`): " + ", ".join(f"`{k}`" for k in notify.FAILURE_REASONS) + ".")
    L.append("")
    L.append("**Ledger** postings per sent transfer: debit `CUSTOMER:<id>` for send + fee; credit `PAYOUT_CLEARING` for send; "
             f"credit `PARTNER_PAYABLE` for {ledger.PARTNER_SHARE} x fee (half-even, Q-LED-1); credit `FEE_INCOME` for the rest. "
             "Balance = credits minus debits.")
    L.append("")
    L.append("**Screening constants:** " + f"THRESHOLD={screening.THRESHOLD}, FUZZY_PERCENT={screening.FUZZY_PERCENT}, "
             f"MIN_FUZZY_LEN={screening.MIN_FUZZY_LEN}, MAX_TOKENS={screening.MAX_TOKENS}, particles dropped: "
             + ", ".join(sorted(screening.PARTICLES)) + ". Demo watchlist: "
             + "; ".join(f"`{n}`" for n in screening.DEFAULT_WATCHLIST) + ".")
    return "\n".join(L)


GENERATORS = {"signatures": signatures, "constants": constants, "kit_api": kit_api}
MARK = r"<!-- BEGIN GENERATED: {name} -->\n.*?<!-- END GENERATED: {name} -->"


def render_all() -> dict[str, str]:
    return {name: fn() for name, fn in GENERATORS.items()}


def apply(text: str, blocks: dict[str, str]) -> str:
    for name, body in blocks.items():
        pattern = re.compile(MARK.format(name=re.escape(name)), re.S)
        if not pattern.search(text):
            raise SystemExit(f"KIT_NOTES.md has no GENERATED block named {name!r}")
        block = f"<!-- BEGIN GENERATED: {name} -->\n{body}\n<!-- END GENERATED: {name} -->"
        text = pattern.sub(lambda m: block, text)
    return text


if __name__ == "__main__":
    blocks = render_all()
    if len(sys.argv) == 3 and sys.argv[1] == "--write":
        path = sys.argv[2]
        with open(path, encoding="utf-8") as handle:
            old = handle.read()
        new = apply(old, blocks)
        if new != old:
            with open(path, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(new)
            print(f"updated {path}")
        else:
            print(f"{path} is up to date")
    else:
        for name, body in blocks.items():
            print(f"<!-- BEGIN GENERATED: {name} -->\n{body}\n<!-- END GENERATED: {name} -->\n")
