"""Tests for the Module 14.1 lab (labs/m14: app.py, smoke.py, prompts/, Dockerfile, docker-compose.yml, release.yml, release_checklist.yaml).

They check MECHANICS: that configuration is read and refused when wrong, that readiness fails when it should, that a canary is a stable
bucket, that an idempotency key stops a second model call, that logs hold no question text, and that the deployment files have the
properties the lesson claims. The service runs in-process against the offline mock through FastAPI's TestClient.
They cannot show answer quality, and the Dockerfile and compose file are checked as TEXT and as YAML: Docker is not run here, so an image
build and a container start are verified only by a person with a container runtime (Exercise 14.1-C). The workflow is parsed, not run."""
import json
import re
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import anthropic
import pytest
import yaml
from fastapi.testclient import TestClient

KIT = Path(__file__).resolve().parents[1]
LABS = KIT / "labs" / "m14"
V1, V2 = "najm_desk_v1", "najm_desk_v2"
REAL_ENV = {"ANTHROPIC_API_KEY": "sk-ant-not-a-real-key"}


@pytest.fixture
def svc(monkeypatch, server):
    """app.py imported fresh and pointed at the mock; `make` builds a service with its own Settings and a no-retry client."""
    monkeypatch.setenv("ANTHROPIC_BASE_URL", server)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "mock")
    for var in ("MODEL", "PROMPT_VERSION", "CANARY_PROMPT", "CANARY_PERCENT", "APP_ENV", "POLICY_DIR", "PROMPT_DIR", "GIT_SHA"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.syspath_prepend(str(LABS))
    sys.modules.pop("app", None)
    import app

    def make(env=None, client=None):
        cfg = app.Settings(env or {})
        client = client or anthropic.Anthropic(base_url=server, api_key="mock", max_retries=0)
        return cfg, TestClient(app.create_app(cfg, client))
    yield SimpleNamespace(app=app, make=make, url=server)
    sys.modules.pop("app", None)


class Counting:
    """A client that answers without a network and counts the calls it receives."""

    def __init__(self):
        self.calls = []
        self.messages = SimpleNamespace(create=self.create)

    def create(self, **kw):
        self.calls.append(kw)
        return SimpleNamespace(content=[SimpleNamespace(type="text", text="Yes. [vpn]")], model=kw["model"], stop_reason="end_turn",
                               usage=SimpleNamespace(input_tokens=11, output_tokens=3, cache_read_input_tokens=0), _request_id=f"req_{len(self.calls)}")


Q = {"question": "How many days a week can I work remotely?", "user": "rayan"}


def lines(capsys):
    return [json.loads(x) for x in capsys.readouterr().out.splitlines() if x.startswith("{")]


# ---------------------------------------------------------------- configuration

def test_defaults_are_a_dev_environment_with_the_lab_model_and_the_production_prompt(svc):
    cfg = svc.app.Settings({})
    assert (cfg.app_env, cfg.model, cfg.prompt, cfg.canary_prompt, cfg.canary_pct) == ("dev", "claude-sonnet-5-5", V1, "", 0)
    assert cfg.release == "dev" and cfg.timeout_s == 20


def test_everything_comes_from_the_environment(svc):
    cfg = svc.app.Settings({"APP_ENV": "staging", "MODEL": "claude-haiku-5-5", "PROMPT_VERSION": V1, "CANARY_PROMPT": V2,
                            "CANARY_PERCENT": "10", "REQUEST_TIMEOUT_S": "5", "GIT_SHA": "abc123"})
    assert (cfg.app_env, cfg.model, cfg.prompt, cfg.canary_prompt, cfg.canary_pct, cfg.timeout_s, cfg.release) == \
        ("staging", "claude-haiku-5-5", V1, V2, 10, 5.0, "abc123")


@pytest.mark.parametrize("bad", ["-1", "101", "ten"])
def test_a_bad_canary_percentage_stops_the_start_up(svc, bad):
    with pytest.raises(ValueError):
        svc.app.Settings({"CANARY_PERCENT": bad})


@pytest.mark.parametrize("env", [
    {"APP_ENV": "prod"},                                                                          # no key at all: the default is the mock
    {"APP_ENV": "prod", "ANTHROPIC_API_KEY": "mock"},
    {"APP_ENV": "prod", **REAL_ENV, "ANTHROPIC_BASE_URL": "http://127.0.0.1:8787"}])
def test_prod_refuses_the_mock_key_and_a_local_base_url(svc, env):
    with pytest.raises(ValueError, match="prod"):
        svc.app.Settings(env)


def test_prod_starts_with_a_real_looking_key_and_the_default_base_url(svc):
    assert svc.app.Settings({"APP_ENV": "prod", **REAL_ENV}).app_env == "prod"


def test_settings_never_hold_the_api_key(svc):
    cfg = svc.app.Settings({"APP_ENV": "prod", **REAL_ENV})
    assert "sk-ant" not in json.dumps(vars(cfg), default=str)


# ---------------------------------------------------------------- prompts as versioned files

def test_a_prompt_version_is_its_name_and_a_hash_of_the_text_without_the_header(svc, tmp_path):
    (tmp_path / "p.txt").write_text("# header, not sent\nBe brief.\n")
    version, text = svc.app.load_prompt("p", tmp_path)
    assert text == "Be brief.\n" and re.fullmatch(r"p@[0-9a-f]{8}", version)
    (tmp_path / "p.txt").write_text("# a different header\nBe brief.\n")
    assert svc.app.load_prompt("p", tmp_path)[0] == version                    # editing the notes is not a new version
    (tmp_path / "p.txt").write_text("# header\nBe brief!\n")
    assert svc.app.load_prompt("p", tmp_path)[0] != version                    # one character of prompt is


def test_the_two_shipped_prompts_differ_and_neither_contains_a_header_line(svc):
    (v1, t1), (v2, t2) = (svc.app.load_prompt(n, LABS / "prompts") for n in (V1, V2))
    assert v1 != v2 and t1 != t2 and "#" not in (t1 + t2) and "HANDOFF" in t1 and "stolen" in t2 and "stolen" not in t1


def test_a_missing_prompt_file_stops_the_start_up_not_the_first_customer(svc):
    with pytest.raises(FileNotFoundError):
        svc.make({"PROMPT_VERSION": "no_such_prompt"})


def test_the_prompt_files_name_themselves_on_their_first_line(svc):
    for n in (V1, V2):
        assert (LABS / "prompts" / f"{n}.txt").read_text().splitlines()[0] == f"# labs/m14/prompts/{n}.txt"


# ---------------------------------------------------------------- canary

def share(svc, pct, n=2000):
    cfg = svc.app.Settings({"PROMPT_VERSION": V1, "CANARY_PROMPT": V2, "CANARY_PERCENT": str(pct)})
    return sum(svc.app.pick_prompt(cfg, f"user{i}") == V2 for i in range(n)) / n


def test_a_canary_of_zero_reaches_nobody_and_of_one_hundred_reaches_everybody(svc):
    assert share(svc, 0) == 0.0 and share(svc, 100) == 1.0


def test_a_canary_of_twenty_percent_reaches_about_a_fifth(svc):
    assert 0.17 <= share(svc, 20) <= 0.23


def test_a_user_stays_in_the_same_bucket_and_a_bigger_canary_only_adds_users(svc):
    cfg = lambda pct: svc.app.Settings({"PROMPT_VERSION": V1, "CANARY_PROMPT": V2, "CANARY_PERCENT": str(pct)})
    users = [f"user{i}" for i in range(300)]
    five = {u for u in users if svc.app.pick_prompt(cfg(5), u) == V2}
    twenty = {u for u in users if svc.app.pick_prompt(cfg(20), u) == V2}
    assert five <= twenty and all(svc.app.pick_prompt(cfg(5), u) == svc.app.pick_prompt(cfg(5), u) for u in users)


def test_the_bucket_is_the_same_in_every_process_so_replicas_agree(svc):
    code = ("import sys; sys.path.insert(0, 'labs/m14'); import app; "
            "c = app.Settings({'PROMPT_VERSION': 'a', 'CANARY_PROMPT': 'b', 'CANARY_PERCENT': '50'}); "
            "print(''.join(app.pick_prompt(c, f'user{i}') for i in range(40)))")
    runs = {subprocess.run([sys.executable, "-c", code], cwd=KIT, env={"PYTHONHASHSEED": seed, "PATH": "/usr/bin:/bin", "ANTHROPIC_API_KEY": "mock"},
                           capture_output=True, text=True, timeout=60).stdout for seed in ("1", "2", "3")}
    assert len(runs) == 1 and set(runs.pop().strip()) == {"a", "b"}                   # python's built-in hash() would differ per process


def test_no_canary_prompt_means_no_canary_whatever_the_percentage(svc):
    cfg = svc.app.Settings({"CANARY_PERCENT": "100"})
    assert {svc.app.pick_prompt(cfg, f"u{i}") for i in range(50)} == {V1}


def test_rollback_is_one_value(svc, capsys):
    c = Counting()
    env = {"PROMPT_VERSION": V1, "CANARY_PROMPT": V2, "CANARY_PERCENT": "100"}
    _, on = svc.make(env, c)
    assert on.post("/v1/ask", json=Q).json()["prompt_version"].startswith(V2)
    _, off = svc.make({**env, "CANARY_PERCENT": "0"}, c)
    assert off.post("/v1/ask", json=Q).json()["prompt_version"].startswith(V1)
    assert c.calls[0]["system"] != c.calls[1]["system"]                         # and the text the model saw really changed


# ---------------------------------------------------------------- liveness, readiness, version

def test_liveness_never_calls_the_model_or_reads_any_dependency(svc):
    c = Counting()
    _, http = svc.make({"POLICY_DIR": "/does/not/exist"}, c)
    assert http.get("/health").json() == {"status": "ok"} and c.calls == []


def test_readiness_is_green_when_the_service_can_work(svc):
    c = Counting()
    _, http = svc.make({}, c)
    assert http.get("/ready").json()["ready"] is True and c.calls == []         # a probe is free: it never pays for a model call


def test_readiness_fails_without_policy_documents(svc, tmp_path):
    _, http = svc.make({"POLICY_DIR": str(tmp_path)})
    r = http.get("/ready")
    assert r.status_code == 503 and r.json()["detail"]["problems"] == ["no policy documents"]
    assert http.get("/health").status_code == 200                               # alive but not ready: the platform stops sending traffic, it does not restart


def test_readiness_fails_without_an_api_key(svc, monkeypatch):
    _, http = svc.make({})
    monkeypatch.delenv("ANTHROPIC_API_KEY")
    assert http.get("/ready").json()["detail"]["problems"] == ["no API key"]


def test_readiness_also_reports_what_is_running_and_every_prompt_that_can_be_served(svc):
    _, http = svc.make({"PROMPT_VERSION": V1, "CANARY_PROMPT": V2, "CANARY_PERCENT": "5", "GIT_SHA": "abc123", "MODEL": "claude-haiku-5-5"})
    body = http.get("/ready").json()
    assert body["ready"] is True and body["release"] == "abc123" and body["model"] == "claude-haiku-5-5" and set(body["prompts"]) == {V1, V2}
    assert all(re.fullmatch(r"najm_desk_v\d@[0-9a-f]{8}", v) for v in body["prompts"].values())


# ---------------------------------------------------------------- asking

def test_an_answer_cites_a_document_and_names_the_prompt_and_request(svc):
    _, http = svc.make({})
    body = http.post("/v1/ask", json=Q).json()
    assert "[remote-work]" in body["answer"] and body["prompt_version"].startswith(V1) and body["request_id"].startswith("req_mock_")
    assert body["model"] == "claude-sonnet-5-5"


def test_the_model_receives_the_configured_model_a_bounded_reply_and_only_the_question(svc):
    c = Counting()
    _, http = svc.make({"MODEL": "claude-haiku-5-5"}, c)
    http.post("/v1/ask", json=Q)
    (call,) = c.calls
    assert call["model"] == "claude-haiku-5-5" and call["max_tokens"] >= 1024 and call["output_config"] == {"effort": "low"}
    assert "temperature" not in call and "tool_choice" not in call
    assert call["messages"] == [{"role": "user", "content": Q["question"]}]            # the user message is the question and nothing else


def test_the_policy_library_is_a_cached_stable_prefix_in_front_of_the_prompt_text(svc):
    c = Counting()
    env = {"PROMPT_VERSION": V1, "CANARY_PROMPT": V2}
    _, v1 = svc.make(env, c)
    _, v2 = svc.make({**env, "CANARY_PERCENT": "100"}, c)
    v1.post("/v1/ask", json=Q)
    v2.post("/v1/ask", json=Q)
    (docs1, text1), (docs2, text2) = c.calls[0]["system"], c.calls[1]["system"]
    assert docs1["cache_control"] == {"type": "ephemeral"} and "cache_control" not in text1
    assert docs1 == docs2 and text1 != text2                                           # a new prompt version does not invalidate the cached library
    assert docs1["text"].count("<document id=") == 15 and '<document id="vpn">' in docs1["text"]
    assert all(m in docs1["text"] for m in ("</document>\n", "Staff must use the corporate VPN"))


def test_load_docs_is_deterministic_and_empty_for_an_empty_folder(svc, tmp_path):
    folder = KIT / "labkit" / "data" / "policies"
    assert svc.app.load_docs(folder) == svc.app.load_docs(folder) and svc.app.load_docs(tmp_path) == ""      # same bytes every time, or the cache never hits
    assert svc.app.load_docs(folder).index('<document id="ai-tools">') < svc.app.load_docs(folder).index('<document id="wifi">')    # sorted, not directory order


@pytest.mark.parametrize("payload", [{"question": ""}, {"question": "x" * 2001}, {}, {"question": 5}])
def test_bad_input_is_a_422_and_never_reaches_the_model(svc, payload):
    c = Counting()
    _, http = svc.make({}, c)
    assert http.post("/v1/ask", json=payload).status_code == 422 and c.calls == []


# ---------------------------------------------------------------- idempotency

def test_the_same_key_from_the_same_user_replays_and_pays_once(svc):
    c = Counting()
    _, http = svc.make({}, c)
    first = http.post("/v1/ask", json=Q, headers={"Idempotency-Key": "k1"}).json()
    again = http.post("/v1/ask", json=Q, headers={"Idempotency-Key": "k1"}).json()
    assert len(c.calls) == 1 and again == {**first, "replayed": True} and "replayed" not in first


def test_a_key_belongs_to_one_user(svc):
    c = Counting()
    _, http = svc.make({}, c)
    http.post("/v1/ask", json=Q, headers={"Idempotency-Key": "k1"})
    other = http.post("/v1/ask", json={**Q, "user": "lujain"}, headers={"Idempotency-Key": "k1"}).json()
    assert len(c.calls) == 2 and "replayed" not in other                         # another person's key never replays someone else's answer


def test_without_a_key_every_request_is_new_and_nothing_is_remembered(svc):
    c = Counting()
    _, http = svc.make({}, c)
    http.post("/v1/ask", json=Q)
    http.post("/v1/ask", json=Q)
    assert len(c.calls) == 2


# ---------------------------------------------------------------- failure

def test_a_provider_error_becomes_a_calm_503_without_provider_detail(svc, capsys):
    _, http = svc.make({})
    r = http.post("/v1/ask", json={**Q, "question": Q["question"] + " [mock:overloaded]"})
    assert r.status_code == 503 and "Service Desk" in r.json()["detail"]
    assert "Overloaded" not in r.text and "529" not in r.text and "Traceback" not in r.text
    (rec,) = [x for x in lines(capsys) if x["event"] == "model_error"]
    assert rec["error"] == "OverloadedError"


@pytest.mark.parametrize("stop", ["max_tokens", "refusal", "pause_turn"])
def test_a_reply_that_did_not_end_its_turn_is_a_hand_off_never_an_answer(svc, capsys, stop):
    """A cut-off (max_tokens) or declined (refusal) reply is not an answer: Najm Desk hands off and logs why, without the question."""
    c = Counting()
    inner = c.create
    c.messages.create = lambda **kw: SimpleNamespace(**{**vars(inner(**kw)), "stop_reason": stop, "content": [SimpleNamespace(type="text", text="Remote work is allowed up to th")]})
    _, http = svc.make({}, c)
    body = http.post("/v1/ask", json=Q).json()
    assert body["answer"].startswith("HANDOFF:") and "Remote work" not in body["answer"]
    (rec,) = [x for x in lines(capsys) if x["event"] == "no_answer"]
    assert rec["stop"] == stop and Q["question"] not in json.dumps(rec)


def test_a_failed_request_is_not_remembered_under_its_key(svc):
    _, http = svc.make({})
    bad = http.post("/v1/ask", json={**Q, "question": Q["question"] + " [mock:overloaded]"}, headers={"Idempotency-Key": "k9"})
    good = http.post("/v1/ask", json=Q, headers={"Idempotency-Key": "k9"})
    assert bad.status_code == 503 and good.status_code == 200 and "replayed" not in good.json()


# ---------------------------------------------------------------- logs

def test_one_structured_log_line_per_answer_with_tokens_and_ids_and_no_question_text(svc, capsys):
    _, http = svc.make({"APP_ENV": "staging", "GIT_SHA": "abc123"})
    secret = "My password is Summer2026! how many remote days"
    http.post("/v1/ask", json={"question": secret, "user": "rayan"}, headers={"Idempotency-Key": "k-private"})
    out = capsys.readouterr().out
    (rec,) = [json.loads(x) for x in out.splitlines() if x.startswith("{")]
    assert rec["event"] == "ask" and rec["env"] == "staging" and rec["release"] == "abc123" and rec["prompt_version"].startswith(V1)
    assert rec["input_tokens"] > 0 and rec["output_tokens"] > 0 and rec["cache_read"] == 0 and rec["request_id"].startswith("req_mock_")
    assert set(rec) == {"ts", "env", "release", "event", "prompt_version", "model", "input_tokens", "output_tokens", "cache_read", "ms", "request_id"}
    assert "Summer2026" not in out and "rayan" not in out and "mock" not in out.replace("req_mock_", "")      # no question, no user, no key


# ---------------------------------------------------------------- the smoke test

def run_smoke(url, **extra):
    env = {"ANTHROPIC_BASE_URL": url, "ANTHROPIC_API_KEY": "mock", "PATH": "/usr/bin:/bin", **extra}
    return subprocess.run([sys.executable, str(LABS / "smoke.py")], env=env, capture_output=True, text=True, timeout=60)


def test_the_smoke_test_passes_against_the_mock(svc):
    r = run_smoke(svc.url)
    assert r.returncode == 0, r.stdout + r.stderr
    assert r.stdout.count("PASS  ") == 6 and "FAIL" not in r.stdout


def test_the_smoke_test_fails_when_readiness_fails(svc, tmp_path):
    r = run_smoke(svc.url, POLICY_DIR=str(tmp_path))
    assert r.returncode == 1 and "FAIL  readiness answers" in r.stdout


def test_the_smoke_test_can_check_a_deployed_service_by_url(svc):
    import threading
    import uvicorn
    cfg, _ = svc.make({})
    server = uvicorn.Server(uvicorn.Config(svc.app.create_app(cfg, anthropic.Anthropic(base_url=svc.url, api_key="mock", max_retries=0)),
                                           host="127.0.0.1", port=0, log_level="error"))
    threading.Thread(target=server.run, daemon=True).start()
    for _ in range(100):
        if server.started:
            break
        import time
        time.sleep(0.05)
    port = server.servers[0].sockets[0].getsockname()[1]
    try:
        r = run_smoke(svc.url, SMOKE_URL=f"http://127.0.0.1:{port}")
        assert r.returncode == 0 and r.stdout.count("PASS  ") == 6, r.stdout + r.stderr
        down = run_smoke(svc.url, SMOKE_URL="http://127.0.0.1:9")
        assert down.returncode != 0                                                 # nothing there: the check fails, it does not pass
    finally:
        server.should_exit = True


def test_the_smoke_test_fails_when_the_provider_is_down(svc):
    r = run_smoke("http://127.0.0.1:9", REQUEST_TIMEOUT_S="2")                  # nothing listens there
    assert r.returncode == 1 and "FAIL  an answer arrives with a citation" in r.stdout


def test_the_smoke_test_imports_httpx2_because_anthropic_1x_does_not_install_the_old_httpx():
    import ast
    imported = {a.name for n in ast.walk(ast.parse((LABS / "smoke.py").read_text())) if isinstance(n, ast.Import) for a in n.names}
    assert "httpx2" in imported and "httpx" not in imported       # `import httpx` only worked where another package happened to install it


# ---------------------------------------------------------------- the container files (as text and as YAML: Docker is not run)

def stages(text):
    parts = re.split(r"^FROM .*?(?: AS (\w+))?$", text, flags=re.M)
    return dict(zip(parts[1::2], parts[2::2]))


def test_the_dockerfile_is_multi_stage_pinned_non_root_and_ends_on_the_runtime_stage():
    text = (LABS / "Dockerfile").read_text()
    froms = re.findall(r"^FROM (\S+)(?: AS (\w+))?", text, flags=re.M)
    assert [name for _, name in froms] == ["build", "mock", "runtime"]            # the LAST stage is what a plain build ships
    assert all(image == "${PYTHON_IMAGE}" for image, _ in froms)
    default = re.search(r"^ARG PYTHON_IMAGE=(\S+)$", text, flags=re.M).group(1)
    assert ":latest" not in text and re.fullmatch(r"python:3\.\d+\.\d+-slim-\w+", default)      # an exact patch release, not a moving tag
    runtime = text[text.index("AS runtime"):]
    user = re.findall(r"^USER (\S+)$", runtime, flags=re.M)
    assert user and user[-1].isdigit() and int(user[-1]) > 0                       # numeric and not root
    assert runtime.rstrip().splitlines()[-1].startswith("CMD [")


def test_the_dockerfile_keeps_secrets_tests_and_the_mock_out_of_the_runtime_image():
    text = (LABS / "Dockerfile").read_text()
    runtime = text[text.index("AS runtime"):]
    assert not re.search(r"^(ENV|ARG)\b.*(KEY|TOKEN|SECRET|PASSWORD)", text, flags=re.I | re.M) and "sk-ant" not in text      # a secret in ENV or ARG is in the image history
    copies = re.findall(r"^COPY (?:--from=\S+ )?(\S+) ", runtime, flags=re.M)                  # what the runtime stage takes in, by source path
    assert copies == ["/venv", "labkit/data/policies", "labs/m14/prompts", "labs/m14/app.py"]
    assert not any(c in ("labkit", ".", "tests") for c in copies) and "mock_server" not in runtime
    assert "--no-cache-dir" in text and "COPY --from=build /venv /venv" in runtime
    assert not [x for x in text.splitlines() if re.match(r"^\s*(RUN|USER|CMD|ENV|COPY|ARG|FROM)\b.*\s#\s", x) and "python -c" not in x]    # no inline comments: Docker would read them as arguments


def test_the_dockerfile_copies_exactly_what_the_service_reads_at_run_time():
    text = (LABS / "Dockerfile").read_text()
    runtime = text[text.index("AS runtime"):]
    copied = re.findall(r"^COPY (?!--from)(\S+) (\S+)$", runtime, flags=re.M)
    assert ("labkit/data/policies", "./labkit/data/policies") in copied            # app.py reads HERE.parents[1] / labkit / data / policies
    assert ("labs/m14/prompts", "./labs/m14/prompts") in copied and ("labs/m14/app.py", "./labs/m14/app.py") in copied
    assert 'uvicorn", "--app-dir", "labs/m14", "app:app"' in runtime


def test_the_service_runs_from_the_layout_the_image_builds(svc, tmp_path):
    """Docker is not run, but the layout is rehearsed: copy exactly what the runtime stage copies, then start the app from there."""
    root = tmp_path / "app"
    (root / "labs" / "m14").mkdir(parents=True)
    (root / "labkit" / "data").mkdir(parents=True)
    (root / "labs" / "m14" / "app.py").write_text((LABS / "app.py").read_text())
    subprocess.run(["cp", "-r", str(LABS / "prompts"), str(root / "labs" / "m14" / "prompts")], check=True)
    subprocess.run(["cp", "-r", str(KIT / "labkit" / "data" / "policies"), str(root / "labkit" / "data" / "policies")], check=True)
    code = ("import sys; sys.path.insert(0, 'labs/m14'); import app; from fastapi.testclient import TestClient; c = TestClient(app.app); "
            "print(c.get('/ready').status_code, c.get('/ready').json()['prompts'])")
    env = {"ANTHROPIC_BASE_URL": svc.url, "ANTHROPIC_API_KEY": "mock", "PATH": "/usr/bin:/bin"}
    r = subprocess.run([sys.executable, "-c", code], cwd=root, env=env, capture_output=True, text=True, timeout=60)
    assert r.returncode == 0 and r.stdout.startswith("200 {'najm_desk_v1': 'najm_desk_v1@"), r.stderr


def test_the_requirements_pin_the_sdk_range_and_nothing_heavy_ships():
    reqs = [x for x in (LABS / "requirements.txt").read_text().splitlines() if x and not x.startswith("#")]
    assert reqs == ["anthropic>=1,<2", "fastapi", "uvicorn", "pydantic>=2"]


def test_compose_runs_the_runtime_stage_read_only_with_no_capabilities_and_no_real_key():
    compose = yaml.safe_load((LABS / "docker-compose.yml").read_text())
    api, mock = compose["services"]["api"], compose["services"]["mock"]
    assert api["build"]["target"] == "runtime" and mock["build"]["target"] == "mock"
    assert api["read_only"] is True and api["cap_drop"] == ["ALL"] and "no-new-privileges:true" in api["security_opt"]
    assert api["depends_on"] == ["mock"]
    env = api["environment"]
    assert env["ANTHROPIC_API_KEY"] == "mock" and env["ANTHROPIC_BASE_URL"] == "http://mock:8787" and env["APP_ENV"] == "dev"
    assert "sk-ant" not in (LABS / "docker-compose.yml").read_text()
    assert api["build"]["context"] == "../.." and api["build"]["dockerfile"] == "labs/m14/Dockerfile"


# ---------------------------------------------------------------- the pipeline and the checklist

WORKFLOW = yaml.safe_load((LABS / "release.yml").read_text())
JOBS = WORKFLOW["jobs"]
TRIGGERS = WORKFLOW[True]                                                         # PyYAML reads the bare key `on` as True (YAML 1.1)


def steps_text(job):
    return "\n".join(str(s.get("run", "")) + str(s.get("uses", "")) for s in JOBS[job]["steps"])


def test_the_workflow_parses_and_has_the_three_stages_in_order():
    assert list(JOBS) == ["verify", "image", "canary"]
    assert [JOBS[j].get("needs") for j in JOBS] == [None, "verify", "image"]
    assert set(TRIGGERS) == {"pull_request", "push", "workflow_dispatch"} and "pull_request_target" not in TRIGGERS


def test_pull_requests_get_the_free_checks_only_and_no_secret():
    text = (LABS / "release.yml").read_text()
    assert "secrets." not in text and WORKFLOW["permissions"] == {"contents": "read"}
    verify = steps_text("verify")
    assert "pytest tests/test_m14_" in verify and "smoke.py" in verify and "gate.py" in verify and "--mode mock" in verify
    assert [s["env"]["ANTHROPIC_API_KEY"] for s in JOBS["verify"]["steps"] if "env" in s] == ["mock"]        # the only key a pull request ever sees
    assert JOBS["image"]["if"] == "github.event_name != 'pull_request'"


def test_the_canary_waits_for_a_person():
    assert JOBS["canary"]["environment"] == "canary"                                  # required reviewers are set on the environment
    assert JOBS["canary"]["if"] == "github.event_name == 'workflow_dispatch'"
    assert TRIGGERS["workflow_dispatch"]["inputs"]["canary_percent"]["default"] == "5"
    assert "canary_percent" in steps_text("canary") and "docker build" in steps_text("image")


def test_the_workflow_never_runs_two_rollouts_at_once_and_has_timeouts():
    assert WORKFLOW["concurrency"]["cancel-in-progress"] is False and JOBS["verify"]["timeout-minutes"] <= 30


def test_the_checklist_has_nine_unique_items_each_asking_for_evidence_and_a_four_part_manifest():
    doc = yaml.safe_load((LABS / "release_checklist.yaml").read_text())
    assert set(doc["release"]) == {"image", "prompt", "model", "eval_baseline"}
    ids = [i["id"] for i in doc["items"]]
    assert ids == [f"R{n}" for n in range(1, 10)]
    assert all(set(i) == {"id", "check", "evidence"} and len(i["check"]) > 20 for i in doc["items"])
    text = " ".join(i["check"].lower() for i in doc["items"])
    for must in ("eval", "non-root", "rollback", "kill switch", "canary", "readiness", "sign-off"):
        assert must in text


def test_the_files_name_themselves_on_their_first_line():
    for name in ("app.py", "smoke.py", "Dockerfile", "docker-compose.yml", "release.yml", "release_checklist.yaml", "requirements.txt"):
        assert (LABS / name).read_text().splitlines()[0].startswith(f"# labs/m14/{name}")
