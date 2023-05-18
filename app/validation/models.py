from betty.types import Item


class ItemModel(Item):
    pass


class IdeaModel(Item):
    idea: str
    emoji: str
