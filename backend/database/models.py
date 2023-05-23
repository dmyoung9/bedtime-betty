from sqlalchemy import UniqueConstraint
from sqlalchemy.inspection import inspect

from . import db


from sqlalchemy.orm import class_mapper, ColumnProperty

def to_dict(obj, visited=None):
    if visited is None:
        visited = set()
    
    columns = {c.key: getattr(obj, c.key) for c in class_mapper(obj.__class__).iterate_properties
               if type(c) == ColumnProperty}

    relationships = {}
    for name, relation in class_mapper(obj.__class__).relationships.items():
        if relation.key not in visited:
            visited.add(relation.key)
            related_obj = getattr(obj, name)
            if related_obj is not None:
                if relation.uselist:
                    relationships[name] = [to_dict(child, visited) for child in related_obj]
                else:
                    relationships[name] = to_dict(related_obj, visited)

    return {**columns, **relationships}

class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class Title(db.Model, Serializer):
    __tablename__ = "titles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)


class Idea(db.Model, Serializer):
    __tablename__ = "ideas"

    id = db.Column(db.Integer, primary_key=True)
    emoji = db.Column(db.String)
    idea = db.Column(db.String)

    __table_args__ = (UniqueConstraint("emoji", "idea", name="unique_idea_constraint"),)


class Lesson(db.Model, Serializer):
    __tablename__ = "lessons"

    id = db.Column(db.Integer, primary_key=True)
    lesson = db.Column(db.String, unique=True)


class Author(db.Model, Serializer):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String)
    author_style = db.Column(db.String)

    __table_args__ = (
        UniqueConstraint(
            "author_name", "author_style", name="unique_author_constraint"
        ),
    )


class Artist(db.Model, Serializer):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String)
    artist_style = db.Column(db.String)

    __table_args__ = (
        UniqueConstraint(
            "artist_name", "artist_style", name="unique_artist_constraint"
        ),
    )


class Story(db.Model, Serializer):
    __tablename__ = "stories"

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    idea_id = db.Column(db.Integer, db.ForeignKey("ideas.id"), nullable=True)
    title_id = db.Column(db.Integer, db.ForeignKey("titles.id"), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=True)

    idea = db.relationship("Idea", foreign_keys=[idea_id])
    title = db.relationship("Title", foreign_keys=[title_id])
    author = db.relationship("Author", foreign_keys=[author_id])
    artist = db.relationship("Artist", foreign_keys=[artist_id])
    lesson = db.relationship("Lesson", foreign_keys=[lesson_id])
    pages = db.relationship("Page", back_populates="story")

    def serialize(self):
        return {
            "id": self.id,
            "age": self.age,
            "idea_id": self.idea_id,
            "lesson_id": self.lesson_id,
            "artist_id": self.artist_id,
            "author_id": self.author_id,
            "title_id": self.title_id,
            "pages": self.pages,
        }


class Page(db.Model, Serializer):
    __tablename__ = "pages"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    total = db.Column(db.Integer)
    content = db.Column(db.String)
    image = db.Column(db.String, nullable=True)
    story_id = db.Column(db.Integer, db.ForeignKey("stories.id"))

    story = db.relationship("Story", back_populates="pages")

    def serialize(self):
        return {
            "id": self.id,
            "number": self.number,
            "total": self.total,
            "content": self.content,
            "image": self.image,
            "story_id": self.story_id,
        }
