"""T03: searching customers by name treats the fragment as data, never as SQL."""
from remit.models import Customer
from remit.store import Store


def a_store():
    store = Store(":memory:")
    store.add_customer(Customer("C1", "Brian O'Brien", "T1"))
    store.add_customer(Customer("C2", "Aisha Rahman", "T2"))
    return store


def test_an_ordinary_search_still_finds_names_case_insensitively():
    assert [c.id for c in a_store().search_by_name("RAH")] == ["C2"]


def test_a_quote_mark_in_the_fragment_is_just_a_character():
    assert [c.id for c in a_store().search_by_name("O'B")] == ["C1"]


def test_a_crafted_fragment_does_not_change_the_query():
    assert a_store().search_by_name("zzz%' OR name LIKE '%") == []
