"""Readable, prefixed identifiers: ``new_id("TRF")`` -> ``"TRF-9F3A1C7B2D40"``.

In production the token part is random. Tests install a deterministic generator
with ``use_generator(SequentialIds())`` so that ids are predictable.
"""
from __future__ import annotations

import itertools
import re
import uuid
from typing import Callable

_PREFIX = re.compile(r"^[A-Z]{2,5}$")

# None means "random". Tests swap this out through use_generator().
_generator: Callable[[], str] | None = None


def new_id(prefix: str) -> str:
    """Return a new identifier ``<PREFIX>-<TOKEN>``.

    ``prefix`` is 2-5 upper-case ASCII letters (``TRF`` transfer, ``CUS`` customer,
    ``JNL`` journal entry). Raises ValueError for anything else.
    """
    if not isinstance(prefix, str) or not _PREFIX.match(prefix):
        raise ValueError(f"id prefix must be 2-5 upper-case letters, got {prefix!r}")
    token = _generator() if _generator is not None else uuid.uuid4().hex[:12].upper()
    return f"{prefix}-{token}"


class SequentialIds:
    """Deterministic token source: ``000001``, ``000002``, ... (for tests)."""

    def __init__(self, start: int = 1) -> None:
        self._counter = itertools.count(start)

    def __call__(self) -> str:
        return f"{next(self._counter):06d}"


def use_generator(generator: Callable[[], str] | None) -> None:
    """Install a token generator (any zero-argument callable returning str).

    Pass ``None`` to go back to random tokens.
    """
    global _generator
    _generator = generator
