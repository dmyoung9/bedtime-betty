# import asyncio
from dotenv import load_dotenv
from typing import Type

# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI

# from langchain.memory import ConversationBufferMemory
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate

from betty.chat import JSONStreamingHandler, RoleBasedConversationBufferMemory

from betty.types import Item
from betty.prompts import get_prompts_for_item

load_dotenv()

MODEL = "gpt-3.5-turbo"


class ChatAPI:
    def __init__(self, ai_prefix, model=MODEL, *args, **kwargs):
        self.chat_args = [model, *args]
        self.chat_kwargs = kwargs
        self.chat = None
        self.ai_prefix = ai_prefix

    def _parse_response(self, output: str, obj: Type[Item]) -> list[Item]:
        parser = PydanticOutputParser(pydantic_object=obj.response_model())
        return parser.parse(output).dict()["data"]

    async def generate(self, obj: Type[Item], *args, **kwargs):
        info = {"obj_key": obj.key(), "obj_plural": obj.plural()}
        info["plural"] = "s" if kwargs.get("num", 1) > 1 else ""
        info.update(kwargs)

        chat = ChatOpenAI(**self.chat_kwargs)
        system_prompt = ChatPromptTemplate.from_messages(get_prompts_for_item(None)[0])
        memory = RoleBasedConversationBufferMemory(ai_prefix=self.ai_prefix)
        chain = ConversationChain(llm=chat, prompt=system_prompt, memory=memory)

        prompts = get_prompts_for_item(obj)
        for step in prompts:
            chat_prompt = ChatPromptTemplate.from_messages(step).format(**info)
            output = await chain.arun(input=chat_prompt, callbacks=[])
            print()

        return [obj(**item) for item in self._parse_response(output, obj)]

    async def stream(self, obj: Type[Item], *args, **kwargs):
        info = {"obj_key": obj.key(), "obj_plural": obj.plural()}
        info["plural"] = "s" if kwargs.get("num", 1) > 1 else ""
        info.update(kwargs)

        chat = ChatOpenAI(streaming=True, **self.chat_kwargs)
        system_prompt = ChatPromptTemplate.from_messages(get_prompts_for_item(None)[0])
        memory = RoleBasedConversationBufferMemory(ai_prefix=self.ai_prefix)
        chain = ConversationChain(llm=chat, prompt=system_prompt, memory=memory)

        prompts = get_prompts_for_item(obj)
        for step in prompts:
            chat_prompt = ChatPromptTemplate.from_messages(step).format(**info)
            output = await chain.arun(
                input=chat_prompt,
                callbacks=[JSONStreamingHandler(obj, lambda x: print(x))],
            )
            print()

        return [obj(**item) for item in self._parse_response(output, obj)]
