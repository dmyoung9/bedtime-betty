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


# class StoryRequestModel(ItemRequestModel[StoryModel]):
#     id: int


# class StoryCreateModel(ItemCreateModel[StoryModel]):
#     sections: list[SectionModel] = []
