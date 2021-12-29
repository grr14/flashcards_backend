from extensions import db


class UserDecks(db.Model):

    __tablename__ = "user_decks"

    user_id = db.Column(db.Integer, nullable=False)
    deck_id = db.Column(db.Integer, nullable=False)
