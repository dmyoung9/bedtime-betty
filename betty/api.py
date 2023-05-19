import ast
import base64

from functools import wraps
import os
import json
from pathlib import Path
from typing import AsyncGenerator, Iterable, Literal, TypedDict

import openai
import tiktoken


from betty import BaseAPI
from betty.prompt import Prompt

BASE_PATH = Path(os.getcwd())
PROMPTS_PATH = BASE_PATH / "prompts"

MODEL = "gpt-3.5-turbo-0301"
Role = Literal["system", "assistant", "user"]


class Message(TypedDict):
    role: Role
    content: str


def guard_errors(func):
    """A decorator function that handles OpenAI API errors."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except openai.error.APIError as e:
            # Handle API error here, e.g. retry or log
            print(f"OpenAI API returned an API Error: {e}")
        except openai.error.APIConnectionError as e:
            # Handle connection error here
            print(f"Failed to connect to OpenAI API: {e}")
        except openai.error.RateLimitError as e:
            # Handle rate limit error (we recommend using exponential backoff)
            print(f"OpenAI API request exceeded rate limit: {e}")

    return wrapper


def count_tokens(text: str, model: str = MODEL) -> int:
    """Returns the number of tokens in the given text,
    according to the specified model's tokenization rules."""

    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def system(content: str) -> Message:
    """Creates a system message with the given content."""

    return OpenAI.message("system", content)


def assistant(content: str) -> Message:
    """Creates an assistant message with the given content."""

    return OpenAI.message("assistant", content)


def user(content: str) -> Message:
    """Creates a user message with the given content."""
    # noqa: F821
    return OpenAI.message("user", content)


class OpenAI(BaseAPI):
    """A class that provides methods for interacting with the OpenAI API."""

    def __init__(self, api_key: str):
        openai.api_key = api_key

    @staticmethod
    def message(role: Role, content: str) -> Message:
        """Creates a message with the given role and content."""

        return {"role": role, "content": content}

    def build_messages(
        self, system_prompt_filename: str, prompt_filename: str, **kwargs
    ) -> Iterable[Message]:
        system_prompt = Prompt.from_file(PROMPTS_PATH / system_prompt_filename).format()
        prompt = Prompt.from_file(PROMPTS_PATH / prompt_filename).format(kwargs)

        return [
            system(system_prompt),
            user(prompt),
        ]

    @guard_errors
    async def _get_completion(
        self,
        messages: Iterable[Message],
        model: str = MODEL,
        temperature: float = 1,
    ) -> str:
        """Returns the text generated by the model based on the given messages."""

        response = await openai.ChatCompletion.acreate(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=False,
        )

        return response["choices"][0]["message"]["content"]

    @guard_errors
    async def _stream_completion(
        self,
        messages: Iterable[Message],
        model: str = MODEL,
        temperature: float = 1,
    ) -> AsyncGenerator[str, None]:
        """Streams the generated text in chunks based on the given messages."""

        response = await openai.ChatCompletion.acreate(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=True,
        )

        async for chunk in response:
            yield chunk["choices"][0]["delta"]

    async def get_json(
        self,
        messages: Iterable[Message],
        model: str = MODEL,
        temperature: float = 1,
    ):
        """Streams the generated text in chunks based on the given messages."""

        response = await self._get_completion(
            model=model,
            messages=messages,
            temperature=temperature,
        )

        return json.loads(response)

    async def stream_json(
        self,
        messages: Iterable[Message],
        model: str = MODEL,
        temperature: float = 1,
    ) -> AsyncGenerator[dict, None]:
        """Streams the generated text in chunks based on the given messages."""

        response = self._stream_completion(
            model=model,
            messages=messages,
            temperature=temperature,
        )

        buffer = ""
        start_position = -1
        brace_count = 0

        async for chunk in response:
            for char in chunk.get("content", ""):
                buffer += char
                if char == "{":
                    if start_position == -1:
                        start_position = len(buffer) - 1
                    brace_count += 1
                elif char == "}":
                    brace_count -= 1
                    if brace_count == 0:
                        try:
                            yield json.loads(buffer[start_position:])
                        except json.JSONDecodeError:
                            yield ast.literal_eval(buffer[start_position:])

                        start_position = -1
                        buffer = buffer[len(buffer) :]  # Keep the buffer clean

    @guard_errors
    async def get_image(
        self, prompt: str, size: int = 1024, response_format="url"
    ) -> str:
        """Returns an image generated based on the given prompt and parameters."""

        image_response = await openai.Image.acreate(
            prompt=prompt, n=1, size=f"{size}x{size}", response_format=response_format
        )

        content = image_response["data"][0][response_format]
        return base64.b64decode(content) if response_format == "b64_json" else content
