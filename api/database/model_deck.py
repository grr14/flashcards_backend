from extensions import db


class Deck(db.Model):

    __tablename__ = "deck"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    creator_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    theme = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=True)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)
    is_public = db.Column(db.Boolean, nullable=False, default=True)

    @property
    def identity(self):
        return self.id

    @property
    def deck_name(self):
        return self.name

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @classmethod
    def lookup(cls, name):
        return cls.query.filter_by(name=name).one_or_none()

    def __repr__(self):
        return f"Deck('{self.id}','{self.creator_id}','{self.name}','{self.theme}','{self.created_at}','{self.updated_at}','{self.is_public}')"

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
