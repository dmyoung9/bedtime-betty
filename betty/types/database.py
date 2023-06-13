from __future__ import annotations

from sqlalchemy.orm import Mapped

from ..database import db


class Items(db.Model):
    __abstract__ = True

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)


# class Images(Items):
#     url: Mapped[str] = db.Column(db.String, unique=True)
#     page_id: Mapped[int] = db.Column(db.ForeignKey("pages.id"))
#     page: Mapped[Sections] = db.relationship(back_populates="image")


class Sections(Items):
    content: Mapped[str] = db.Column(db.String, unique=True)
    # image: Mapped[Images] = db.relationship(back_populates="page")
    story_id: Mapped[int] = db.Column(db.ForeignKey("stories.id"))


class Stories(Items):
    age: Mapped[int] = db.Column(db.Integer)
    author: Mapped[str] = db.Column(db.String)
    title: Mapped[str] = db.Column(db.String, unique=True)
    emoji: Mapped[str] = db.Column(db.String, unique=True)
    outline: Mapped[str] = db.Column(db.String, unique=True)
    lesson: Mapped[str] = db.Column(db.String)

    sections: Mapped[list[Sections]] = db.relationship()
