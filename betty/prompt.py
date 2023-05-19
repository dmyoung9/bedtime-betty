from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional


BASE_PATH = Path(os.getcwd())
PROMPTS_PATH = BASE_PATH / "prompts"


class Prompt:
    """A class to represent a text prompt."""

    def __init__(self, prompt: str):
        """Initialize a Prompt instance with the given text."""

        self.prompt = prompt

    @staticmethod
    def from_file(filename: str) -> Prompt:
        """Create a Prompt instance by reading the prompt text from a file."""

        prompt = Path(PROMPTS_PATH / filename).read_text(encoding="utf-8")
        return Prompt(prompt)

    def format(self, info: Optional[dict[str, Any]] = None):
        """Format the prompt text using the provided info dictionary."""

        return self.prompt.format(**info) if info is not None else self.prompt

    def __str__(self) -> str:
        """Return the string representation of the prompt."""

        return self.prompt
