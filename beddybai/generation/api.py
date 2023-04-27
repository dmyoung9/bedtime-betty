from functools import wraps
from typing import Iterable

import aiohttp
import openai

from ..common.config import MODEL, OPENAI_API_KEY
from .types import Message, Role

openai.api_key = OPENAI_API_KEY


def guard_errors(func):
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


class OpenAI:
    @staticmethod
    def message(role: Role, content: str) -> Message:
        return {"role": role, "content": content}

    @staticmethod
    def system(content: str) -> Message:
        return OpenAI.message("system", content)

    @staticmethod
    def assistant(content: str) -> Message:
        return OpenAI.message("assistant", content)

    @staticmethod
    def user(content: str) -> Message:
        return OpenAI.message("user", content)

    async def get_completion(
        self, messages: Iterable[Message], model: str = MODEL, temperature: float = 1
    ) -> str:
        """Gets an "all-at-once" completion from the API."""

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}",
        }
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": False,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                chat_response = await response.json()
                return chat_response["choices"][0]["message"]["content"]

    @guard_errors
    async def get_image(self, prompt: str, size: int = 1024) -> str:
        """Gets the URL to a generated image based on the prompt."""

        # url = "https://api.openai.com/v1/images/generations"
        # headers = {
        #     "Content-Type": "application/json",
        #     "Authorization": f"Bearer {OPENAI_API_KEY}",
        # }
        # data = {"prompt": prompt}

        image_response = await openai.Image.acreate(
            prompt=prompt, n=1, size=f"{size}x{size}", response_format="url"
        )

        return image_response["data"][0]["url"]

    @guard_errors
    async def get_streaming_completion(
        self, messages: Iterable[Message], model=MODEL, temperature=1
    ):
        """
        Gets a "streaming" completion from the API.
        Yields chunks as they are generated.
        """

        response = await openai.ChatCompletion.acreate(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=True,
        )

        async for chunk in response:
            yield chunk["choices"][0]["delta"]
