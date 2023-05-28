from __future__ import annotations

from abc import ABCMeta
from dataclasses import asdict, dataclass
import json
from typing import Any, Optional


def serialize_to_json(obj: Any) -> str:
    def _serialize(obj):
        if isinstance(obj, Item):
            return {k: _serialize(v) for k, v in asdict(obj).items()}
        elif isinstance(obj, list):
            return [_serialize(x) for x in obj]
        elif isinstance(obj, dict):
            return {k: _serialize(v) for k, v in obj.items()}
        else:
            return obj

    return json.dumps(_serialize(obj))


@dataclass
class Item(metaclass=ABCMeta):
    def __str__(self):
        return str(self.__dict__)

    def __dict__(self):
        return asdict(self)

    @classmethod
    def _base_examples(cls, num, previous: Optional[list[Item]] = None) -> list[Item]:
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

        return data

    @classmethod
    def examples(cls, num):
        return cls._base_examples(num)
