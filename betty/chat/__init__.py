from typing import Any, Awaitable, Callable, Optional, Type
from uuid import UUID

from langchain.callbacks.base import AsyncCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.output_parsers import PydanticOutputParser
from langchain.schema import ChatMessage

from ..types import ItemModel


class RoleBasedConversationBufferMemory(ConversationBufferMemory):
    def save_context(self, inputs: dict[str, Any], outputs: dict[str, str]) -> None:
        """Save context from this conversation to buffer."""
        input_str, output_str = self._get_input_output(inputs, outputs)

        role, content = input_str.split(": ")[:2]
        self.chat_memory.add_message(ChatMessage(role=role, content=content))
        self.chat_memory.add_ai_message(output_str)


class JSONStreamingHandler(AsyncCallbackHandler):
    START_POSITION_DEFAULT: int = -1

    def __init__(
        self,
        obj: Type[ItemModel],
        callback_func: Callable[[ItemModel], Awaitable[Any]],
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.item_model = obj
        self.callback_func = callback_func
        self.buffer: list[str] = []
        self.start_position = self.START_POSITION_DEFAULT
        self.brace_count = 0
        self.in_array = False
        self.parser = PydanticOutputParser(pydantic_object=self.item_model)

    def _update_buffer(self, char: str) -> None:
        self.buffer.append(char)

    def _reset_buffer(self) -> None:
        self.buffer = []

    def _handle_open_brace(self) -> None:
        if self.start_position == self.START_POSITION_DEFAULT:
            self.start_position = len(self.buffer) - 1
        self.brace_count += 1

    def _handle_close_brace(self) -> Optional[ItemModel]:
        self.brace_count -= 1
        if self.brace_count == 0:
            obj = self.item_model(
                **dict(self.parser.parse("".join(self.buffer[self.start_position :])))
            )

            self.start_position = self.START_POSITION_DEFAULT
            self._reset_buffer()
            return obj

        return None

    def _check_token(self, token: str) -> Optional[ItemModel]:
        obj = None

        for char in token:
            self.buffer += char

            if char == "[":
                self.in_array = True
            elif char == "]":
                self.in_array = False
            if char == "{" and self.in_array:
                self._handle_open_brace()
            elif char == "}" and self.in_array:
                obj = self._handle_close_brace()

        return obj

    async def on_llm_new_token(
        self,
        token: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        if obj := self._check_token(token):
            return await self.callback_func(obj)

        return await super().on_llm_new_token(
            token, run_id=run_id, parent_run_id=parent_run_id, **kwargs
        )
