"""Lab m14, hidden acceptance tests, part 5: quote, send, the ledger, the KYC limits and the command line together.

The fixtures (``service``, ``customers``, ``notifier``, ``store``) come from the repository's own tests/conftest.py:
C001 Aisha (T2, English), C002 Bilal (T1, English), C003 Mariam (T3, Arabic).
"""
from decimal import Decimal

import pytest

from remit.money import Money


def qar(amount):
    return Money(amount, "QAR")


EN_AISHA = (
    "Hi Aisha Rahman, your transfer TRF-000001 to Bangladesh was sent. "
    "Rahim Uddin received 16,437.25 BDT at a rate of 1 QAR = 32.8745 BDT. "
    "You paid 500.00 QAR plus a fee of 14.50 QAR. "
    "Please keep this message as your receipt."
)
AR_MARIAM = (
    "مرحباً Mariam Saleh، تم إرسال تحويلك TRF-000001 إلى بنغلاديش. "
    "تم استلام مبلغ ٣٩٤٬٤٩٤٫٠٠ تاكا بنغلاديشية من قبل Rahim Uddin بسعر صرف ١ ريال قطري مقابل ٣٢٫٨٧٤٥ تاكا. "
    "المبلغ المرسل: ١٢٬٠٠٠٫٠٠ ريال قطري، والرسوم: ١٣٠٫٠٠ ريال قطري. "
    "يرجى الاحتفاظ بهذه الرسالة كإيصال لك."
)


def test_a_quote_prices_the_fee_the_rate_and_the_receive_amount(service):
    quote = service.quote(qar("500"), "BDT")
    assert quote.corridor.code == "QAR-BDT"
    assert (quote.fee, quote.total) == (qar("14.50"), qar("514.50"))
    assert quote.fx.rate == Decimal("32.8745")
    assert quote.fx.receive == Money("16437.25", "BDT")
    assert quote.delivery_method == "bank_deposit" and not quote.express


def test_an_express_quote_adds_the_surcharge_and_a_wallet_quote_is_allowed(service):
    quote = service.quote(qar("500"), "BDT", express=True, delivery_method="wallet")
    assert quote.fee == qar("32.50") and quote.total == qar("532.50") and quote.delivery_method == "wallet"


def test_quote_and_send_refuse_what_the_corridor_refuses(service):
    from remit.errors import AmountOutOfRange, UnsupportedDeliveryMethod

    with pytest.raises(AmountOutOfRange):
        service.quote(qar("99.99"), "BDT")
    with pytest.raises(AmountOutOfRange):
        service.send("C003", qar("12000.01"), "BDT", "Rahim Uddin")
    with pytest.raises(UnsupportedDeliveryMethod):
        service.send("C001", qar("500"), "BDT", "Rahim Uddin", delivery_method="cash_pickup")


def test_a_send_stores_the_transfer_with_the_bangladesh_numbers(service, store):
    result = service.send("C001", qar("500"), "BDT", "Rahim Uddin")
    t = result.transfer
    assert (t.corridor, t.send_amount, t.fee) == ("QAR-BDT", qar("500.00"), qar("14.50"))
    assert (t.receive_amount, t.rate, t.delivery_method) == (Money("16437.25", "BDT"), Decimal("32.8745"), "bank_deposit")
    assert result.total_debited == qar("514.50") and result.notified
    assert store.get_transfer(t.id) == t


def test_the_english_customer_gets_the_bangladesh_wording(service, notifier):
    service.send("C001", qar("500"), "BDT", "Rahim Uddin")
    note = notifier.sent[-1]
    assert (note.template_id, note.lang) == ("transfer_sent_bdt", "en")
    assert note.text == EN_AISHA


def test_the_arabic_customer_gets_the_arabic_wording_at_the_maximum(service, notifier):
    result = service.send("C003", qar("12000.00"), "BDT", "Rahim Uddin")
    assert result.transfer.fee == qar("130.00") and result.transfer.receive_amount == Money("394494.00", "BDT")
    note = notifier.sent[-1]
    assert (note.template_id, note.lang) == ("transfer_sent_bdt", "ar")
    assert note.text == AR_MARIAM


def test_the_other_corridors_keep_the_ordinary_message(service, notifier):
    service.send("C001", qar("500"), "INR", "Ravi Kumar")
    note = notifier.sent[-1]
    assert note.template_id == "transfer_sent"
    assert note.text.startswith("Hi Aisha Rahman, your transfer TRF-000001 was sent. Ravi Kumar received 11,286.00 INR.")


def test_the_ledger_is_posted_in_qar_with_the_usual_split(service):
    from remit import ledger

    service.send("C001", qar("500"), "BDT", "Rahim Uddin")
    assert ledger.balance("CUSTOMER:C001") == Decimal("-514.50")
    assert ledger.balance("PAYOUT_CLEARING") == Decimal("500.00")
    assert ledger.balance("PARTNER_PAYABLE") == Decimal("4.35")
    assert ledger.balance("FEE_INCOME") == Decimal("10.15")


def test_kyc_limits_apply_to_bangladesh_like_everywhere_else(service, notifier, store):
    from remit.errors import LimitExceeded

    service.send("C002", qar("2000.00"), "BDT", "Rahim Uddin")  # T1: the daily limit is reached exactly
    with pytest.raises(LimitExceeded):
        service.send("C002", qar("100.00"), "BDT", "Rahim Uddin")
    assert notifier.sent[-1].template_id == "transfer_failed"
    assert "over your sending limit" in notifier.sent[-1].text
    assert store.count_transfers() == 1


def test_one_cent_over_the_daily_limit_is_refused_even_though_the_corridor_allows_more(service):
    from remit.errors import LimitExceeded

    with pytest.raises(LimitExceeded):
        service.send("C002", qar("2000.01"), "BDT", "Rahim Uddin")  # T1 daily 2,000.00
    with pytest.raises(LimitExceeded):
        service.send("C001", qar("10000.01"), "BDT", "Rahim Uddin")  # T2 daily 10,000.00
    assert service.send("C001", qar("10000.00"), "BDT", "Rahim Uddin").transfer.fee == qar("130.00")


def test_a_quote_the_customer_saw_is_honoured_and_expires_after_a_minute(service, clock):
    from remit.errors import QuoteExpired

    quote = service.quote(qar("500"), "BDT")
    result = service.send("C001", qar("500"), "BDT", "Rahim Uddin", quote=quote)
    assert result.transfer.rate == Decimal("32.8745")
    clock.advance(seconds=61)
    with pytest.raises(QuoteExpired):
        service.send("C001", qar("500"), "BDT", "Rahim Uddin", quote=quote)


def test_the_command_line_quotes_bangladesh(cli):
    code, out, err = cli("quote", "QAR", "500", "BDT")
    assert code == 0 and err == ""
    for line in (
        "Corridor:  QAR -> BDT",
        "Send:      500.00 QAR",
        "Fee:       14.50 QAR",
        "Total:     514.50 QAR",
        "Rate:      32.8745 (valid for 60 s)",
        "Receive:   16437.25 BDT",
        "Delivery:  bank_deposit",
    ):
        assert line in out.splitlines()


def test_the_command_line_reports_a_refused_amount_and_a_refused_delivery_method(cli):
    code, _, err = cli("quote", "QAR", "99.99", "BDT")
    assert code == 1 and "amount_out_of_range" in err
    code, _, err = cli("quote", "QAR", "500", "BDT", "--delivery", "cash_pickup")
    assert code == 1 and "unsupported_delivery_method" in err


def test_the_command_line_sends_and_prints_the_bangladesh_message(cli, tmp_path):
    env = {"REMIT_DB": str(tmp_path / "remit.db")}
    assert cli("customer", "add", "--id", "C100", "--name", "Aisha Rahman", "--kyc", "T2", environ=env)[0] == 0
    code, out, err = cli("send", "--customer", "C100", "QAR", "500", "BDT", "--recipient", "Rahim Uddin", environ=env)
    assert code == 0, err
    assert "to Bangladesh was sent" in out and "1 QAR = 32.8745 BDT" in out
    assert "(fee 14.50 QAR) -> 16437.25 BDT at 32.8745" in out
