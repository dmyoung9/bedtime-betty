from abc import ABCMeta, abstractmethod

from typing import Any, AsyncGenerator, Generic, Type, TypeVar, Union

T = TypeVar("T")

DEFAULT_NUM = 3
DEFAULT_AGE = 7


class BaseGenerator(Generic[T], metaclass=ABCMeta):
    def __init__(self, system_prompt: str, *args, **kwargs):
        self.system_prompt = system_prompt

    @abstractmethod
    def _build_filename(self, obj: Union[Type[T], str]) -> str:
        ...

    @abstractmethod
    def _build_info(
        self,
        *args,
        **kwargs,
    ) -> dict[str, Any]:
        ...

    @abstractmethod
    async def _generate(self, obj, *args, **kwargs):
        ...

    @abstractmethod
    async def _stream(self, obj, *args, **kwargs):
        ...

    async def generate_items(
        self,
        obj: Type[T],
        **kwargs,
    ) -> list[T]:
        info = self._build_info(obj=obj, **kwargs)
        filename = self._build_filename(obj)
        system_prompt_filename = self._build_filename(self.system_prompt)

        print(f"Generating {filename.split('.')[0]} for {info}...")

        items = await self._generate(obj, filename, system_prompt_filename, **info)
        print(items)

        return [obj(**item) for item in items]

    async def stream_items(
        self,
        obj: Type[T],
        **kwargs,
    ) -> AsyncGenerator[T, None]:
        info = self._build_info(obj=obj, **kwargs)
        filename = self._build_filename(obj)
        system_prompt_filename = self._build_filename(self.system_prompt)

        print(f"Streaming {filename.split('.')[0]} for {info}...")

        async for item in self._stream(obj, filename, system_prompt_filename, **info):
            yield obj(**item)
