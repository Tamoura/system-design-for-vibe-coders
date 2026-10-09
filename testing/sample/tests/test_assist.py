from najm.assist import Agent, FakeModel, answer, retrieve


def test_retrieval_finds_the_limits_document():
    assert retrieve("what is the daily limit")[0][0] == "limits"


def test_answer_is_grounded_in_the_policy():
    result = answer("What is the daily transfer limit?")
    assert "50,000 QAR" in result["text"]
    assert result["sources"][0] == "limits"


def test_unknown_questions_get_a_polite_no_answer():
    assert "can't find that" in answer("Can I pay in bitcoin?")["text"]


def test_temperature_zero_is_deterministic():
    a = answer("What is the daily transfer limit?", FakeModel(temperature=0))
    b = answer("What is the daily transfer limit?", FakeModel(temperature=0))
    assert a == b


def test_freezing_a_card_needs_confirmation():
    agent = Agent()
    turn = agent.handle("Please freeze card-1")
    assert turn["tool_calls"] == []
    assert "confirm" in turn["reply"].lower()
