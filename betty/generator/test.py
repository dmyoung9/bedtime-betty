import random
from typing import AsyncGenerator, Type, Union
from . import BaseGenerator
from ..types.items import Image, Item, Page

codes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]


class TestGenerator(BaseGenerator[Item]):
    def __init__(self, *args, **kwargs):
        super().__init__("bedtime_betty")

    async def _generate(self, obj, *args, **kwargs):
        if obj == Image:

            def hex_color():
                return "".join([random.choice(codes) for _ in range(6)])

            def text_color(hex_color):
                r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
                lum = 0.299 * r + 0.587 * g + 0.114 * b
                return "fff" if lum < 128 else "000"

            bg_color = hex_color()
            text = text_color(bg_color)
            return [
                {
                    "url": f"https://placehold.co/{kwargs.get('size', 1024)}"
                    f"/{bg_color}/{text}"
                }
                for _ in range(kwargs.get("num", 6))
            ]
        elif obj == Page:
            return obj.examples(kwargs.get("num", 3))["pages"]

        return obj.examples(kwargs.get("num", 3))

    async def _stream(self, obj, *args, **kwargs):
        for item in obj.examples(kwargs.get("num", 3)):
            yield item

    async def generate_story_items(self, obj: Type[Item], **kwargs) -> list[Item]:
        return await self.generate_items(obj, **kwargs)

    async def stream_story_items(
        self, obj: Type[Item], **kwargs
    ) -> AsyncGenerator[Item, None]:
        async for item in self.stream_items(obj, **kwargs):
            yield item

    def _build_filename(self, obj: Union[Type[Item], str]) -> str:
        return f"{obj}.md" if isinstance(obj, str) else f"{obj.__name__.lower()}s.md"

    def _build_info(self, **kwargs):
        kwargs.pop("obj", None)
        return kwargs
