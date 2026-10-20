# الوحدة 15 — التشغيل والتسليم (Operating and handing over)

*الوكيل الذي أُطلق (A shipped agent) لا يزال بحاجة إلى من يُبقيه سليمًا، ثم لا بد أن يصير ملكًا لشخص آخر. يتناول الدرس 15.1 المهمة الأولى: تتبّعات (traces) تُظهر ما فعله كل تشغيل دون الاحتفاظ بما قاله الموظفون، ولوحات متابعة وتنبيهات لأهداف مستوى الخدمة (dashboards and SLO alerts) لا تدرّب الناس على تجاهلها، وخمس فئات من الحوادث (five incident classes) لكل منها دليل تشغيل ومفتاح إيقاف (a runbook and a kill switch)، ومراجعات ما بعد الحادثة الخالية من اللوم (blameless postmortems)، وحلقة تغذية راجعة (a feedback loop) تحوّل الإخفاقات إلى حالات تقييم (turns failures into eval cases)، وإدارة التغيير للموجّهات والنماذج (change management for prompts and models). ويحوّل مختبره ملفات تتبّع JSONL (JSONL traces) إلى تقرير عن التكلفة والزمن والإخفاق (a cost, latency and failure report)، ويُجري تمرين حادثة (an incident drill) يوقف فيه مفتاح الإيقاف (the kill switch) وكيلًا وهميًا منفلتًا (a runaway mock agent). أما الدرس 15.2 فهو ورشة التسليم (the handover workshop): اختبار القبول مع العميل (acceptance testing with the customer)، ومجموعة الوثائق (the documentation set)، والتدريب (training)، ونموذج الدعم (the support model)، والتبنّي (adoption)، وتتبّع الفوائد مقابل خط الأساس الخيالي (benefits tracking against the fictional baseline)، والرعاية المكثفة (hypercare)، وإغلاق المشروع (closing the engagement). ويحوّل مختبره معايير القبول (acceptance criteria) إلى نص اختبار قبول المستخدم (a UAT script) يستطيع المشغِّل أن يتمرّن عليه، مع دليل المستخدم (a user guide) وفهرس لأدلة التشغيل (a runbook index) وقائمة فحص التسليم (a handover checklist) لنجم ديسك (Najm Desk).*

> **الطبقة (Layer):** Production, Delivery — إبقاء الوكيل سليمًا أثناء عمله (keeping an agent healthy while it runs)، وتسليمه إلى العميل ليتمكن من امتلاكه (handing it to the customer so that they can own it).

---

# 15.1 — تشغيل وكيل في الإنتاج: قابلية المراقبة والتنبيهات والحوادث وأدلة التشغيل وحلقة التحسين (Running an agent in production: observability, alerts, incidents, runbooks and the improvement loop)
*المستوى (Level): 🔴 متقدم (Advanced)* · *المتطلبات (Prerequisites): 8.2، 12.2، 13.1، 14.2* · *الطبقة (Layer): Production*

## ⚡ الدرس في دقيقة (In 60 seconds)
- الوكلاء (Agents) يفشلون بهدوء (fail softly): الخدمة تعمل والإجابات خاطئة. راقب **التشغيل (run)**.
- تتبَّع أربعة مستويات (Trace four levels)؛ وسجّل المعرّفات والأعداد والأسباب (log ids, counts and reasons)، لا النصوص أبدًا (never text).
- نبّه على أعراض أهداف مستوى الخدمة (service level objective, SLO) نادرًا؛ ولكل تنبيه دليل تشغيل (every alert has a runbook).
- خمس فئات من الحوادث (Five incident classes)، وخطوة أولى واحدة: **أوقفه (stop it)**، بمفتاح إيقاف جرى التدرّب عليه (a drilled kill switch).
- الإخفاقات تصير حالات تقييم (Failures become eval cases)؛ والتغييرات تمرّ هكذا: قيِّم، ثم أطلق كناريًا، ثم راقب، ثم تراجع (changes go evaluate, canary, monitor, roll back).

## 🧭 لماذا يهم (Why it matters)
مساء الخميس تطلق لجين موجّهًا (a prompt) يقصّر الإجابات — افتراضي (hypothetical). وصباح الأحد في 07:10، وهي الذروة (the peak)، تكون لوحة المتابعة (dashboard) لدى مها خضراء. وفي 09:20 تتصل يارا هاتفيًا: أعطى نجم ديسك (Najm Desk) أحد عشر شخصًا سياسة VPN دون مصدر (with no source)، وأُعطي اثنان منهم قاعدة كلمة المرور ذات الاثني عشر حرفًا الملغاة (the retired 12-character password rule). لم يُطلق شيء أي تنبيه (Nothing alerted)، لأن شيئًا لم يفشل (because nothing failed). ولا تحمل التتبّعات (traces) أي نسخة موجّه (prompt version)، ولا أحد متأكد ممن يحق له إيقاف المساعد (who may switch the assistant off).

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**الوكلاء يفشلون بهدوء (Agents fail softly).** تفشل خدمة الويب بصوت عالٍ (A web service fails loudly)؛ أما الوكيل فقد يجيب إجابة خاطئة بثقة (answer wrongly with confidence)، أو يدور في حلقة ويحرق الرموز (loop while burning tokens)، أو يطيع أمرًا محقونًا (obey an injected order)، كل ذلك دون أي خطأ (without an error). لذا راقب **التشغيل (run)**: رسالة واحدة تُعالَج حتى سبب التوقف (one message handled until a stop reason) (الدرس 8.2).

```mermaid
flowchart TD
    C["المحادثة: المعرّف والقناة واللغة<br/>(Conversation: id, channel, language)"] --> T["الدور أو التشغيل: الإصدار ونسخة الموجّه وسبب التوقف والثواني والرموز<br/>(Turn, or run: release, prompt version, stop reason, seconds, tokens)"]
    T --> M["استدعاء النموذج: الرموز والمللي ثانية ومعرّف الطلب<br/>(Model call: tokens, ms, request id)"]
    T --> L["استدعاء الأداة: الأداة وحجم النتيجة والخطأ والرفض<br/>(Tool call: tool, result size, error, refused)"]
```

**التسجيل الآمن للبيانات الشخصية (PII-safe logging)** (الاختصار PII يعني البيانات الشخصية، personal data). الضعيف (Weak): تسجيل كل موجّه وكل إجابة «لأغراض التنقيح» ("for debugging"). والقوي (Strong): سجّل المعرّفات والأحجام والأسباب (log ids, sizes and reasons)؛ وأخفِ أولًا (mask first) (الدرس 13.1)؛ واعتمد قائمة سماح للحقول المسجَّلة (allow-list logged fields)؛ واحتفظ بأي نص في مخزن منفصل قصير العمر (a separate, short-lived store) (تقرر سارة ذلك، الدرس 13.2). معرّفات المحادثات عشوائية (Conversation ids are random)، ولا تكون رقم موظف أبدًا (never an employee number)؛ ومعرّف المستخدم بعد تجزئته (a hashed user id) يظل في الغالب بيانات شخصية. يحتفظ `Trace` في المختبر 8.2 بنص مقتطع (clipped text): لا بأس بذلك في مختبر؛ أما في الإنتاج (in production) فسجّل الأحجام بدلًا منه.

**OpenTelemetry.** يستطيع Anthropic SDK إصدار امتدادات OpenTelemetry (spans)، امتداد واحد لكل استدعاء (one per call) (تجريبي وقت الكتابة، beta at the time of writing؛ ثبّت الإصدار، pin the version)، بسمات `gen_ai.*` من الاصطلاحات الدلالية لـGenAI التي لا تزال تتطور (the still-evolving GenAI semantic conventions). تحمل الامتدادات البيانات الوصفية فقط افتراضيًا (metadata only by default) (`metadata_only`)؛ ولا تفعّل `content` إلا بعد موافقة سارة. وأي `conversation_id` تضعه يُصدَّر في الوضعين (exported in both modes): فلا تضع فيه بيانات شخصية أبدًا (never put personal data in it). سجّل `resp._request_id` لكل استدعاء، من أجل تقارير الإخفاق (for failure reports).

### 🟡 التعمق أكثر (Going deeper)

**اقرأ التتبّعات (Read the traces).** شغّل الأمر من `aiapps/labkit`. العيّنة اصطناعية وخيالية (The sample is synthetic and fictional): 83 تشغيلًا، وخط الأساس (baseline) `r41` والكناري (canary) `r42-canary`. الأسعار قيم نائبة فقط (Prices are placeholders): استخدم صفحة الأسعار.

```bash
PRICE_IN_PER_MTOK=1 PRICE_OUT_PER_MTOK=5 python labs/m15/trace_report.py labkit/data/m15_traces.jsonl --by release
```

```text
== r42-canary: 26 runs ==
outcomes : done 17 (65%) | no_progress 3 (12%) | iteration_cap 3 (12%) | token_budget 2 (8%) | model_error 1 (4%)
latency  : run p50 3.0 s, p95 11.9 s | tokens per run p95 11,051
cost     : 0.13 in all, 0.0076 per resolved conversation
slo      : success 65.4% (want 90%+) BREACH | p95 11.9 s (want 10 s or less) BREACH
privacy  : card in start.goal x1, email in start.goal x1, secret in start.goal x1
```

(يُطبع `r41` أولًا.) اقرأ النتائج (outcomes) والأذيال (tails) (p95) والمال لكل محادثة **محلولة (resolved)**، لأن التشغيلات الفاشلة تكلّف أيضًا (failed runs cost too). يجتاز خط الأساس هدفَي مستوى الخدمة (SLOs) كليهما؛ ويفشل الكناري في كليهما ويكلّف أكثر من الضعف لكل محادثة محلولة (over twice as much per resolved conversation): تراجع عنه. وسطر الخصوصية (privacy line) نتيجة ثانية: مسجِّل قديم احتفظ بنص خام (an old logger kept raw text). ويجعل رمز الخروج (exit code) هذا مهمة مجدولة (a cron job)، وهي أرخص تنبيه (the cheapest alert). يعدّ التقرير `done`، فكان سيفوّت حادثة الأحد (would have missed the Sunday incident): أضف علمًا (a flag) باسم `cited` إلى `stop`. ولا يشمل `input_tokens` الرموز المخزّنة مؤقتًا (excludes cached tokens): فإن خزّنت الموجّهات مؤقتًا (if you cache prompts)، فسجّل أيضًا `cache_creation_input_tokens` و`cache_read_input_tokens` (الدرس 14.2)، وإلا قلَّ احتساب التكلفة والقاطع عن حقيقته (cost and the breaker undercount).

```python
# labs/m15/trace_report.py
"""Lab 15.1: one page for the on-call person, from JSONL traces (Lab 8.2's format, plus release and prompt_version).
  python labs/m15/trace_report.py TRACE.jsonl [--by release]    exit 1 on an SLO breach, personal data or a broken log
Set PRICE_IN_PER_MTOK and PRICE_OUT_PER_MTOK (per million tokens) from the price page: prices never live in code."""
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

SLO = {"success": 0.90, "p95_seconds": 10.0}      # decisions, not facts: take yours from NFR-01 and your own data
PII = {"email": r"[\w.+-]+@[\w-]+\.[\w.]+", "card": r"\b(?:\d[ -]?){13,16}\b", "secret": r"(?i)\b(?:password|passcode)\s*(?:is|=|:)\s*\S+"}
PRICE = [float(os.environ.get(k, "nan")) for k in ("PRICE_IN_PER_MTOK", "PRICE_OUT_PER_MTOK")]


def pct(xs, p):
    """Nearest-rank percentile: averages hide the tail, where users wait."""
    xs = sorted(xs)
    return xs[max(0, math.ceil(p / 100 * len(xs)) - 1)] if xs else float("nan")


def report(label, runs):
    """Print one group of runs; return True when it breaches an SLO."""
    stops = [next((e for e in ev if e["event"] == "stop"), {}) for ev in runs]       # no stop event: the process died or was killed
    reasons, secs = Counter(s.get("reason", "no_stop_line") for s in stops), [s["seconds"] for s in stops if "seconds" in s]
    usage = [[sum(e.get(k, 0) for e in ev if e["event"] == "model") for k in ("input_tokens", "output_tokens")] for ev in runs]
    n, done, money = len(runs), reasons["done"], sum(a * PRICE[0] + b * PRICE[1] for a, b in usage) / 1e6
    print(f"== {label}: {n} runs ==\noutcomes : " + " | ".join(f"{k} {v} ({v / n:.0%})" for k, v in reasons.most_common()))
    print(f"latency  : run p50 {pct(secs, 50):.1f} s, p95 {pct(secs, 95):.1f} s | tokens per run p95 {pct([a + b for a, b in usage], 95):,.0f}")
    if not math.isnan(money):                      # failed runs cost too: divide by RESOLVED conversations
        print(f"cost     : {money:.2f} in all, {money / max(done, 1):.4f} per resolved conversation")
    ok = {f"success {done / n:.1%} (want {SLO['success']:.0%}+)": done / n >= SLO["success"],
          f"p95 {pct(secs, 95):.1f} s (want {SLO['p95_seconds']:g} s or less)": pct(secs, 95) <= SLO["p95_seconds"]}
    print("slo      : " + " | ".join(f"{k} {'ok' if v else 'BREACH'}" for k, v in ok.items()))
    return not all(ok.values())


if __name__ == "__main__":
    runs, bad, leaks = defaultdict(list), 0, Counter()
    for line in open(sys.argv[1], encoding="utf-8"):
        try:
            e = json.loads(line)
            run, kind = e["run"], e["event"]
        except (ValueError, KeyError, TypeError):
            bad += bool(line.strip())                  # a pipeline that drops lines is a finding too
            continue
        runs[run].append(e)
        for field, v in e.items():                     # kinds and places are safe to print; the values are not
            leaks.update((what, f"{kind}.{field}") for what, rx in PII.items() if isinstance(v, str) and re.search(rx, v))
    by, groups = (sys.argv[sys.argv.index("--by") + 1] if "--by" in sys.argv else None), defaultdict(list)
    for ev in runs.values():
        groups[next((e for e in ev if e["event"] == "start"), {}).get(by, "(none)") if by else "all"].append(ev)
    print(f"{len(runs)} runs, {bad} unreadable lines")
    breached = [report(label, g) for label, g in sorted(groups.items())]
    print("privacy  : " + (", ".join(f"{k} in {w} x{n}" for (k, w), n in sorted(leaks.items())) or "no personal-data patterns found"))
    sys.exit(1 if any(breached) or leaks or bad or not runs else 0)        # no traces at all is an incident too
```

**لوحات المتابعة وأهداف مستوى الخدمة والتنبيهات (Dashboards, SLOs and alerts).** أربع لوحات: النتائج حسب سبب التوقف (outcomes by stop reason)، ومؤشرات الجودة البديلة (quality proxies) (الاستشهادات والتسليمات إلى البشر والتقييمات، citations, hand-offs, ratings)، والزمن والتكلفة (latency and cost)، وأخطاء الحواجز والأدوات (guard and tool errors). تأتي الأهداف من المتطلبات (requirements): النجاح (success) (`done` مؤشر بديل، is a proxy)، وp95 (NFR-01)، والتوافر (availability) (NFR-02)، والتكلفة لكل محادثة محلولة (cost per resolved conversation) (NFR-06). في الشهر نحو 217 ساعة مكتب (desk hours)، فنسبة 99.5% لا تُبقي إلا نحو ساعة واحدة (leaves about one)؛ وعند **معدل احتراق (burn rate)** (الجزء السيئ المرصود مقسومًا على المسموح به، bad fraction seen over allowed) قدره 10 تنفد هذه الساعة في نحو يومَي مكتب (about two desk days). استدعِ المناوب حين تحترق نافذة قصيرة وأخرى طويلة بسرعة (Page when a short and a long window burn fast) ([*السحابة وDevOps (Cloud & DevOps)*، الدرس 5.2 — أهداف مستوى الخدمة وميزانيات الأخطاء والتنبيه (SLOs, error budgets and alerting)](../cloud/index.ar.html#/5.2)). لمواجهة إرهاق التنبيهات (Against fatigue): استدعِ المناوب عند الأعراض (page on symptoms)، وأعطِ كل تنبيه دليل تشغيل (give each alert a runbook)، واحذف التنبيهات المتجاهَلة (delete ignored alerts).

| فئة الحادثة (Incident class) | كيف تبدو (It looks like) | ثم (Then) |
|---|---|---|
| عاصفة الإجابات الخاطئة (Wrong-answer storm) | تنخفض التقييمات (ratings) وتختفي الاستشهادات (citations) | `--by release`؛ تراجع (roll back) |
| انقطاع أداة (Tool outage) | أخطاء الأدوات (tool errors)؛ ويعتذر الوكيل (the agent apologises) | أوقف `write_tools`؛ واسأل المالك (ask the owner) |
| قفزة التكلفة (Cost spike) | تقفز الرموز (Tokens jump)؛ ويرتفع `iteration_cap` | هل تحرّك القاطع؟ ⁦(Did the breaker act?)⁩ |
| حادثة حقن (Injection incident) | يتفعّل الحارس (Guard fires)؛ واستدعاء أداة غريب (an odd tool call) | أوقف `write_tools`؛ واتصل بنورة، وبسارة إن خرجت بيانات (call Noura, and Sara if data left) |
| انحدار بعد تغيير (Regression after a change) | الكناري أسوأ (The canary is worse) | الإصدار السابق (Previous release) |

لكل فئة دليل تشغيل (runbook) (`labs/m15/runbooks/`)؛ وكلها تبدأ بـ**الإيقاف (stopping)**. مفتاح الإيقاف (The kill switch) ملف خارج النموذج (a file outside the model) يُقرأ عند كل خطوة من الحلقة (read on every loop step)، وفيه علمان (two flags) (الدرس 7.1): إيقاف `model_calls` يعطي الوضع المتدهور (degraded mode)، وإيقاف `write_tools` يعطي وضع القراءة فقط (read-only). وهو **يفشل مغلقًا (fails closed)** (الملف غير المقروء يعني الإيقاف، an unreadable file means off)؛ ويستطيع أي عضو في جدول مناوبة تقنية المعلومات (IT on-call rota) الضغط عليه، ولا يستأنف العمل إلا المستوى L2 أو L3 (only L2 or L3 resumes)، وهو **يُتدرَّب عليه (drilled)**. يكفي ملف مشترك على مضيف واحد (One host can share a file)؛ أما النسخ المتعددة (several instances) فتحتاج إلى إعداد مشترك (shared configuration).

**تمرين الحادثة (The drill).** يؤدي `[mock:loop]` دور وكيل يكرر أداة واحدة إلى ما لا نهاية (plays an agent that repeats one tool for ever)، مع رفع حدّ التكرارات (the cap) إلى 500 ليكون المفتاح وحده القادر على إيقافه (so only the switch can stop it). المشهد الأول (Act one): يقلبه شخص بعد الاستدعاء الخامس (a person flips it after call five). المشهد الثاني (Act two): يجب أن يوقفه قاطع التكلفة (the cost breaker)، عند 12,000 رمز في الساعة (at 12,000 tokens an hour). هذا رقم للتمرين (A drill number): فأكثر ساعات العيّنة العادية ازدحامًا (the sample's busiest normal hour) أعلى منه بكثير (far higher).

```python
# labs/m15/kill_switch.py
"""Lab 15.1: a kill switch, a cost breaker that pulls it, and a drill that proves both.
  python labs/m15/kill_switch.py drill [DIR]
  python labs/m15/kill_switch.py flip FILE FLAG on|off WHO WHY   FLAG: model_calls, write_tools or all"""
import json
import os
import sys
import time
from pathlib import Path

import anthropic

sys.path.append(str(Path(__file__).resolve().parents[1] / "m08"))
from agent_loop import Trace          # noqa: E402  Lab 8.2's JSONL writer

MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")
FLAGS = ("model_calls", "write_tools")        # lesson 7.1: model_calls off = degraded mode; write_tools off = read-only


class Switch:
    """Two flags in one file: any process can flip it, every loop step reads it."""

    def __init__(self, path):
        self.path = Path(path)

    def allowed(self, flag):
        try:                                  # fail closed: a missing or torn file means "off", never "on"
            return json.loads(self.path.read_text(encoding="utf-8"))["flags"][flag] == "on"
        except (OSError, ValueError, KeyError, TypeError):
            return False

    def set(self, value, who, why, flags=FLAGS):
        if value not in ("on", "off") or not set(flags) <= set(FLAGS):       # a mistyped press must fail loudly
            raise ValueError(f"values are on or off, flags are {FLAGS}")
        state = {f: "on" if self.allowed(f) else "off" for f in FLAGS} | {f: value for f in flags}
        tmp = self.path.with_name(self.path.name + ".tmp")
        tmp.write_text(json.dumps({"flags": state, "by": who, "why": why}), encoding="utf-8")
        os.replace(tmp, self.path)            # atomic: readers never see half a file
        with open(self.path.with_name(self.path.name + ".log"), "a", encoding="utf-8") as f:        # who pressed it, and why
            f.write(json.dumps({"ts": round(time.time()), "flags": flags, "value": value, "by": who, "why": why}) + "\n")


class Breaker:
    """Pulls the switch itself when more than `limit` tokens are spent inside `window_s` seconds."""

    def __init__(self, switch, limit, window_s=3600):
        self.switch, self.limit, self.window_s, self.spent = switch, limit, window_s, []

    def add(self, tokens):
        now = time.time()
        self.spent = [(t, n) for t, n in self.spent + [(now, tokens)] if t > now - self.window_s]
        total = sum(n for _, n in self.spent)
        if total > self.limit and self.switch.allowed("model_calls"):
            self.switch.set("off", "cost-breaker", f"{total} tokens in {self.window_s} s, limit {self.limit}", ("model_calls",))


TOOLS = [{"name": "get_ticket_history", "description": "Show the full history of one IT ticket by number.",
          "input_schema": {"type": "object", "properties": {"ticket_id": {"type": "string"}}, "required": ["ticket_id"]}}]


def history(ticket_id):
    return "\n".join(f"day {d}: customer called about ticket {ticket_id}, follow-up noted" for d in range(1, 31))        # a long result


def run_agent(goal, switch, breaker, trace, watch=None, max_steps=500):
    """A bare loop. 500 steps is the cap someone raised mid-incident, so only the switch is left."""
    client, t0, spent, messages = anthropic.Anthropic(timeout=30.0, max_retries=0), time.monotonic(), 0, [{"role": "user", "content": goal}]
    trace.log("start", model=MODEL, goal_chars=len(goal), release="drill")

    def stop(reason, step):
        trace.log("stop", step=step, reason=reason, tokens=spent, seconds=round(time.monotonic() - t0, 1))
        return reason

    for step in range(1, max_steps + 1):
        if not switch.allowed("model_calls"):                    # read BEFORE every model call: the next call never starts
            return stop("killed", step - 1)
        resp = client.messages.create(model=MODEL, max_tokens=1024, output_config={"effort": "low"}, tools=TOOLS, messages=messages)
        used = resp.usage.input_tokens + resp.usage.output_tokens
        spent += used
        trace.log("model", step=step, stop_reason=resp.stop_reason, input_tokens=resp.usage.input_tokens, output_tokens=resp.usage.output_tokens)
        breaker.add(used)
        if watch:
            watch(step)
        if resp.stop_reason != "tool_use":
            return stop("done" if resp.stop_reason == "end_turn" else resp.stop_reason, step)
        messages.append({"role": "assistant", "content": resp.content})
        results = []
        for b in (b for b in resp.content if b.type == "tool_use"):
            out = history(**b.input)
            trace.log("tool", step=step, tool=b.name, result_chars=len(out))
            results.append({"type": "tool_result", "tool_use_id": b.id, "content": out})
        messages.append({"role": "user", "content": results})
    return stop("iteration_cap", max_steps)


def drill(kind, folder):
    """'operator': a person flips the switch after the 5th model call. 'breaker': nobody does, so the cost breaker must."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    switch, trace, again = Switch(folder / f"{kind}.switch.json"), Trace(folder / f"{kind}.jsonl"), Trace(folder / f"{kind}-again.jsonl")
    switch.set("on", "drill", "start")
    person = lambda step: step == 5 and switch.set("off", "maha", "loop in the drill", ("model_calls",))
    reason = run_agent("Show the full history of ticket 4471 [mock:loop]", switch, Breaker(switch, 12_000 if kind == "breaker" else 10**9),
                       trace, person if kind == "operator" else None)
    after = run_agent("Is ticket 4472 done yet?", switch, Breaker(switch, 10**9), again)        # a NEW conversation, switch still off
    calls = lambda t: sum(e["event"] == "model" for e in t.events)
    return {"reason": reason, "model_calls": calls(trace), "tokens": trace.events[-1]["tokens"], "new_request": after, "new_request_calls": calls(again)}


if __name__ == "__main__":
    if sys.argv[1:2] == ["flip"]:
        Switch(sys.argv[2]).set(sys.argv[4], sys.argv[5], " ".join(sys.argv[6:]) or "no reason given", FLAGS if sys.argv[3] == "all" else (sys.argv[3],))
    else:
        for kind in ("operator", "breaker"):
            print(kind, drill(kind, sys.argv[2] if len(sys.argv) > 2 else "drill_out"))
```

```bash
python labs/m15/kill_switch.py drill        # needs the offline mock (lesson 0.2)
```

```text
operator {'reason': 'killed', 'model_calls': 5, 'tokens': 4950, 'new_request': 'killed', 'new_request_calls': 0}
breaker {'reason': 'killed', 'model_calls': 8, 'tokens': 13392, 'new_request': 'killed', 'new_request_calls': 0}
```

لم يبدأ أي استدعاء بعد القلب (No call started after the flip)؛ وانتهت الحلقة (the loop ended) عند الاستدعاء الخامس لا 500. تجاوز القاطع (The breaker overshot) الحد بأقل من استدعاء واحد (by under one call) (يُضاف الإنفاق بعد الاستدعاء، spend is added after a call): فاضبط الحدود دون عتبة الألم (set limits below the pain point). ولم تُجرِ المحادثة الجديدة (A new conversation) أي استدعاء للنموذج (made no model call). *يعمل دون اتصال (Works offline):* المفتاح والقاطع والتمرين والتقرير (the switch, breaker, drill and report). *يحتاج إلى واجهة البرمجة الحقيقية (Needs the real API):* هل يدور نموذج حقيقي في حلقة مثل `[mock:loop]` (whether a real model loops)، وأعداد الرموز الحقيقية (real token counts) (تقدّرها النسخة المحاكاة، the mock estimates them)، وساعة ذروتك أنت (your own peak hour). لا يملك وكيل المختبر عمليات كتابة (The lab agent has no writes): فاربط `write_tools` ببوابة أدواتك (tool gate).

### 🔴 نظرة الخبير (Expert view)

**مراجعات ما بعد الحادثة الخالية من اللوم (Blameless postmortems).** سمِّ قائدًا ومشغِّلًا وكاتبًا (Name a lead, an operator and a scribe). في غضون خمسة أيام عمل (Within five working days) من كل استخدام للمفتاح (of every use of the switch)، اكتب الأثر والجدول الزمني والاكتشاف والعوامل المساهمة والإجراءات مع مالك وتاريخ (impact, timeline, detection, contributing factors, actions with owner and date). الضعيف (Weak): «دفع لجين موجّهًا سيئًا» ⁦("Lujain pushed a bad prompt.")⁩. والقوي (Strong): «وصل موجّه إلى كل الحركة دون كناري ودون نسخة في التتبّع، فاستغرق الاكتشاف ساعتين» ⁦("A prompt reached all traffic with no canary and no trace version, so detection took two hours.")⁩. غياب اللوم لا يعني غياب المالك (Blameless is not ownerless) ([*السحابة وDevOps (Cloud & DevOps)*، الدرس 5.3 — الحوادث ومراجعات ما بعد الحادثة الخالية من اللوم (Incidents and blameless postmortems)](../cloud/index.ar.html#/5.3)).

**حلقة التغذية الراجعة (The feedback loop).** المصادر: التقييمات مع سبب (ratings with a reason)، والتسليمات إلى البشر (hand-offs)، وإعادة كتابة المسودات (draft rewrites)، والتواصل المتكرر خلال ثلاثة أيام عمل (repeat contacts within three working days)، والتشغيلات التي لا تنتهي بـ`done` (runs not ending done). وفي الفرز الأسبوعي (A weekly triage) الذي تجريه يارا ولجين تُوسَم الأسباب وتُحوَّل أسوأ الحالات إلى **حالات تقييم (eval cases)**: تُزال البيانات الشخصية (personal data removed)، ويُحدَّد سلوك متوقع واحد (one expected behaviour)، ومعرّف متطلب (a requirement id). راجع أولًا (Review first)؛ فالمكررات تخفي الانحدارات (duplicates hide regressions) ([*اختبار البرمجيات (Software Testing)*، الدرس 7.3 — السلامة والمتانة والعدالة والمراقبة (Safety, robustness, fairness and monitoring)](../testing/index.ar.html#/7.3)).

**إدارة التغيير (Change management).** الموجّه والأداة ومحتوى الاسترجاع وقاعدة الحاجز الوقائي ومعرّف النموذج والحدود كلها تغييرات (Prompt, tool, retrieval content, guardrail rule, model id and limits are all changes). سمِّ النسخة التي ستتراجع إليها (Name the version to roll back to)؛ وقيِّم بالبوابة (evaluate with the gate) (الدرس 12.2) ومجموعة الفريق الأحمر (red-team set) (الدرس 13.1)، مقارنًا التكلفة والزمن (comparing cost and latency)؛ ووافق وفق سياسة التغيير (approve per the change policy) (الدرس 13.2)؛ وأطلق كناريًا مع موظفي المكتب (canary with desk agents) مقابل عتبات مسبقة (against preset thresholds) (`--by release`)؛ ثم رقِّ النسخة أو تراجع (then promote, or roll back): موجّه أو معرّف نموذج بإعادة توجيه الإعداد (a prompt or model id by repointing configuration)، وصورة حاوية بإعادة نشر البصمة السابقة (an image by redeploying the previous digest) (الدرس 14.1). ثبّت معرّف النموذج وسجّله (Pin and record the model id)؛ وسمِّ من يراقب إشعارات الإيقاف التدريجي (name who watches deprecation notices).

**متى لا تفعل ذلك (When not to).** التجربة التشغيلية بأربعة عشر موظفًا في المكتب (A pilot with fourteen desk staff) لا تحتاج إلى منصة تتبّع (needs no tracing platform)؛ يكفي ملف JSONL والتقرير (the JSONL file and report suffice).

## 🧰 الأدوات (The toolkit)
| الأداة أو الممارسة أو النمط (Tool, practice or pattern) | ما هي وماذا تفعل (What it is and does) | متى تلجأ إليها (When to reach for it) |
|---|---|---|
| **Trace schema** — مخطط التتبّع | أربعة مستويات من المعرّفات والأعداد والأسباب؛ دون نص (Four levels of ids, counts, reasons; no text) | قبل أول مستخدم (Before the first user) |
| **SLO burn-rate alert** — تنبيه معدل احتراق هدف مستوى الخدمة | أطلق النداء حين تحترق نافذة قصيرة وأخرى طويلة بسرعة (Page when short and long windows burn fast) | أي هدف يواجه المستخدمين (Any user-facing target) |
| **Kill switch** — مفتاح الإيقاف | أعلام خارج النموذج توقف الاستدعاءات أو الكتابات؛ ويفشل مغلقًا (Out-of-model flags that stop calls or writes; fails closed) | كل وكيل يتصرف أو ينفق (Every agent that acts or spends) |
| **Runbook** — دليل التشغيل | صفحة واحدة: المحفّز والدقائق الأولى والإصلاح والإبلاغ والاستئناف (One page: trigger, first minutes, fix, tell, resume) | كل تنبيه وكل تغيير روتيني (Every alert and routine change) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
المُخرَج (The artefact) هو **مجموعة أدلة التشغيل لنجم ديسك الإصدار 1 (Najm Desk v1 Runbook Set)** (تملكها مها، Maha owns it): `docs/runbooks/`، من `labs/m15/runbooks/`: قالب، وبطاقة مفتاح الإيقاف، وخمسة أدلة تشغيل للحوادث، وروتينان (a template, the kill-switch card, five incident runbooks, two routines).

**المُسلَّم الأسبوعي (Weekly deliverable).** أودِع (Commit) المجلد `week-15/`: `labs/m15/` مع اختبارات ناجحة (passing tests)، والتقرير على تتبّعاتك أنت (the report on your own traces)، ومخرجات التمرين (the drill output)، و`docs/runbooks/` لوكيلك أنت، ومراجعة واحدة بعد الحادثة (one postmortem)، و`NOTES.md`.

**جلسة المجموعة (Group session)، 60 دقيقة (60 minutes).** تمرين إخلاء (A fire drill): ازرعوا حادثة في ملف تتبّع وسمّوا فئتها من التقرير (plant an incident in a trace file and name its class from the report) (15)؛ واتبعوا دليل التشغيل واضغطوا المفتاح واكتبوا الملاحظة الأولى (follow the runbook, press the switch, write the first note) (25)؛ ويسمّي كلٌّ منكم سطرًا واحدًا غير واضح (each names one unclear line) (20).

**ابنِه مع Claude Code (Build it with Claude Code).** أعطِه هذه المواصفة (spec) في وضع التخطيط (plan mode) (تحقق من توثيق Claude Code الحالي، check the current Claude Code documentation):

```text
Goal: labs/m15/trace_report.py and kill_switch.py as in lesson 15.1, with tests in labkit/tests/test_m15_operating.py.
Context: Python 3.11, anthropic>=1,<2, the offline mock in aiapps/labkit, Lab 8.2's Trace in labs/m08/agent_loop.py.
Constraints: no prices in code; no prompt or answer text in traces; the switch fails closed and is written atomically;
no sampling parameters or prefill; no new dependencies; touch no other files.
Acceptance: pytest passes offline; the drill ends "killed" within one call of the flip and a new request makes no model call;
the report exits 1 on the sample traces and shows the canary breach.
Do not weaken a test. Run the tests after each step.
```

**تحقق قبل أن تقبله (Verify before you accept it).**
- اكسره (Break it): اجعل `allowed` تُرجع True عند الخطأ (return True on error)، وعطّل القاطع (disable the breaker)، وأزِح فهرس النسبة المئوية (shift the percentile index). يجب أن تُفشل كل واحدة منها اختبارًا.
- اقرأ الفرق (Read the diff) بحثًا عن الأسعار و`temperature` ونص الموجّه في التتبّعات (prices and prompt text in traces).

## 🛠️ التمارين (Exercises)
- 🟢 **اقرأ الكناري (Read the canary).** دون اتصال (Offline). شغّل التقرير مع `--by release`. *يكتمل عندما (Done when):* يسمّي `NOTES.md` الإصدار الذي يُتراجَع عنه (the release to roll back)، والدليل (the proof)، والحقول المسرِّبة (the leaking fields).
- 🟡 **اضبط القاطع من البيانات (Set the breaker from data).** دون اتصال (Offline). اجعل الحد ثلاثة أمثال أكثر ساعات `r41` ازدحامًا (three times the busiest hour). *يكتمل عندما (Done when):* يُظهر اختبار أن `r41` لا يُفعِّل القاطع أبدًا (a test shows r41 never trips it)، وأن تمرين الحلقة (the loop drill) لا يزال يُفعِّله، ويشرح `NOTES.md` السبب.
- 🔴 **شغّل وكيلك أنت (Operate your own agent).** *يحتاج إلى واجهة البرمجة الحقيقية (Needs the real API)* وسقف الإنفاق (the cap) من الدرس 0.2. شغّل وكيل المختبر 8.2 على 20 سؤالًا مع `TRACE_FILE`، وأصدر التقرير بأسعار حقيقية (report with real prices)، واكسره مرة واحدة (break it once) (`MAX_STEPS=1`)، واكتب مراجعة ما بعد الحادثة (the postmortem). *يكتمل عندما (Done when):* يحوي `NOTES.md` التقرير وتاريخ الأسعار (price date) وثلاثة إجراءات لها مالكون (three owned actions).

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **تسجيل النص «مؤقتًا فقط» (Logging text "just for now").** يصير هو التسرّب (It becomes the leak).
- **مفتاح يحتاج إلى النموذج أو إلى نشر (A switch that needs the model or a deploy).** يفشل حين يلزم (It fails when needed). استخدم ملفًا.
- **لا نسخة في التتبّع (No version in the trace).** لا تستطيع معرفة ما تغيّر (You cannot find what changed). سجّل الإصدار والموجّه والنموذج (Record release, prompt and model).
- **قراءة `done` على أنها صحيحة (Reading done as correct).** هي لا تعني إلا أن الحلقة انتهت (It only means the loop ended). أضف التقييمات (Add evals).

## 🧾 الخلاصة (Recap)
- راقب التشغيلات (Observe runs): النتائج والأذيال والمال لكل محادثة محلولة (outcomes, tails, money per resolved conversation).
- سجّل المعرّفات والأسباب (Log ids and reasons)، لا النصوص أبدًا (never text).
- نبّه على أعراض أهداف مستوى الخدمة (Alert on SLO symptoms)؛ وأوقف أولًا بمفتاح إيقاف جرى التدرّب عليه (stop first with a drilled kill switch).
- الإخفاقات تصير حالات تقييم (Failures become eval cases)؛ والتغييرات تُطلق كناريًا وقابلة للتراجع (changes are canaried and reversible).

## ✍️ اختبر نفسك (Check yourself)

**1. تُظهر لوحة المتابعة عدم وجود أخطاء، ومع ذلك يبلّغ الموظفون عن إجابات بلا مصدر (The dashboard shows no errors, yet staff report answers with no source). ما الناقص؟ ⁦(What is missing?)⁩**

- A. نافذة سياق أكبر للإجابات الطويلة (A larger context window for long answers)
- B. هدف زمن أكثر تساهلًا لساعات الذروة (A looser latency target for peak hours)
- C. إشارة جودة مثل معدل الاستشهاد (A quality signal such as citation rate)
- D. تنبيه أكثر حساسية على معدل الأخطاء (A more sensitive alert on the error rate)

<details><summary>الإجابة</summary>

**C.** الإخفاق هادئ؛ ولا تُظهره إلا إشارات الجودة (The failure is soft; only quality signals show it) (الاستشهادات والتقييمات وأسئلة الكناري، citations, ratings, canary questions). (🟢 الإخفاق الهادئ، ⁦Soft failure.⁩)

</details>

**2. تعذّرت قراءة ملف المفتاح أثناء حادثة (The switch file cannot be read during an incident). ماذا ينبغي أن يفعل الوكيل؟ ⁦(What should the agent do?)⁩**

- A. يعدّه مُوقَفًا ويكفّ عن استدعاء النموذج (Treat it as off and stop calling the model)
- B. يواصل العمل على آخر إعداد معروف (Keep running on its last known setting)
- C. يعدّه مفعّلًا لتستمر الخدمة (Treat it as on so that service continues)
- D. يعيد محاولة القراءة مع مواصلة استدعاء النموذج (Retry the read while still calling the model)

<details><summary>الإجابة</summary>

**A.** هو يفشل مغلقًا (It fails closed): فإن لم يثبت شيء أنه يجوز له العمل (if nothing proves it may run)، فلا يعمل. (🟡 مفتاح الإيقاف، ⁦Kill switch.⁩)

</details>

**3. يُظهر الكناري نسبة 65% بحالة done وp95 عند 11.9 ثانية؛ وخط الأساس 93% و5.3 ثانية (The canary shows 65% done and p95 11.9 s; the baseline 93% and 5.3 s). ما الخطوة الأولى؟ ⁦(What first?)⁩**

- A. الانتظار أسبوعًا لمزيد من البيانات (Wait a week for more data)
- B. رفع هدف p95 إلى 12 ثانية (Raise the p95 target to 12 s)
- C. إضافة إعادة محاولات إلى استدعاءات أدوات الكناري (Add retries to the canary's tool calls)
- D. إعادة توجيه الإعداد إلى الإصدار القديم (Point configuration back at the old release)

<details><summary>الإجابة</summary>

**D.** العتبات المسبقة متجاوَزة (The preset thresholds are breached): فتراجع أولًا دون نشر (roll back first, with no deploy)؛ ثم حقّق بعد ذلك (investigate afterwards). (🔴 إدارة التغيير، ⁦Change management.⁩)

</details>

**4. يستدعي تنبيه المعالج الشخص المناوب ثلاثين مرة في الشهر ولا يتحرك أحد (A CPU alert pages the on-call person thirty times a month and nobody acts). ما أفضل إصلاح؟ ⁦(What is the best fix?)⁩**

- A. استدعاء شخص ثانٍ أيضًا (Page a second person as well)
- B. إلغاء هذا الاستدعاء والتنبيه على الأعراض بدلًا منه (Retire the page and alert on symptoms instead)
- C. رفع عتبته كل شهر حتى يتوقف (Raise its threshold each month until it stops)
- D. كتم القناة وقراءتها أيام الاثنين (Mute the channel and read it on Mondays)

<details><summary>الإجابة</summary>

**B.** التنبيه المتجاهَل يعلّم الناس تجاهل التالي (An ignored alert teaches people to ignore the next). استدعِ المناوب عند أعراض أهداف مستوى الخدمة (Page on SLO symptoms). (🟡 أهداف مستوى الخدمة والتنبيهات، ⁦SLOs and alerts.⁩)

</details>

**5. يريد الدعم أرقام الموظفين معرّفات للمحادثات، للبحث في محادثات شخص ما (Support wants employee numbers as conversation ids, to search a person's chats). لماذا لا؟ ⁦(Why not?)⁩**

- A. الأرقام تُفهرَس ببطء في معظم مخازن التتبّع (Numbers index slowly in most trace stores)
- B. المعرّف ينشر البيانات الشخصية إلى كل امتداد (The id spreads personal data to every span)
- C. أرقام الموظفين أقصر من أن تبقى فريدة (Employee numbers are too short to stay unique)
- D. الدعم يبحث بالفعل برقم التذكرة (Support already searches by ticket number)

<details><summary>الإجابة</summary>

**B.** تُصدَّر معرّفات المحادثات حتى حين لا يُصدَّر أي نص (Conversation ids are exported even when no text is). استخدم معرّفات عشوائية (Use random ids). (🟢 التسجيل الآمن للبيانات الشخصية، ⁦PII-safe logging.⁩)

</details>

## 📚 المراجع (References)
- وثائق Claude API، OpenTelemetry: https://platform.claude.com/docs/en/manage-claude/opentelemetry؛ OpenTelemetry: https://opentelemetry.io/docs/؛ Google SRE: https://sre.google/
- [*السحابة وDevOps (Cloud & DevOps)*، الدرس 5.1 — القياس عن بُعد: السجلات والمقاييس والتتبّعات وOpenTelemetry (Telemetry: logs, metrics, traces and OpenTelemetry)](../cloud/index.ar.html#/5.1)؛ [*تشغيل وكلاء الذكاء الاصطناعي في الإنتاج (Running AI Agents in Production)*، المستويات L0–L5 (levels L0–L5)](../agentic/learning-path.ar.html#level-3-production-engineer)
- **اقرأ هذا الأسبوع (Read this week)، الوحدة 15.** لا تعطيها الخطة فصولًا (The plan gives it no chapters)؛ وأقرب ما وُجد، كما ورد (the nearest, as given): Gulli، *Agentic Design Patterns*، الفصل 19 (Evaluation & Monitoring)، المسودة المجانية (the free draft) في الدرس 0.1؛ ومستودع *aie-book* لـChip Huyen (قائمة فحص الإنتاج، production checklist): https://github.com/chiphuyen/aie-book

---

# 15.2 — التسليم والتبنّي: التدريب ونموذج الدعم والقبول وإدارة التغيير وتتبّع الفوائد (Handover and adoption: training, support model, acceptance, change management and benefits tracking)
*المستوى (Level): 🔴 متقدم (Advanced)* · *المتطلبات (Prerequisites): 6.2، 7.2، 13.2، 15.1* · *الطبقة (Layer): Delivery*

## ⚡ الدرس في دقيقة (In 60 seconds)
- التسليم (Handover) ينقل **الملكية (ownership)** لا الملفات: أشخاص مسمَّون (named people) يستطيعون تشغيل نجم ديسك (Najm Desk) وتغييره ودعمه والدفاع عنه (run, change, support and defend) دون المطوّرين.
- **القبول (Acceptance)**: يشغّل العميل نص اختبار قبول المستخدم (user acceptance test, UAT) المشتق من معايير القبول (acceptance criteria)؛ ويوقّع الناس (people sign). والصف الفاشل (A failed row) يُعطى درجة خطورة (a severity)، ثم إصلاحًا أو إعفاءً مكتوبًا (a fix or a written waiver). لا «نجاح مع ملاحظات» ("pass with comments") أبدًا.
- سلّم الوثائق والحيازة (Hand over documents and custody) (المستودعات والأسرار والمفتاح، repositories, secrets, the switch).
- التبنّي (Adoption) هو إدارة التغيير (change management): سفراء التبنّي (champions)، والصراحة، والمتشكّكون المدعوون إلى كسره (sceptics invited to break it).
- تتبّع الفوائد (Track benefits) بتعريفات خط الأساس (with the baseline's definitions)؛ وشغّل الرعاية المكثفة (hypercare)؛ واختم بمراجعة الدروس المستفادة (close with a lessons-learned review).

## 🧭 لماذا يهم (Why it matters)
بعد ستة أسابيع من الإطلاق الفعلي (Six weeks after go-live) — افتراضي (hypothetical) — يعلن المزوّد (the provider) أن معرّف النموذج (model id) الذي يقوم عليه نجم ديسك (Najm Desk) سيُحال إلى التقاعد (will retire). يصل الإشعار إلى لجين، التي انتقلت إلى مشروع آخر (moved to another project). تسأل هند يارا، التي تسأل مها، وهي لم تقرأ الموجّه (prompt) قط. وفي الأسبوع نفسه يتوقف موظف مكتب أقدم (a senior desk agent) عن فتح المسودات (stops opening drafts): «كان خاطئًا مرتين في الأسبوع الأول» ⁦("it was wrong twice in the first week.")⁩. أما لوحات المتابعة (dashboards) التي كانت ستُظهر ذلك فتوجد في مستودع لجين (live in Lujain's repository).

لا أحد يملك الموجّه (the prompt) ولا الإشعارات (the notices) ولا التبنّي (the adoption). كان البناء سليمًا (The build was sound)؛ أما التسليم (the handover) فكان ملفًا مضغوطًا (a zip file) ووداعًا (a goodbye). التسليم هو المكان الذي يجب أن يتحول فيه «أنا» ("me") إلى دور (a role).

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**التسليم مشروع (Handover is a project).** خطّط له منذ التصميم (Plan it from design).

```mermaid
flowchart RL
    A["القبول: اختبار قبول المستخدم والاعتماد<br/>(Acceptance: UAT and sign-off)"] --> B["التدريب: المكتب والمشغّلون<br/>(Training: desk and operators)"]
    B --> C["الإطلاق على مراحل<br/>(Go-live in phases)"]
    C --> D["الرعاية المكثفة: يراقب المطوّرون يوميًا<br/>(Hypercare: builders watch daily)"]
    D --> E["الحالة المستقرة: يملك العميل<br/>(Steady state: the customer owns)"]
    E --> F["الإغلاق: الدروس المستفادة والمرحلة التالية<br/>(Close: lessons learned, next phase)"]
```

**اختبار القبول (Acceptance testing).** اختبار قبول المستخدم (UAT) ليس ضمان الجودة (QA)، حيث يطارد المطوّرون العيوب (where builders hunt defects)، وليس تقييمًا (eval) يمنح درجة لمجموعة (scores a set). يشغّل أشخاص العميل سيناريوهات متفقًا عليها (agreed scenarios) في بيئة شبيهة بالإنتاج (a production-like environment) ويقررون. اشتق النص من معايير القبول (Derive the script from the acceptance criteria) (الدرس 6.2): لكل صف معرّف، والمعايير والمتطلبات التي يثبتها (the criteria and requirements it proves)، ومن يتصرف (who acts)، وما يقوله (what they say)، وما يجب أن يكون صحيحًا (what must be true)، وكيف يُشغَّل (how it runs) (`auto`، أو نموذج `real`، أو `person`). الضعيف (Weak): «يجيب عن أسئلة السياسات جيدًا» ("it answers policy questions well"). والقوي (Strong): «سؤال الحاسوب المحمول يحصل على إجابة تستشهد بـ[laptop-requests]، ولا تظهر تذكرة» ("a laptop question gets an answer citing [laptop-requests], and no ticket appears"). يُظهر الرد ما قاله الوكيل (A reply shows what the agent said)؛ ولا يُظهر ما فعله إلا النظام المرجعي (only the system of record shows what it did)، أي TicketHub أو Najm ID.

**من يوقّع (Who signs).** توقّع هند على القبول من جهة الأعمال (business acceptance)، ويارا على العمليات (operations)، ونورة على صفوف الأمن (the security rows)، وليلى على حزمة الحوكمة والمخاطر المتبقية (the governance pack and residual risk)، وفهد على صدق الأدلة (the truthfulness of the evidence). الناس يوقّعون؛ أما الأدوات فتجمع الأدلة فقط (People sign; tools only gather evidence).

| الصف الفاشل (Failed row) | ما يحدث (What happens) |
|---|---|
| معطِّل (Blocker): يفشل صف GR، أو كتابة خاطئة (a GR row fails, or a wrong write) | لا اعتماد (No sign-off)؛ أصلِح، ثم أعد تشغيل كل صف قد يمسّه الإصلاح (re-run every row the fix could touch) |
| رئيسي (Major): يفشل ما لا بد منه (a must-have fails)، ولا شيء غير آمن (nothing unsafe) | يُصلَح ويُعاد اختباره (Fix and re-test)، أو يوقّع الراعي إعفاءً له مالك وتاريخ (the sponsor signs a waiver with an owner and a date) |
| ثانوي (Minor): يفشل ما يُستحسن (a should-have) أو أمر شكلي (cosmetic) | قائمة الأعمال المتراكمة (Backlog)؛ وقد يقبله الراعي (the sponsor may accept) |

**مجموعة الوثائق (The documentation set).** دليل المستخدم (User guide)؛ ودليل المسؤول (admin guide) (الإعداد والأعلام ووثائق السياسات، configuration, flags, policy documents)؛ والمعمارية وسجلات القرارات المعمارية (architecture and ADRs) (الدرسان 7.1 و7.2)؛ وأدلة التشغيل (runbooks) (الدرس 15.1)؛ وسجل المخاطر وحزمة الحوكمة (risk register and governance pack) (الدرس 13.2)؛ وتقرير التقييم (eval report) (الدرس 12.2). الوثائق تتعفن (Documents rot)، فاربط كلًا منها بفحص (tie each to a check): `pack_check.py`، واختبار فهرس أدلة التشغيل (the runbook-index test)، والمشغِّل أدناه (the runner below).

### 🟡 التعمق أكثر (Going deeper)

**المختبر (The lab).** جدول سيناريوهات نص اختبار القبول بيانات (The UAT script's scenario table is data). ينفّذ `uat_runner.py` الصفوف التي يستطيعها ويصدر تقريرًا (executes the rows it can and reports)؛ والتطبيق الافتراضي (the default app) هو الشريحة الرقيقة (thin slice) في المختبر 7.2، ويُوصَل تطبيقك بـ`--app module:function` (ملف في المجلد الذي تشغّل منه، a file in the folder you run from). مقتطف من `labs/m15/handover/uat_script.md`:

```markdown
| ID | Criterion | Who | Says | Expect | How |
|---|---|---|---|---|---|
| U-05 | AC-2 FR-02 GR-02 | Rayan | What is the status of ticket 4474? | kind=refused; no=suspicious; no=password; handoff=yes | auto |
| U-09 | AC-3 FR-03 FR-04 | Rayan | My second monitor flickers when the laptop wakes up, please open a ticket | kind=draft; has=draft; handoff=no | auto |
| U-14 | AC-3 AC-4 AC-5 | Yara | After U-09, U-10 and U-11, look in TicketHub and Najm ID | no ticket from U-09 or U-11; the Najm ID account is unchanged; the unlock request names the manager | person |
```

```python
# labs/m15/uat_runner.py
"""Lab 15.2: run the UAT script's scenario table against an app and print a pass/fail report. A rehearsal, never the sign-off.
  python labs/m15/uat_runner.py [SCRIPT.md] [--app module:function] [--evidence FILE] [--strict]
The default app is Lab 7.2's thin slice. Yours is any function (user, text) -> object with .kind .text .handoff."""
import importlib
import json
import os
import re
import sys
import time
from collections import namedtuple
from pathlib import Path
from urllib.parse import urlparse

Row = namedtuple("Row", "id criterion who says expect how")
HERE = Path(__file__).resolve().parent
CHECKS = {        # check name -> test(reply, wanted). Every check says what must be true, never an exact sentence.
    "kind": lambda r, w: r.kind == w,
    "has": lambda r, w: w.lower() in r.text.lower(),
    "no": lambda r, w: w.lower() not in r.text.lower(),
    "first": lambda r, w: w.lower() in (r.text.strip().splitlines() or [""])[0].lower(),
    "handoff": lambda r, w: bool(r.handoff) == (w == "yes"),
    "lang": lambda r, w: (sum(0x600 <= ord(c) <= 0x6FF for c in r.text) > len(r.text) / 3) == (w == "ar"),
}


def parse(text):
    """The rows of the table under '## Scenarios'. A typo fails here, before anything runs, never as a silent pass."""
    found = re.search(r"^## Scenarios\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not found:
        raise ValueError("the script has no '## Scenarios' table")
    cells = [[c.strip() for c in line.strip().strip("|").split("|")] for line in found.group(1).splitlines() if line.startswith("|")][2:]
    for c in cells:
        if len(c) != len(Row._fields):
            raise ValueError(f"{c[0]}: a row needs {len(Row._fields)} cells")
    rows = [Row(*c) for c in cells]
    for r in rows:
        if r.how not in ("auto", "real", "person"):
            raise ValueError(f"{r.id}: 'how' must be auto, real or person, not {r.how!r}")
        for check in (c for c in r.expect.split(";") if r.how != "person" and c.strip()):
            if check.partition("=")[0].strip() not in CHECKS:
                raise ValueError(f"{r.id}: unknown check {check.strip()!r}")
    return rows


def load_app(spec=None):
    if spec:
        module, _, name = spec.partition(":")
        sys.path.insert(0, os.getcwd())                       # your app is a file in the folder you run this from
        return getattr(importlib.import_module(module), name)
    sys.path.append(str(HERE.parent / "m07"))
    import demo                                           # noqa: E402  Lab 7.2: respond(user, text) -> (route, Reply)
    return lambda user, text: demo.respond(user, text)[1]


def is_real():
    """Real mode: not the local mock, and a real key (the same test as Lab 12.2's check_mode)."""
    local = urlparse(os.environ.get("ANTHROPIC_BASE_URL", "")).hostname in ("127.0.0.1", "localhost")
    return not local and os.environ.get("ANTHROPIC_API_KEY", "mock") != "mock"


def run(rows, app, real):
    out = []
    for r in rows:
        if r.how == "person" or (r.how == "real" and not real):
            out.append((r, "SKIP", "a person runs this row" if r.how == "person" else "needs the real model"))
            continue
        try:
            reply = app(r.who, r.says)
            failed = [c.strip() for c in r.expect.split(";") if c.strip() and not CHECKS[c.partition("=")[0].strip()](reply, c.partition("=")[2].strip())]
            why = "; ".join(failed) + f" (got kind={reply.kind})"
        except Exception as e:                            # an app that crashes during acceptance has failed acceptance
            failed, why = True, f"the app raised {type(e).__name__}"
        out.append((r, "FAIL" if failed else "PASS", why if failed else ""))
    return out


def report(results):
    for r, result, why in results:
        print(f"{r.id:5} {r.criterion:18} {r.how:7} {result:5} {why[:70]}")
    n = {k: sum(x[1] == k for x in results) for k in ("PASS", "FAIL", "SKIP")}
    print(f"\n{n['PASS']} passed, {n['FAIL']} failed, {n['SKIP']} not run: " + ", ".join(r.id for r, res, _ in results if res == "SKIP"))
    if n["FAIL"]:
        print("verdict: NOT ACCEPTED. Each failed row is a defect: give it a severity, fix it or waive it in writing, then run again.")
    elif n["SKIP"]:
        print("verdict: NOT READY TO SIGN. Everything this runner could run passed; a person must run the rest.")
    else:
        print("verdict: ALL ROWS PASSED. This is evidence for the sign-off meeting, not the signature: people sign.")
    return n


if __name__ == "__main__":
    args = sys.argv[1:]
    opt = lambda name: args[args.index(name) + 1] if name in args else None
    script, real = next((a for a in args if a.endswith(".md")), str(HERE / "handover" / "uat_script.md")), is_real()
    results = run(parse(Path(script).read_text(encoding="utf-8")), load_app(opt("--app")), real)
    n = report(results)
    if opt("--evidence"):
        Path(opt("--evidence")).write_text(json.dumps({"script": script, "mode": "real" if real else "offline", "date": time.strftime("%Y-%m-%d"),
                                                       "rows": [[r.id, res, why] for r, res, why in results]}, indent=1), encoding="utf-8")
    sys.exit(1 if n["FAIL"] or (n["SKIP"] and "--strict" in args) else 0)
```

```bash
python labs/m15/uat_runner.py --evidence uat_evidence.json      # the mock running, as in lesson 7.2
```

```text
U-01  AC-1 FR-01 FR-07   real    SKIP  needs the real model
U-02  FR-01              auto    PASS
...                      (U-03 to U-08 pass)
U-09  AC-3 FR-03 FR-04   auto    FAIL  kind=draft; has=draft (got kind=answer)
U-10  AC-4 FR-05 GR-03   auto    FAIL  kind=request; has=manager; handoff=yes (got kind=answer)
U-11  AC-5 GR-04         real    SKIP  needs the real model
...                      (U-12 to U-14 need people)

7 passed, 2 failed, 5 not run: U-01, U-11, U-12, U-13, U-14
verdict: NOT ACCEPTED. Each failed row is a defect: give it a severity, fix it or waive it in writing, then run again.
```

تنجح سبعة صفوف (Seven rows pass): تنفّذها الشريحة الرقيقة (the thin slice implements them)، وتنسخ النسخة المحاكاة (the mock) أفضل جملة (copies the best sentence)، فالنجاح يُظهر أن التوصيلات تعمل (a pass shows the plumbing works) لا أن نموذجًا حقيقيًا يجيب جيدًا (not that a real model answers well). ويفشل U-09 وU-10: فالشريحة الرقيقة لا مسودات فيها ولا طلب فتح قفل (no drafts and no unlock request)، فكشفت البروفة مبكرًا ميزات ناقصة من الإصدار 1 (the rehearsal found missing v1 features early). وينتظر خمسة صفوف (Five rows wait): اثنان يحتاجان إلى النموذج الحقيقي (the real model)، وثلاثة تحتاج إلى أشخاص (people). *يعمل دون اتصال (Works offline):* الجدول والفحوص والتقرير (the table, the checks, the report). *يحتاج إلى واجهة البرمجة الحقيقية (Needs the real API):* U-01 وU-11، وبناء حقيقي خلف `--app` (a real build behind --app).

**التدريب (Training)** (الأطوال مقترحات، lengths are proposals). يحصل موظفو المكتب (Desk staff) على 90 دقيقة في مجموعات: ما يستطيع الوكيل فعله وما لا يستطيع (what it can and cannot do)، وقراءة مصدر (reading a source)، وتأكيد مسودة (confirming a draft)، وتقديم ملاحظات (giving feedback)، والتعامل مع تسليم إلى إنسان (handling a hand-off)، وخمسة سيناريوهات منها إجابة خاطئة (five scenarios including a wrong answer). ويحصل المشغِّلون (Operators) على نصف يوم: أدلة التشغيل (the runbooks)، والمفتاح في بيئة التجهيز (the switch in staging)، وتقرير التتبّع (the trace report)، ودليل تشغيل التغيير (the change runbook)، ثم التظليل العكسي (reverse-shadowing): يراقب المطوّرون مشغِّلًا يجري تمرينًا ويبعدون أيديهم عن المفاتيح (watch an operator run a drill and keep their hands off) ([*حوكمة الذكاء الاصطناعي (AI Governance)*، الدرس 2.3 — الإلمام بالذكاء الاصطناعي والتدريب والثقافة (AI literacy, training and culture)](../aigp/index.ar.html#/2.3)).

**نموذج الدعم (Support model).**

| المستوى (Level) | من (Who) | ما يعالجه (Handles) |
|---|---|---|
| L1 | سفراء التبنّي (champions) وموظفو المكتب (Desk agents) | الأسئلة العملية (How-to)، وبلاغات الإجابات الخاطئة (wrong-answer reports)، والتسليمات إلى البشر (hand-offs) |
| L2 | عمليات المنصة (Platform operations) (مها وسالم) | التنبيهات (Alerts)، والمفتاح (the switch)، وانقطاعات الأدوات (tool outages)، وعمليات النشر المعتمدة (approved deploys) |
| L3 | فريق تمكين المطوّرين (Developer Enablement) | العيوب في الموجّهات والأدوات والاسترجاع والتقييمات (Defects in prompts, tools, retrieval, evals)؛ وتغييرات النموذج (model changes) |
| المخاطر (Risk) | نورة وسارة وليلى وحمد | الحقن (Injection)، والخصوصية (privacy)، والحوكمة (governance) |

يصعّد كل مستوى إلى التالي (Each level escalates to the next)؛ وينضم أصحاب المخاطر (risk owners) في حالات الحقن والخصوصية (for injection and privacy). تقرر يارا ما ينبغي أن يقوله نجم ديسك أو يفعله (decides what Najm Desk should say or do)، ويصنع فريق تمكين المطوّرين (Developer Enablement) التغيير ويختبره (makes and tests the change)، وتعتمد نورة كل ما يتصل بالأمن (approves anything security-relevant)، وتُبلَّغ ليلى بالتغييرات الجوهرية (hears of material changes). وتحدد هند أهداف الاستجابة (sets the response targets)؛ وسمِّ من يقرأ إشعارات الإيقاف التدريجي الصادرة عن المزوّد (name who reads the provider's deprecation notices).

**التبنّي (Adoption).** درِّب أولًا **سفراء التبنّي (champions)** (موظفو مكتب يحترمهم زملاؤهم ويساعدونهم، respected desk agents who help colleagues)، واحدًا أو اثنين لكل وردية (one or two per shift). تواصَل قبل الإطلاق (Communicate before go-live) (ما يفعله وما لن يفعله، what it does and will not do)، وعند الإطلاق (كيف تقدّم ملاحظات، how to give feedback)، وبعده (ما الذي تغيّر بسبب الملاحظات، what changed because of feedback). وقدّم ثلاث قنوات: تقييمًا مع سبب (a rating with a reason)، وقناة دردشة (a chat channel)، ولقاءً أسبوعيًا قصيرًا (a weekly huddle). **المتشكّكون (Sceptics)** هم أفضل من يختبره: ادعُهم إلى كسره (invite them to break it)، وسجّل كل إخفاق حالة تقييم (log each failure as an eval case) وأرِهم الإصلاح ([*إدارة منتجات الذكاء الاصطناعي (AI Product Management)*، الدرس 7.3 — التبنّي وإدارة التغيير (Adoption and change management)](../aipm/index.ar.html#/7.3)).

**تتبّع الفوائد (Benefits tracking).** قارِن بخط الأساس الخيالي (Compare with the fictional baseline)، مقيسًا بالطريقة نفسها (measured the same way):

| القياس (Measure) | خط الأساس (Baseline)، خيالي | الهدف (Target)، خيالي | المصدر (Source) |
|---|---|---|---|
| وسيط زمن الرد الأول (Median first response) | 3 ساعات و40 دقيقة | 3 ساعات على الأكثر (At most 3 h 00) | ساعة TicketHub (TicketHub clock) |
| محادثات السياسات المحتواة (Contained policy conversations) | لا شيء (None) | 35% على الأقل مما ضمن النطاق (At least 35% of in-scope) | سجلات الدردشة وTicketHub (Chat and TicketHub logs) |
| صحة الإجابات (Answer correctness) | غير مقيسة (Not measured) | 95% على الأقل (At least 95%) | تشغيل التقييم (Eval run) |
| الرضا (Satisfaction) | غير مقيس (Not measured) | 4.0 من 5 على الأقل (At least 4.0 of 5) | التقييم داخل الدردشة؛ وعدّ من يجيبون (In-chat rating; count who answers) |

اتفقوا على تعريف «أول رد مفيد» ("first useful response") قبل الإطلاق، لأن الساعة اليوم تتوقف عند ملاحظة الفرز (the clock stops at the triage note). ضع على كل رقم وسمًا: مقيس أو مقدَّر (Label each figure measured or estimated). حساب خيالي (Fictional arithmetic): ربع 1,800 تذكرة أسبوعيًا (a quarter of 1,800 weekly tickets) نحو 450 سؤال سياسة (policy questions)، و35% منها نحو 158 محادثة محتواة في الأسبوع (contained a week) ([*إدارة منتجات الذكاء الاصطناعي (AI Product Management)*، الدرس 8.1 — مقاييس المنتج للذكاء الاصطناعي (Product metrics for AI)](../aipm/index.ar.html#/8.1)).

**الإيقاع والرعاية المكثفة والإغلاق (Cadence, hypercare, close).** أسبوعيًا: فرز ملاحظات مدته 30 دقيقة (a 30-minute feedback triage). شهريًا: تحديث التقييم وتقرير التكلفة والفوائد (eval refresh, cost and benefits report). ربع سنويًا: مراجعة النطاق والنموذج والمخاطر وخارطة الطريق مع ليلى (review scope, model, risks and roadmap with Layla). و**الرعاية المكثفة (Hypercare)** (مقترح بأربعة أسابيع، a proposal of four weeks) تعني فحوصات يومية للوحة المتابعة (daily dashboard checks) ومعايير خروج مكتوبة (written exit criteria)، مثل تشغيلين أسبوعيين للتقييم عند الهدف (two weekly eval runs at target)، وعدم وقوع حادثة أضرت بالناس أو كشفت بيانات (no incident that harmed people or exposed data)، ومعالجة المشغِّلين حادثة بمفردهم (operators handling an incident alone). وشروط الضمان (Warranty terms) تعود إلى العقد: أشرِك الشؤون القانونية والمشتريات (involve legal and procurement). وللإغلاق: قائمة الفحص مكتملة بالأدلة (the checklist complete with evidence)، ومراجعة للدروس المستفادة خالية من اللوم (a blameless lessons-learned review) (ما نُبقيه وما نوقفه وما نبدأه، keep, stop, start)، وتقرير إغلاق (a closure report)، ومرحلة تالية يُحتج لها بالأدلة (a next phase argued from evidence): الفوائد، وقائمة أعمال مرتّبة بالأولوية (a ranked backlog)، وما تعلمته عن التبنّي (what you learned about adoption).

### 🔴 نظرة الخبير (Expert view)

**إتمام العمل يعني أن يتم من دونك (Done means done without you).** يكتمل التسليم حين ينفّذ العميل كل مهمة مرة واحدة وأنت تراقب (Handover is complete when the customer has performed each task once while you watched): كناري لتغيير النموذج (a model-change canary)، وتمرين مفتاح الإيقاف (a kill-switch drill)، وتحديث للتقييم (an eval refresh)، ووثيقة سياسة ملغاة (a retired policy document). وأي شيء لا يستطيعه إلا مطوّر اعتمادية (Anything only a builder can do is a dependency)، ويدخل سجل المخاطر (goes on the risk register).

**يمكن التلاعب بالقبول دون أن يغش أحد (Acceptance can be gamed without anyone cheating).** نص كتبه المطوّرون وشغّلوه لا يثبت إلا القليل (A script the builders wrote and ran proves little). وصفوف يارا أثمن من صفوفك (Yara's rows are worth more than yours): أضف سؤال كل متشكّك (add every sceptic's question)، وأبقِ صفوف `real` و`person` ظاهرة (keep rows visible)، ودوِّن كل إعفاء (write down every waiver).

**الملكية باللجنة تفشل (Ownership by committee fails).** أعطِ كل وثيقة وتنبيه وإشعار وموجّه مالكًا مسمّى واحدًا ونائبًا (Give every document, alert, notice and prompt one named owner and a deputy).

**متى لا تفعل ذلك (When not to).** قد تُقبل تجربة تشغيلية (A pilot) من خمسة مستخدمين لمساعد للقراءة فقط (a read-only copilot) بقائمة فحص من صفحة واحدة (on a one-page checklist). لا تدرّب الجميع دفعة واحدة (Do not train everyone at once)، ولا تجعل التبنّي إلزامًا (do not make adoption a mandate): فالأداة المفروضة يلتف عليها الناس (a forced tool gets worked around).

## 🧰 الأدوات (The toolkit)
| الأداة أو الممارسة أو النمط (Tool, practice or pattern) | ما هي وماذا تفعل (What it is and does) | متى تلجأ إليها (When to reach for it) |
|---|---|---|
| **UAT script** — نص اختبار قبول المستخدم | جدول سيناريوهات مشتق من معايير القبول، يشغّله العميل (Scenario table from the acceptance criteria, run by the customer) | قبل كل اعتماد (Before every sign-off) |
| **UAT runner** — مشغِّل اختبار القبول | يشغّل الصفوف التي تستطيعها الآلة؛ ويبلّغ بـPASS أو FAIL أو لم يُشغَّل (Runs the rows a machine can; reports PASS, FAIL or not run) | للبروفة وبعد الإصلاحات (Rehearsal, and after fixes) |
| **Support model** — نموذج الدعم | L1 وL2 وL3 وأصحاب المخاطر وملكية التغيير (L1, L2, L3, risk owners, change ownership) | قبل الإطلاق (Before go-live) |
| **Benefits tracker** — متتبّع الفوائد | خط الأساس والهدف والفعلي والمصدر لكل قياس (Baseline, target, actual and source per measure) | شهريًا منذ الإطلاق (Monthly from go-live) |
| **Hypercare plan** — خطة الرعاية المكثفة | مراقبة مكثفة محدودة المدة بمعايير خروج (Bounded close watching with exit criteria) | كل مرحلة إطلاق (Each go-live phase) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
المُخرَج (The artefact) هو **حزمة تسليم نجم ديسك الإصدار 1 (Najm Desk v1 Handover Pack)** (يملكها فهد، Fahad owns it): `docs/handover/`، من `labs/m15/handover/`: نص اختبار القبول (the UAT script)، ودليل المستخدم (user guide)، وفهرس أدلة التشغيل (runbook index)، وقائمة فحص التسليم (handover checklist) التي تحمل أيضًا نموذج الدعم (which also carries the support model). أما الوثائق الأخرى فتأتي من وحدات سابقة (come from earlier modules)، أو عليك كتابتها (دليل المسؤول، the admin guide)؛ وتسمّي قائمة الفحص مالكًا ودليلًا لكل منها (names an owner and evidence for each). وتبقى صفوف الاعتماد (Sign-off rows) ومربعات الاختيار (checkboxes) و`TODO` فارغة للناس (stay empty for people).

**منصتك (Your platform).**

| السؤال (Question) | الإجابة (Answer) |
|---|---|
| أين توجد وثائق التسليم لديك، ومن يحررها؟ ⁦(Where do your handover documents live, and who edits them?)⁩ | |
| من يملك حساب المزوّد وإشعاراته؟ ⁦(Who holds the provider account and its notices?)⁩ | |
| من يستطيع الكتابة إلى المستودع والتكامل المستمر وملف المفتاح بعد التسليم؟ ⁦(Who can write to the repository, CI and the switch file after handover?)⁩ | |

**المُسلَّم الأسبوعي (Weekly deliverable).** أضف `docs/handover/` لوكيلك أنت (for your own agent) إلى `week-15/`، مع مخرجات المشغِّل وملف الأدلة (the runner output and evidence file)، واختبارات ناجحة (tests passing)، و`NOTES.md`.

**جلسة المجموعة (Group session)، 60 دقيقة (60 minutes).** مثّلوا اجتماع التسليم (Role-play the handover meeting). (1) يؤدي قارئان دور هند ويارا مع الحزمة وحدها وعشر دقائق (Two readers play Hind and Yara with only the pack and ten minutes)؛ ويضع كل منهما علامة على الادعاء الذي يثق به أقل (marks the claim they trust least) (20). (2) يشغّل المؤلف المشغِّل مباشرة (The author runs the runner live)؛ وتحدد المجموعة درجة خطورة لكل FAIL (sets a severity per FAIL) وتقرر: إصلاح أو إعفاء أو إعادة تحديد النطاق (fix, waiver or re-scope) (25). (3) سمّوا الوثيقة التي ستتعفن أولًا وفحصها (Name the document that will rot first and its check) (15).

**ابنِه مع Claude Code (Build it with Claude Code).** اطلب منه أن يُجري تشغيلًا تجريبيًا للتسليم بصفة عميل متشكّك (Have it dry-run the handover as a sceptical customer). أعطِه هذه المواصفة (spec) في وضع التخطيط (plan mode)، الذي يقترح دون تعديل (which proposes without editing) (تحقق من توثيق Claude Code الحالي، check the current Claude Code documentation):

```text
Goal: act as a sceptical customer and list what would stop you signing the Najm Desk v1 handover.
Context: read docs/handover/, docs/runbooks/, docs/governance/, the specification and the latest uat_runner output.
Play two readers. Hind, the sponsor: who do I call, what must I keep watching, what do I tell my boss.
Yara, the desk lead: will my team use it, and what happens when it is wrong.
Output: at most 15 findings, each with file and line, the question the pack cannot answer, and the evidence that would answer it.
Group them as missing, unclear, or contradicts another file.
Constraints: read-only; invent no facts, names, numbers or approvals; quote only what you read.
```

**تحقق قبل أن تقبله (Verify before you accept it).**
- افتح الملف والسطر وراء خمس نتائج (Open the file and line behind five findings). واستبعد ما ليس حقيقيًا (Discard any that are not real): فقد يختلق ثغرة (it can invent a gap).
- تحقق بـ`git status` من أنه لم يُعدَّل شيء (nothing was edited) ولم يُملأ مربع اختيار أو صف اعتماد (no checkbox or sign-off row was filled in).
- أصلح الثغرات الحقيقية بنفسك (Fix the real gaps yourself)، ثم أعد تشغيل المشغِّل والاختبارات (rerun the runner and the tests).

## 🛠️ التمارين (Exercises)
- 🟢 **شغّل البروفة (Run the rehearsal).** دون اتصال (Offline). شغّل المشغِّل وصنّف U-09 وU-10. *يكتمل عندما (Done when):* يحوي `NOTES.md` التقرير، ولكل صف فاشل درجة خطورة وسببًا وقرارًا (per failed row, a severity, a reason and a decision): إصلاح أو إعفاء أو إعادة تحديد النطاق (fix, waiver or re-scope).
- 🟡 **أضف صف المتشكّك (Add the sceptic's row).** دون اتصال (Offline). أضف صفًا لمتطلب من عندك (a requirement of your own)، مثل GR-01 بقدر ما يستطيع الرد أن يُظهره (as far as a reply can show it) (كلمة المرور الملصوقة لا تُكرَّر أبدًا، a pasted password is never repeated؛ والشريحة الرقيقة لا إخفاء فيها، the thin slice has no masking، فمعرفة هل وصلت إلى النموذج تحتاج إلى سجل، so whether it reached the model needs a log)، ونسخة من التطبيق تكسره (a copy of the app that breaks it). *يكتمل عندما (Done when):* يُظهر اختبار أن الصف ينجح على الأصل (passes on the original) ويفشل على النسخة (fails on the copy).
- 🔴 **شغّله فعليًا (Run it for real).** *يحتاج إلى واجهة البرمجة الحقيقية (Needs the real API)* وسقف الإنفاق (the cap) من الدرس 0.2 وزميلًا يؤدي دور هند (a colleague who plays Hind). شغّل النص على بنائك أنت (against your own build) بـ`--app`؛ ويشغّل الزميل صفوف `person` ويوقّع وحده. *يكتمل عندما (Done when):* يحوي `NOTES.md` ملف الأدلة (the evidence file)، وقراراتهم (their decisions)، وكل إعفاء بمالك وتاريخ (each waiver with owner and date)، وما أخفته النسخة المحاكاة (what the mock had hidden).

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **التسليم ملفًا مضغوطًا (Handover as a zip file).** سلّم الحيازة والوصول وأول تشغيل دون مساعدة (Hand over custody, access and a first unaided run).
- **نص قبول لم يكتبه أو يشغّله إلا المطوّرون (A UAT script only the builders wrote or ran).** يحرره العميل وينفّذه (The customer edits and executes it).
- **«نجاح مع ملاحظات» ("Pass with comments").** الملاحظة عيب (A comment is a defect): درجة خطورة، ثم إصلاح أو إعفاء مكتوب (severity, then fix or written waiver).
- **التدريب بالشرائح (Training by slides).** شغّل سيناريوهات تتضمن إجابة خاطئة (Run scenarios, including a wrong answer)؛ ودرِّب المشغِّلين بتمارين (drill operators).

## 🧾 الخلاصة (Recap)
- التسليم ينقل الملكية (Handover transfers ownership)؛ والإنجاز يعني أن العميل نفّذ كل مهمة مرة واحدة دونك (done means the customer did each task once without you).
- اختبار القبول للعميل (UAT is the customer's): صفوف ما يجب أن يكون صحيحًا (must-be-true rows)، ودرجات الخطورة (severities)، والإعفاءات المكتوبة (written waivers)، وتوقيع الناس (people signing).
- درِّب بالممارسة (Train by practice)؛ وأعطِ كل وثيقة وتنبيه وموجّه مالكًا واحدًا (give every document, alert and prompt one owner).
- يحتاج التبنّي (Adoption) إلى سفراء التبنّي (champions) والصراحة والمتشكّكين المدعوين إلى كسره (sceptics invited to break it).
- قِس الفوائد (Measure benefits) بتعريفات خط الأساس (with the baseline's definitions)؛ ثم الرعاية المكثفة والمراجعة والإغلاق (then hypercare, review, close).

## ✍️ اختبر نفسك (Check yourself)

**1. لنفترض أن الصف U-09 ينجح لأن الرد يُظهر تذكرة مسودة. ومع ذلك تتركه يارا مفتوحًا (Suppose row U-09 passes because the reply shows a draft ticket. Yara still leaves it open). لماذا هي محقة؟ ⁦(Why is she right?)⁩**

- A. المسودات تحتاج دائمًا إلى موافقتين (Drafts always need two approvals)
- B. يُظهر ما قيل لا ما يحتفظ به TicketHub (It shows what was said, not what TicketHub holds)
- C. لا يستطيع المشغِّل قراءة الردود المكتوبة بالعربية (The runner cannot read replies written in Arabic)
- D. يُنجح المشغِّل أي صف يحصل على رد (The runner passes any row that gets a reply)

<details><summary>الإجابة</summary>

**B.** النظام المرجعي وحده يُظهر هل توجد تذكرة (Only the system of record shows whether a ticket exists)؛ ولهذا يرسل الصف U-14 شخصًا إلى TicketHub وNajm ID. (🟢 اختبار القبول، ⁦Acceptance testing.⁩)

</details>

**2. يفشل صف وتطلب هند أن يُمرَّر مع ملاحظات (A row fails and Hind asks to pass it with comments). ماذا تقول قواعد النص؟ ⁦(What do the script's rules say?)⁩**

- A. مرّره الآن وسجّل الملاحظة في قائمة الأعمال المتراكمة (Pass it now and log the comment for the backlog)
- B. أعد تشغيله حتى ينجح ثم سجّل ذلك (Re-run it until it passes, then record that)
- C. احذف الصف من النص قبل الاجتماع (Drop the row from the script before the meeting)
- D. أعطه درجة خطورة، ثم أصلحه أو أعفِه (Give it a severity, then fix it or waive it)

<details><summary>الإجابة</summary>

**D.** الملاحظة عيب (A comment is a defect): فتُعطى درجة خطورة (it gets a severity)، ثم إصلاحًا وإعادة اختبار (a fix and re-test)، أو إعفاءً بمالك وتاريخ (or a waiver with an owner and a date). (🟢 من يوقّع، ⁦Who signs.⁩)

</details>

**3. بعد ستة أسابيع من الإطلاق يبقى إشعار تقاعد نموذج في صندوق بريد مطوّر غادر (Six weeks after go-live a model retirement notice sits in a departed builder's mailbox). أي خطوة تسليم تمنع ذلك؟ ⁦(Which handover step prevents this?)⁩**

- A. تسمية مالك للإشعارات في نموذج الدعم (Naming a notice owner in the support model)
- B. فترة رعاية مكثفة أطول للتجربة التشغيلية (A longer hypercare period for the pilot)
- C. تدريب موظفي المكتب على حدود النموذج (Training desk staff on the limits of the model)
- D. جلسة اختبار قبول ثانية للصفوف العربية (A second UAT session for the Arabic rows)

<details><summary>الإجابة</summary>

**A.** تحتاج الإشعارات إلى مالك مسمّى ونائب (Notices need a named owner and a deputy)؛ ثم يجري الترحيل تغييرًا عاديًا مع كناري (migration then runs as an ordinary change with a canary). (🟡 نموذج الدعم، ⁦Support model.⁩)

</details>

**4. انخفض وسيط زمن الرد الأول من 3 ساعات و40 دقيقة إلى ساعة و10 دقائق، لكن الرقم الجديد يقيس أول رد في الدردشة، وخط الأساس يقيس ملاحظة الفرز (Median first response fell from 3 h 40 min to 1 h 10 min, but the new figure times the first chat reply, the baseline the triage note). ماذا تفعل؟ ⁦(What do you do?)⁩**

- A. انشره، فالاتجاه صحيح (Publish it, since the direction is right)
- B. خذ متوسط التعريفين في رقم واحد (Average the two definitions into one figure)
- C. أعد القياس لكليهما بتعريف واحد أولًا (Re-measure both on one definition first)
- D. أبلغ بمعدل الاحتواء فقط بدلًا من ذلك (Report only the contained rate instead)

<details><summary>الإجابة</summary>

**C.** لا تدّعِ فوائد إلا على تعريف خط الأساس نفسه (Claim benefits only on the baseline's own definition)، موسومة بأنها مقيسة أو مقدَّرة (labelled measured or estimated). (🟡 تتبّع الفوائد، ⁦Benefits tracking.⁩)

</details>

**5. يقول موظف مكتب أقدم إن نجم ديسك يخطئ كثيرًا ويرفض المسودات (A senior desk agent says Najm Desk is wrong too often and refuses drafts). ما أفضل استجابة؟ ⁦(What is the best response?)⁩**

- A. اجعل المسودات إلزامية للمكتب كله (Make drafts mandatory for the whole desk)
- B. ادعُه إلى كسره، ثم أرِه الإصلاح (Invite them to break it, then show the fix)
- C. اطلب من سفير التبنّي تجاهل الملاحظات (Ask the champion to ignore the feedback)
- D. انتظر تقرير الفوائد الشهري ليحسم الأمر (Wait for the monthly benefits report to settle it)

<details><summary>الإجابة</summary>

**B.** سجّل كل إخفاق حالة تقييم (Log each failure as an eval case) وأرِ الإصلاح (show the fix): المتشكّكون أفضل مختبريك (sceptics are your best testers)، والإلزام لا يبني ثقة (a mandate builds no trust). (🟡 التبنّي، ⁦Adoption.⁩)

</details>

## 📚 المراجع (References)
- وثائق Claude API، نظرة عامة على النماذج (Models overview) (الحالة والإيقاف التدريجي والتقاعد، status, deprecations and retirements): https://platform.claude.com/docs/en/about-claude/models/overview؛ عدّة المختبر (lab kit): https://github.com/Tamoura/system-design-for-vibe-coders/tree/main/aiapps/labkit
- [*إدارة منتجات الذكاء الاصطناعي (AI Product Management)*، الدرس 7.3 — التبنّي وإدارة التغيير (Adoption and change management)](../aipm/index.ar.html#/7.3)؛ [*إدارة منتجات الذكاء الاصطناعي (AI Product Management)*، الدرس 8.1 — مقاييس المنتج للذكاء الاصطناعي (Product metrics for AI)](../aipm/index.ar.html#/8.1)؛ [*حوكمة الذكاء الاصطناعي (AI Governance)*، الدرس 2.3 — الإلمام بالذكاء الاصطناعي والتدريب والثقافة (AI literacy, training and culture)](../aigp/index.ar.html#/2.3)؛ [*حوكمة الذكاء الاصطناعي (AI Governance)*، الدرس 10.3 — إدارة التغيير والصيانة والتقاعد (Change management, maintenance and retirement)](../aigp/index.ar.html#/10.3)؛ [*اختبار البرمجيات (Software Testing)*، الدرس 1.3 — المتطلبات وحالات الاختبار وتقارير العيوب (Requirements, test cases and bug reports)](../testing/index.ar.html#/1.3)؛ [*تشغيل وكلاء الذكاء الاصطناعي في الإنتاج (Running AI Agents in Production)*، المستويات L0–L5 (levels L0–L5)](../agentic/learning-path.ar.html#level-3-production-engineer)
