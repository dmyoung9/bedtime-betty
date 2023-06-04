import json
import os
from pathlib import Path
from typing import Optional, Union

from langchain.prompts import SystemMessagePromptTemplate, ChatMessagePromptTemplate

from ..types import Item

BASE_PATH = Path(os.getcwd())
PROMPTS_PATH = BASE_PATH / "prompts"


def load_prompt(filename: Union[str, Path]) -> str:
    file_path = PROMPTS_PATH / filename
    return file_path.read_text()


def get_prompts_for_item(
    obj: Optional[Item] = None,
) -> list[list[ChatMessagePromptTemplate]]:
    prompts = []
    if obj is None:
        prompts_path = PROMPTS_PATH / "system"
        datafile_path = prompts_path / "system.json"
    else:
        prompts_path = PROMPTS_PATH / obj.plural()
        datafile_path = prompts_path / f"{obj.plural()}.json"

    metadata = json.loads(load_prompt(datafile_path))

    for step in metadata.get("steps", []):
        step_prompts = []
        for prompt in step.get("prompts", []):
            message = load_prompt(prompts_path / prompt.pop("filename"))

            prompt_template = (
                SystemMessagePromptTemplate.from_template(template=message, **prompt)
                if obj is None
                else ChatMessagePromptTemplate.from_template(template=message, **prompt)
            )

            step_prompts.append(prompt_template)
        prompts.append(step_prompts)

    return prompts
