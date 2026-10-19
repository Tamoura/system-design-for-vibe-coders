import os
import socket
import threading
import time

import pytest
import uvicorn

from labkit import mock_server


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def server():
    port = free_port()
    config = uvicorn.Config(mock_server.create_app(""), host="127.0.0.1", port=port, log_level="error")
    srv = uvicorn.Server(config)
    t = threading.Thread(target=srv.run, daemon=True)
    t.start()
    for _ in range(100):
        if srv.started:
            break
        time.sleep(0.05)
    yield f"http://127.0.0.1:{port}"
    srv.should_exit = True


@pytest.fixture
def client(server):
    import anthropic
    return anthropic.Anthropic(base_url=server, api_key="mock", max_retries=0)
