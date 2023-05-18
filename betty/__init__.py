from abc import ABCMeta, abstractmethod

from typing import Any, AsyncGenerator, Generic, Type, TypeVar

T = TypeVar("T")

DEFAULT_NUM = 3
DEFAULT_AGE = 7


class BaseAPI(metaclass=ABCMeta):
    @abstractmethod
    def build_messages(self, *args, **kwargs):
        ...

    @abstractmethod
    def get_json(self, *args, **kwargs):
        ...

    @abstractmethod
    def stream_json(self, *args, **kwargs):
        ...


class BaseGenerator(Generic[T], metaclass=ABCMeta):
    def __init__(self, api: BaseAPI, system_prompt: str, *args, **kwargs):
        self.api = api
        self.system_prompt = system_prompt

    @abstractmethod
    def _build_filename(self, obj: Type[T]) -> str:
        ...

    @abstractmethod
    def _build_info(
        self,
        **kwargs,
    ) -> dict[str, Any]:
        ...

    async def generate_items(
        self,
        obj: Type[T],
        **kwargs,
    ) -> list[T]:
        info = self._build_info(**kwargs)
        filename = self._build_filename(obj)
        print(f"Generating {filename.split('.')[0]} for {info}...")

        messages = self.api.build_messages(filename, **info)
        items = await self.api.get_json(messages)

        return [obj(**item) for item in items]

    async def stream_items(
        self,
        obj: Type[T],
        **kwargs,
    ) -> AsyncGenerator[T, None]:
        info = self._build_info(**kwargs)
        filename = self._build_filename(obj)
        print(f"Streaming {filename.split('.')[0]} for {info}...")

        messages = self.api.build_messages(filename, **info)
        async for item in self.api.stream_json(messages):
            yield obj(**item)
