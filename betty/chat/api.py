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
    """
    A class used to handle the chat API

    ...

    Attributes
    ----------
    ai_prefix : str
        a string used as the prefix for the AI
    model : str
        the model used for the AI (default is 'gpt-3.5-turbo')
    chat_args : list
        list of arguments for the chat
    chat_kwargs : dict
        dictionary of keyword arguments for the chat
    chat : ChatOpenAI
        instance of ChatOpenAI

    Methods
    -------
    _parse_response(output: str, response_model: Type[ItemResponseModel]) -> list[ItemModel]
        Parse the output from the chat
    _run_chain(item_type: Type[Item], chat: ChatOpenAI, callbacks: list[BaseCallbackHandler], *args, **kwargs) -> list[Item]
        Run a chain of conversation
    generate(item_type: Type[Item], *args, **kwargs) -> list[Item]
        Generate a list of items
    stream(item_type: Type[Item], callback_func: Callable[[Item], Coroutine[Any, Any, None]], callback_kwargs: dict[Any, Any], *args, **kwargs) -> None
        Stream a list of items
    """

    def __init__(self, ai_prefix, model=MODEL, *args, **kwargs):
        self.chat_args = [model, *args]
        self.chat_kwargs = kwargs
        self.chat = None
        self.ai_prefix = ai_prefix

    def _parse_response(
        self, output: str, response_model: Type[ItemResponseModel]
    ) -> list[ItemModel]:
        """
        Parse the output from the chat

        Parameters
        ----------
        output : str
            output string from the chat
        response_model : Type[ItemResponseModel]
            model type to parse the output into

        Returns
        -------
        list
            a list of parsed items
        """
        parser = PydanticOutputParser(pydantic_object=response_model)
        try:
            return parser.parse(output).dict()["data"]
        except OutputParserException:
            return self._parse_response(
                json.dumps(ast.literal_eval(output)), response_model
            )

    async def _run_chain(
        self,
        item_type: Type[Item],
        chat: ChatOpenAI,
        callbacks: list[BaseCallbackHandler],
        *args,
        **kwargs
    ) -> list[Item]:
        """
        Run a chain of conversation

        Parameters
        ----------
        item_type : Type[Item]
            type of the item
        chat : ChatOpenAI
            instance of ChatOpenAI
        callbacks : list[BaseCallbackHandler]
            list of callback handlers
        *args : list
            list of additional arguments
        **kwargs : dict
            dictionary of additional keyword arguments

        Returns
        -------
        list
            a list of items
        """
        obj_response: Type[ItemResponseModel] = item_type.get_response_model()

        info = {"obj_key": item_type.key(), "obj_plural": item_type.plural()}
        info["plural"] = "s" if kwargs.get("num", 1) > 1 else ""
        info.update(kwargs)

        system_prompt = ChatPromptTemplate.from_messages(get_prompts_for_item(None)[0])
        memory = RoleBasedConversationBufferMemory(ai_prefix=self.ai_prefix)
        chain = ConversationChain(llm=chat, prompt=system_prompt, memory=memory)

        prompts = get_prompts_for_item(item_type)
        for step in prompts:
            chat_prompt = ChatPromptTemplate.from_messages(step).format(**info)
            output = await chain.arun(input=chat_prompt, callbacks=callbacks)

        return [
            item_type(**item) for item in self._parse_response(output, obj_response)
        ]

    async def generate(self, item_type: Type[Item], *args, **kwargs) -> list[Item]:
        """
        Generate a list of items

        Parameters
        ----------
        item_type : Type[Item]
            type of the item
        *args : list
            list of additional arguments
        **kwargs : dict
            dictionary of additional keyword arguments

        Returns
        -------
        list
            a list of items
        """
        chat = ChatOpenAI(**self.chat_kwargs)

        return await self._run_chain(item_type, chat, [], *args, **kwargs)

    async def stream(
        self,
        item_type: Type[Item],
        callback_func: Callable[[Item], Coroutine[Any, Any, None]],
        callback_kwargs: dict[Any, Any],
        *args,
        **kwargs
    ) -> None:
        """
        Stream a list of items

        Parameters
        ----------
        item_type : Type[Item]
            type of the item
        callback_func : Callable[[Item], Coroutine[Any, Any, None]]
            callback function to call on each item
        callback_kwargs : dict[Any, Any]
            dictionary of additional keyword arguments for the callback function
        *args : list
            list of additional arguments
        **kwargs : dict
            dictionary of additional keyword arguments
        """
        chat = ChatOpenAI(streaming=True, **self.chat_kwargs)
        callbacks = [JSONStreamingHandler(item_type, callback_func, callback_kwargs)]

        await self._run_chain(item_type, chat, callbacks, *args, **kwargs)
