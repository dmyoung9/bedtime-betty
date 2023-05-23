import openai

from betty.api.openai import guard_errors

from .. import BaseAPI


class ImageAPI(BaseAPI):
    def __init__(self, api_key: str):
        openai.api_key = api_key

    # @guard_errors
    async def _get_images(
        self, prompt: str, size: int = 1024, response_format="url", num=1
    ) -> list[str]:
        """Returns an image generated based on the given prompt and parameters."""

        image_response = await openai.Image.acreate(
            prompt=prompt, n=num, size=f"{size}x{size}", response_format=response_format
        )

        content = image_response["data"]
        return [image[response_format] for image in content]

    async def get_json(
        self,
        prompt: str,
        size: int = 1024,
        response_format="url",
        num: int = 1,
        **kwargs,
    ) -> list[dict]:
        response = await self._get_images(
            prompt=prompt,
            size=size,
            response_format=response_format,
            num=num,
        )

        return [{"url": url} for url in response]

    async def stream_json(self, *args, **kwargs):
        raise ValueError("Dall-E 2 does not support streaming images.")
