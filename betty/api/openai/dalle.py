import base64
import openai

from betty.api.openai import guard_errors

from .. import BaseAPI


class ImageAPI(BaseAPI):
    def __init__(self, api_key: str):
        openai.api_key = api_key

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
