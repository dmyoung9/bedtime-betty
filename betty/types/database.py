from __future__ import annotations

from sqlalchemy.orm import Mapped

from ..database import db


class Items(db.Model):
    __abstract__ = True

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)


class Sections(Items):
    content: Mapped[str] = db.Column(db.String, unique=True)
    story_id: Mapped[int] = db.Column(db.ForeignKey("stories.id"))


class Stories(Items):
    age: Mapped[int] = db.Column(db.Integer)
    author: Mapped[str] = db.Column(db.String)
    title: Mapped[str] = db.Column(db.String, unique=True)
    emoji: Mapped[str] = db.Column(db.String, unique=True)
    outline: Mapped[str] = db.Column(db.String, unique=True)
    lesson: Mapped[str] = db.Column(db.String)

    sections: Mapped[list[Sections]] = db.relationship()
