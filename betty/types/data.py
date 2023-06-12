from dataclasses import dataclass

from . import Item


# @dataclass
# class Artist(Item):
#     artist_name: str
#     artist_style: str

#     @classmethod
#     def model(cls) -> Type[ArtistModel]:
#         return ArtistModel

#     @classmethod
#     def request_model(cls) -> Type[ArtistRequestModel]:
#         return ArtistRequestModel

#     @classmethod
#     def response_model(cls) -> Type[ItemResponseModel[ArtistModel]]:
#         return ItemResponseModel[ArtistModel]


# @dataclass
# class Author(Item):
#     author_name: str
#     author_style: str

#     @classmethod
#     def model(cls) -> Type[AuthorModel]:
#         return AuthorModel

#     @classmethod
#     def request_model(cls) -> Type[AuthorRequestModel]:
#         return AuthorRequestModel

#     @classmethod
#     def response_model(cls) -> Type[ItemResponseModel[AuthorModel]]:
#         return ItemResponseModel[AuthorModel]


@dataclass
class Idea(Item):
    idea: str
    emoji: str


# @dataclass
# class Lesson(Item):
#     lesson: str

#     @classmethod
#     def model(cls) -> Type[LessonModel]:
#         return LessonModel

#     @classmethod
#     def request_model(cls) -> Type[LessonRequestModel]:
#         return LessonRequestModel

#     @classmethod
#     def response_model(cls) -> Type[ItemResponseModel[LessonModel]]:
#         return ItemResponseModel[LessonModel]


# @dataclass
# class Section(Item):
#     content: str

#     @classmethod
#     def model(cls) -> Type[SectionModel]:
#         return SectionModel

#     @classmethod
#     def request_model(cls) -> Type[SectionRequestModel]:
#         return SectionRequestModel

#     @classmethod
#     def response_model(cls) -> Type[ItemResponseModel[SectionModel]]:
#         return ItemResponseModel[SectionModel]


# @dataclass
# class Story(Cover):
#     @classmethod
#     def model(cls) -> Type[StoryModel]:
#         return StoryModel

#     @classmethod
#     def request_model(cls) -> Type[StoryRequestModel]:
#         return StoryRequestModel

#     @classmethod
#     def response_model(cls) -> Type[ItemResponseModel[StoryModel]]:
#         return ItemResponseModel[StoryModel]

#     @classmethod
#     def create_model(cls) -> Type[StoryCreateModel]:
#         return StoryCreateModel
