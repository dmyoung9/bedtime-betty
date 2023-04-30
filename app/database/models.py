from . import db


class Title(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    story_title: str = db.Column(db.String)
    __table_args__ = (
        db.UniqueConstraint("story_title", name="unique_title_constraint"),
    )


class Theme(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    emoji: str = db.Column(db.String)
    story_theme: str = db.Column(db.String)
    __table_args__ = (
        db.UniqueConstraint("emoji", "story_theme", name="unique_theme_constraint"),
    )

    def to_json(self):
        return {"id": self.id, "emoji": self.emoji, "story_theme": self.story_theme}


class Lesson(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    story_lesson: str = db.Column(db.String)
    __table_args__ = (
        db.UniqueConstraint("story_lesson", name="unique_title_constraint"),
    )


class Author(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    author_name: str = db.Column(db.String)
    author_style: str = db.Column(db.String)
    __table_args__ = (
        db.UniqueConstraint(
            "author_name", "author_style", name="unique_theme_constraint"
        ),
    )

    def to_json(self):
        return {
            "id": self.id,
            "author_name": self.author_name,
            "author_style": self.author_style,
        }


class Artist(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    artist_name: str = db.Column(db.String)
    artist_style: str = db.Column(db.String)
    __table_args__ = (
        db.UniqueConstraint(
            "artist_name", "artist_style", name="unique_theme_constraint"
        ),
    )

    def to_json(self):
        return {
            "id": self.id,
            "artist_name": self.artist_name,
            "artist_style": self.artist_style,
        }


class Story(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    age_min: int = db.Column(db.Integer)
    age_max: int = db.Column(db.Integer)
    theme_id: int = db.Column(db.Integer, db.ForeignKey("theme.id"), nullable=True)
    title_id: int = db.Column(db.Integer, db.ForeignKey("title.id"), nullable=True)
    author_id: int = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=True)
    artist_id: int = db.Column(db.Integer, db.ForeignKey("artist.id"), nullable=True)
    lesson_id: int = db.Column(db.Integer, db.ForeignKey("lesson.id"), nullable=True)

    theme = db.relationship("Theme", foreign_keys=[theme_id])
    title = db.relationship("Title", foreign_keys=[title_id])
    author = db.relationship("Author", foreign_keys=[author_id])
    artist = db.relationship("Artist", foreign_keys=[artist_id])
    lesson = db.relationship("Lesson", foreign_keys=[lesson_id])

    def to_json(self):
        if theme := self.theme.to_json() if self.theme else {}:
            theme.pop("id")
        if author := self.author.to_json() if self.author else {}:
            author.pop("id")
        if artist := self.artist.to_json() if self.artist else {}:
            artist.pop("id")

        return {
            "id": self.id,
            "age_min": self.age_min,
            "age_max": self.age_max,
            "story_title": self.title.story_title if self.title else None,
            "story_lesson": self.lesson.story_lesson if self.lesson else None,
            **theme,
            **author,
            **artist,
        }
