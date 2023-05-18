from typing import Optional
from pydantic import BaseModel

DEFAULT_NUM = 3
DEFAULT_AGE = 7


class ItemRequest(BaseModel):
    num: Optional[int] = DEFAULT_NUM
    age: Optional[int] = DEFAULT_AGE
    examples: Optional[str] = None

    class Config:
        extra = "forbid"
