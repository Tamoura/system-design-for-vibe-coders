"""najmkit: Najm Bank's internal helper library (vendored copy, API v1).

Every Najm Bank service uses these three small helpers instead of rolling its own:

    najmkit.ids    new_id(prefix)          readable, prefixed identifiers
    najmkit.clock  now(), FixedClock       one place to get "the current time"
    najmkit.audit  log_event(event, **f)   append-only JSON-lines audit trail

This is an *internal* library. It is not on PyPI, so nothing outside the bank
(including an AI model) can know its API from training data. Read
docs/najmkit.md in the repository root; it is the reference for this vendored copy.
"""

API_VERSION = "v1"
__version__ = "1.3.0"
