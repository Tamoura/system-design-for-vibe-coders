"""Configuration from environment variables (see .env.example).

Remit reads real environment variables only. It does not load ``.env`` files: export
the variables, or let your shell tool do it. Nothing secret is needed to run Remit.

    REMIT_ENV        dev | test | prod                     (default dev)
    REMIT_DB         path of the SQLite file               (default remit.db)
    REMIT_AUDIT_LOG  path of the audit JSON-lines file     (default: no file)
    REMIT_WATCHLIST  path of a watchlist file, one name per line (default: built-in demo list)
    REMIT_LANG       default notification language: en | ar (default en)
"""
from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass

from remit.models import LANGUAGES

ENVIRONMENTS = ("dev", "test", "prod")


@dataclass(frozen=True)
class Config:
    env: str = "dev"
    db_path: str = "remit.db"
    audit_log: str | None = None
    watchlist_path: str | None = None
    language: str = "en"


def load_config(environ: Mapping[str, str] | None = None) -> Config:
    """Build a Config from ``environ`` (``os.environ`` by default). Raises ValueError on bad values."""
    env = os.environ if environ is None else environ
    config = Config(
        env=env.get("REMIT_ENV", "dev"),
        db_path=env.get("REMIT_DB", "remit.db"),
        audit_log=env.get("REMIT_AUDIT_LOG") or None,
        watchlist_path=env.get("REMIT_WATCHLIST") or None,
        language=env.get("REMIT_LANG", "en"),
    )
    if config.env not in ENVIRONMENTS:
        raise ValueError(f"REMIT_ENV must be one of {ENVIRONMENTS}, got {config.env!r}")
    if config.language not in LANGUAGES:
        raise ValueError(f"REMIT_LANG must be one of {LANGUAGES}, got {config.language!r}")
    return config
