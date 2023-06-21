from queue import Queue
from typing import Any, Optional, Type
from uuid import UUID

from langchain.callbacks.base import BaseCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.output_parsers import PydanticOutputParser
from langchain.schema import ChatMessage

from ..types import Item


class RoleBasedConversationBufferMemory(ConversationBufferMemory):
    def save_context(self, inputs: dict[str, Any], outputs: dict[str, str]) -> None:
        """Save context from this conversation to buffer."""
        input_str, output_str = self._get_input_output(inputs, outputs)

        role, content = input_str.split(": ")[:2]
        self.chat_memory.add_message(ChatMessage(role=role, content=content))
        self.chat_memory.add_ai_message(output_str)


class JSONStreamingHandler(BaseCallbackHandler):
    START_POSITION_DEFAULT: int = -1

    def __init__(
        self,
        item_type: Type[Item],
        queue: Queue,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.queue = queue
        self.buffer: list[str] = []
        self.start_position = self.START_POSITION_DEFAULT
        self.brace_count = 0
        self.in_array = False

        self.item_type = item_type
        self.parser = PydanticOutputParser(
            pydantic_object=self.item_type.get_item_model()
        )

    def _update_buffer(self, char: str) -> None:
        self.buffer.append(char)

    def _reset_buffer(self) -> None:
        self.buffer = []

    def _handle_open_brace(self) -> None:
        if self.start_position == self.START_POSITION_DEFAULT:
            self.start_position = len(self.buffer) - 1
        self.brace_count += 1

    def _handle_close_brace(self) -> None:
        self.brace_count -= 1
        if self.brace_count == 0:
            obj = self.item_type(
                **dict(self.parser.parse("".join(self.buffer[self.start_position :])))
            )
            self.queue.put(obj)

            self.start_position = self.START_POSITION_DEFAULT
            self._reset_buffer()

    def on_llm_new_token(
        self,
        token: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        for char in token:
            # print(char, end='')
            self._update_buffer(char)

            if char == "[":
                self.in_array = True
            elif char == "]":
                self.in_array = False
            if char == "{" and self.in_array:
                self._handle_open_brace()
            elif char == "}" and self.in_array:
                self._handle_close_brace()
