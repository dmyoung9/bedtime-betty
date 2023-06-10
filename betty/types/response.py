from . import ItemResponseModel
from .validation import (
    ArtistModel,
    AuthorModel,
    IdeaModel,
    LessonModel,
    SectionModel,
    CoverModel,
)


class ArtistResponseModel(ItemResponseModel[ArtistModel]):
    pass


class AuthorResponseModel(ItemResponseModel[AuthorModel]):
    pass


class IdeaResponseModel(ItemResponseModel[IdeaModel]):
    pass


class LessonResponseModel(ItemResponseModel[LessonModel]):
    pass


class SectionResponseModel(ItemResponseModel[SectionModel]):
    pass


class CoverResponseModel(ItemResponseModel[CoverModel]):
    pass
