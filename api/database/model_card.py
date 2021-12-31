from sqlalchemy.orm import backref
from extensions import db


class Card(db.Model):

    __tablename__ = "card"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    front = db.Column(db.String(150), nullable=True)
    back = db.Column(db.String(150), nullable=True)
    review = db.Column(db.Integer, nullable=True)
    is_active = db.Column(db.Boolean, nullable=True, default=True)
    deck_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Card('{self.id}','{self.deck_id}','{self.front}','{self.back}','{self.review}','{self.is_active}')"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
