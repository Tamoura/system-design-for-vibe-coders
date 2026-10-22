"""najmkit: Najm Bank's internal helper library (vendored copy, API v2).

Every Najm Bank service uses these three small helpers instead of rolling its own:

    najmkit.ids    make_id(prefix)           readable, prefixed identifiers
    najmkit.clock  utc_now(), FixedClock     one place to get "the current time"
    najmkit.audit  emit(event, **fields)     append-only JSON-lines audit trail

Version 2.0.0 renamed most of the functions and made audit.emit strict about the values it is given.
The v1 names still work in 2.x: each one is a thin wrapper that raises a DeprecationWarning and calls
the v2 function. Version 3.0 removes them. Read docs/najmkit-v2-migration.md before you move a service.

This is an *internal* library. It is not on PyPI, so nothing outside the bank (including an AI model)
can know its API from training data. docs/najmkit.md is the reference for the v1 names; the migration
notes list what changed.
"""

API_VERSION = "v2"
__version__ = "2.0.0"
