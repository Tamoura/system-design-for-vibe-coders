# labs/m02/promptfile.py
"""Prompts as code: a prompt is a file in Git; the loader returns the text to send and a PROMPT_VERSION to log.
Leading # lines are notes for humans and are not sent."""
import hashlib
from dataclasses import dataclass
from pathlib import Path

PROMPT_DIR = Path(__file__).parent / "prompts"


@dataclass(frozen=True)
class Prompt:
    name: str   # the file stem, for example "classify_v3"
    text: str   # exactly what is sent as the system prompt
    sha: str    # 8 hex characters of the SHA-256 of the text: one changed character gives a new value

    @property
    def version(self) -> str:
        return f"{self.name}@{self.sha}"   # PROMPT_VERSION: log it on every call, store it in every result


def load_prompt(name: str, directory: Path = PROMPT_DIR) -> Prompt:
    lines = (directory / f"{name}.txt").read_text(encoding="utf-8").splitlines()
    while lines and lines[0].startswith("#"):          # the header: path, changelog, owner
        lines.pop(0)
    text = "\n".join(lines).strip() + "\n"
    return Prompt(name, text, hashlib.sha256(text.encode("utf-8")).hexdigest()[:8])
