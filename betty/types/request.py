# class ArtistRequestModel(ItemRequestModel[ArtistModel]):
#     num: int
#     age: int


# class AuthorRequestModel(ItemRequestModel[AuthorModel]):
#     num: int
#     age: int


# class LessonRequestModel(ItemRequestModel[LessonModel]):
#     num: int
#     age: int


# class SectionRequestModel(ItemRequestModel[SectionModel]):
#     age: int
#     cover: CoverModel


# class CoverRequestModel(ItemRequestModel[CoverModel]):
#     num: int
#     age: int


# class StoryRequestModel(ItemRequestModel[StoryModel]):
#     id: int


# class StoryCreateModel(ItemCreateModel[StoryModel]):
#     sections: list[SectionModel] = []
