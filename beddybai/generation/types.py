from typing import Literal, TypedDict

Role = Literal["system", "assistant", "user"]


class Message(TypedDict):
    role: Role
    content: str
