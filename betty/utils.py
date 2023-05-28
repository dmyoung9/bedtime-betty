import os
from pathlib import Path


BASE_PATH = Path(os.getcwd())
PROMPTS_PATH = BASE_PATH / "prompts"


def load_prompt(filename):
    file_path = PROMPTS_PATH / filename
    return file_path.read_text()
