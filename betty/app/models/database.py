from __future__ import annotations

from sqlalchemy.orm import Mapped

from .. import db


class Items(db.Model):
    __abstract__ = True

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)


class People(Items):
    name: Mapped[str] = db.Column(db.String, unique=True)
    style: Mapped[str] = db.Column(db.String, unique=True)


class Artists(People):
    pass


class Authors(People):
    pass


class Descriptions(Items):
    description: Mapped[str] = db.Column(db.String, unique=True)


class Images(Items):
    url: Mapped[str] = db.Column(db.String, unique=True)
    page_id: Mapped[int] = db.Column(db.ForeignKey("pages.id"))
    page: Mapped[Pages] = db.relationship(back_populates="image")


class Ideas(Items):
    idea: Mapped[str] = db.Column(db.String, unique=True)


class Lessons(Items):
    lesson: Mapped[str] = db.Column(db.String, unique=True)


class Pages(Items):
    number: Mapped[int] = db.Column(db.Integer, unique=True)
    content: Mapped[str] = db.Column(db.String, unique=True)
    image: Mapped[Images] = db.relationship(back_populates="page")
    story_id: Mapped[int] = db.Column(db.ForeignKey("stories.id"))


class Stories(Items):
    age: Mapped[int] = db.Column(db.Integer)
    idea_id: Mapped[int] = db.Column(db.ForeignKey("ideas.id"))
    title_id: Mapped[int] = db.Column(db.ForeignKey("titles.id"))
    author_id: Mapped[int] = db.Column(db.ForeignKey("authors.id"))
    artist_id: Mapped[int] = db.Column(db.ForeignKey("artists.id"))
    lesson_id: Mapped[int] = db.Column(db.ForeignKey("lessons.id"))

    idea: Mapped[Ideas] = db.relationship()
    title: Mapped[Titles] = db.relationship()
    author: Mapped[Authors] = db.relationship()
    artist: Mapped[Artists] = db.relationship()
    lesson: Mapped[Lessons] = db.relationship()
    pages: Mapped[list[Pages]] = db.relationship()


class Titles(Items):
    title: Mapped[str] = db.Column(db.String, unique=True)
