"""Customer notifications in English and Arabic.

``render(template_id, lang, **values)`` fills a template. ``Money`` values are
formatted for the language: English writes ``1,234.50 QAR``; Arabic writes the amount
in Arabic-Indic digits with Arabic separators and the currency's Arabic name
(``١٬٢٣٤٫٥٠ ريال قطري``). Other values (names, ids) are inserted as they are. Extra
values that a template does not use are ignored; a missing one raises
MissingTemplateVariable.

A *notifier* delivers a notification to a customer in the customer's language. Two are
provided: ``InMemoryNotifier`` (keeps what it "sent", used by tests) and
``ConsoleNotifier`` (prints it, used by the CLI). There is no email or SMS gateway in
this repository.
"""
from __future__ import annotations

import string
import sys
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Protocol, TextIO

from remit.errors import MissingTemplateVariable, UnknownTemplate, UnsupportedLanguage
from remit.models import LANGUAGES, Customer
from remit.money import Money

ARABIC_INDIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"
ARABIC_DECIMAL_SEPARATOR = "٫"
ARABIC_THOUSANDS_SEPARATOR = "٬"

CURRENCY_NAMES_AR: dict[str, str] = {
    "QAR": "ريال قطري",
    "INR": "روبية هندية",
    "PHP": "بيزو فلبيني",
    "EGP": "جنيه مصري",
    "PKR": "روبية باكستانية",
    "BDT": "تاكا بنغلاديشية",
}

TEMPLATES: dict[str, dict[str, str]] = {
    "transfer_sent": {
        "en": (
            "Hi {name}, your transfer {transfer_id} was sent. "
            "{recipient} received {receive_amount}. "
            "You paid {send_amount} plus a fee of {fee}."
        ),
        "ar": (
            "مرحباً {name}، تم إرسال تحويلك {transfer_id}. "
            "تم استلام مبلغ {receive_amount} من قبل {recipient}. "
            "المبلغ المرسل: {send_amount}، والرسوم: {fee}."
        ),
    },
    "transfer_failed": {
        "en": (
            "Hi {name}, your transfer of {send_amount} to {recipient} could not be completed. "
            "{reason} No money has been taken from your account."
        ),
        "ar": (
            "مرحباً {name}، تعذّر إتمام تحويلك بمبلغ {send_amount} إلى {recipient}. "
            "{reason} لم يتم خصم أي مبلغ من حسابك."
        ),
    },
}

# Customer-facing reasons for transfer_failed. Deliberately vague for "needs_review":
# we never tell a customer that a name matched a sanctions list.
FAILURE_REASONS: dict[str, dict[str, str]] = {
    "limit_exceeded": {
        "en": "It would take you over your sending limit.",
        "ar": "سيتجاوز هذا التحويل حد الإرسال المسموح لك.",
    },
    "needs_review": {
        "en": "We need to review it before it can go ahead. Please contact us.",
        "ar": "نحتاج إلى مراجعته قبل المتابعة. يرجى التواصل معنا.",
    },
}


def localize_digits(text: str, lang: str) -> str:
    """Replace ASCII digits with Arabic-Indic digits when ``lang`` is Arabic."""
    _check_lang(lang)
    if lang == "ar":
        return text.translate(str.maketrans("0123456789", ARABIC_INDIC_DIGITS))
    return text


def format_money(money: Money, lang: str) -> str:
    """``1,234.50 QAR`` in English; ``١٬٢٣٤٫٥٠ ريال قطري`` in Arabic."""
    _check_lang(lang)
    number = f"{money.amount:,.2f}"
    if lang == "en":
        return f"{number} {money.currency}"
    number = localize_digits(number, "ar")
    number = number.replace(",", ARABIC_THOUSANDS_SEPARATOR).replace(".", ARABIC_DECIMAL_SEPARATOR)
    return f"{number} {CURRENCY_NAMES_AR[money.currency]}"


def format_number(value: Decimal, lang: str) -> str:
    """A plain Decimal (for example a rate) with the language's digits and separator."""
    text = format(value, "f")
    if lang == "ar":
        return localize_digits(text, "ar").replace(".", ARABIC_DECIMAL_SEPARATOR)
    _check_lang(lang)
    return text


def failure_reason(code: str, lang: str) -> str:
    """The customer-facing sentence for a ``transfer_failed`` reason code."""
    _check_lang(lang)
    try:
        return FAILURE_REASONS[code][lang]
    except KeyError:
        raise UnknownTemplate(f"no failure reason {code!r}") from None


def _check_lang(lang: str) -> None:
    if lang not in LANGUAGES:
        raise UnsupportedLanguage(f"unsupported language {lang!r}; expected one of {LANGUAGES}")


def render(template_id: str, lang: str, **values: Any) -> str:
    """Render template ``template_id`` in ``lang`` (``"en"`` or ``"ar"``)."""
    _check_lang(lang)
    try:
        template = TEMPLATES[template_id][lang]
    except KeyError:
        raise UnknownTemplate(f"no template {template_id!r} for language {lang!r}") from None
    shown: dict[str, Any] = {}
    for key, value in values.items():
        if isinstance(value, Money):
            shown[key] = format_money(value, lang)
        elif isinstance(value, Decimal):
            shown[key] = format_number(value, lang)
        else:
            shown[key] = value
    needed = {name for _, name, _, _ in string.Formatter().parse(template) if name}
    missing = sorted(needed - shown.keys())
    if missing:
        raise MissingTemplateVariable(f"template {template_id!r} needs {', '.join(missing)}")
    return template.format(**shown)


@dataclass(frozen=True)
class Notification:
    customer_id: str
    template_id: str
    lang: str
    text: str


class Notifier(Protocol):
    def notify(self, customer: Customer, template_id: str, **values: Any) -> Notification: ...


@dataclass
class InMemoryNotifier:
    """Renders in the customer's language and remembers it in ``sent``."""

    sent: list[Notification] = field(default_factory=list)

    def notify(self, customer: Customer, template_id: str, **values: Any) -> Notification:
        text = render(template_id, customer.language, name=customer.name, **values)
        note = Notification(customer.id, template_id, customer.language, text)
        self.sent.append(note)
        return note


class ConsoleNotifier:
    """Prints the notification (what the CLI uses)."""

    def __init__(self, stream: TextIO | None = None) -> None:
        self._stream = stream

    def notify(self, customer: Customer, template_id: str, **values: Any) -> Notification:
        text = render(template_id, customer.language, name=customer.name, **values)
        print(f"[notification to {customer.id} ({customer.language})] {text}", file=self._stream or sys.stdout)
        return Notification(customer.id, template_id, customer.language, text)
