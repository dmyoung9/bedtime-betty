import ast
import json

from typing import Any, Callable, Coroutine, Type

from dotenv import load_dotenv

from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema import OutputParserException

from ..chat import JSONStreamingHandler, RoleBasedConversationBufferMemory
from ..types import Item, ItemModel, ItemResponseModel
from ..prompts import get_prompts_for_item

load_dotenv()

MODEL = "gpt-3.5-turbo"


class ChatAPI:
    def __init__(self, ai_prefix, model=MODEL, *args, **kwargs):
        self.chat_args = [model, *args]
        self.chat_kwargs = kwargs
        self.chat = None
        self.ai_prefix = ai_prefix

    def _parse_response(
        self, output: str, obj: Type[ItemResponseModel]
    ) -> list[ItemModel]:
        parser = PydanticOutputParser(pydantic_object=obj)
        try:
            return parser.parse(output).dict()["data"]
        except OutputParserException:
            return self._parse_response(json.dumps(ast.literal_eval(output)), obj)

    async def _run_chain(
        self,
        obj: Type[ItemModel],
        chat: ChatOpenAI,
        callbacks: list[BaseCallbackHandler],
        *args,
        **kwargs
    ) -> list[Item]:
        obj_class = obj.get_dataclass()
        obj_response: Type[ItemResponseModel] = obj.get_response_model()

        info = {"obj_key": obj_class.key(), "obj_plural": obj_class.plural()}
        info["plural"] = "s" if kwargs.get("num", 1) > 1 else ""
        info.update(kwargs)

        system_prompt = ChatPromptTemplate.from_messages(get_prompts_for_item(None)[0])
        memory = RoleBasedConversationBufferMemory(ai_prefix=self.ai_prefix)
        chain = ConversationChain(llm=chat, prompt=system_prompt, memory=memory)

        prompts = get_prompts_for_item(obj_class)
        for step in prompts:
            chat_prompt = ChatPromptTemplate.from_messages(step).format(**info)
            output = await chain.arun(input=chat_prompt, callbacks=callbacks)

        return [
            obj_class(**item) for item in self._parse_response(output, obj_response)
        ]

    async def generate(self, obj: Type[ItemModel], *args, **kwargs) -> list[Item]:
        chat = ChatOpenAI(**self.chat_kwargs)

        return await self._run_chain(obj, chat, [], *args, **kwargs)

    async def stream(
        self,
        obj: Type[ItemModel],
        callback_func: Callable[[ItemModel], Coroutine[Any, Any, None]],
        *args,
        **kwargs
    ) -> None:
        chat = ChatOpenAI(streaming=True, **self.chat_kwargs)
        callbacks = [JSONStreamingHandler(obj, callback_func)]

        await self._run_chain(obj, chat, callbacks, *args, **kwargs)
