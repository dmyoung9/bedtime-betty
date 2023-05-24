from __future__ import annotations

from abc import ABCMeta
from dataclasses import asdict, dataclass
import json
from typing import Optional, Union


@dataclass
class Item(metaclass=ABCMeta):
    def __str__(self):
        return str(self.__dict__)

    def __dict__(self):
        return asdict(self)

    def as_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def _base_examples(
        cls, num, previous: Optional[list[Item]] = None
    ) -> dict[str, Union[int, list[Item]]]:
        data = previous or []

        data.extend(
            [
                cls(
                    **{
                        key: f"{{{key}}} {num - idx + 1}"
                        for key in cls.__dataclass_fields__.keys()
                    }
                )
                for idx in range(num - len(data), 0, -1)
            ]
        )

        return {"total": num, "data": data}

    @classmethod
    def examples(cls, num):
        return cls._base_examples(num)
