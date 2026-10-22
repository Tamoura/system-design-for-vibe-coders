"""Fixtures for lab m10's hidden tests only (this conftest applies to tests/_hidden and nothing else)."""
import io

import pytest


@pytest.fixture
def cli():
    """Run ``python -m remit <argv>`` in-process and return (exit code, stdout, stderr).

    ``remit.cli`` is imported inside the function, not at the top of a test file: a broken
    cli.py (an unresolved merge conflict, say) must only fail the tests that need the command
    line, so the report can say which task is still wrong.
    """

    def run(*argv, environ=None, clock=None):
        from remit.cli import main

        out, err = io.StringIO(), io.StringIO()
        code = main(list(argv), environ=environ, clock=clock, out=out, err=err)
        return code, out.getvalue(), err.getvalue()

    return run
