from flask import Blueprint, jsonify
from api.database.model_deck import Deck
from api.database.model_card import Card
from extensions import db

bp = Blueprint("deck", __name__, url_prefix="/deck")


@bp.route("/get/<deck_id>")
def get_deck(deck_id):
    deck = db.session.query(Deck).filter_by(id=deck_id).first()
    cards = db.session.query(Card).filter_by(deck_id=deck_id).all()
    # print(deck)
    print(cards)
    return jsonify(
        id=deck.id,
        creator_id=deck.creator_id,
        name=deck.name,
        theme=deck.theme,
        created_at=deck.created_at,
        updated_at=deck.updated_at,
        is_public=deck.is_public,
        cards=[c.as_dict() for c in cards],
    )


@bp.route("/get_all/<user_id>", methods=["GET"])
def get_all_decks(user_id):
    if not user_id:
        return {"message": "Incorrect request"}
    decks = db.session.query(Deck).filter_by(creator_id=user_id).all()
    print(decks)
    return jsonify(count=len(decks), decks=[d.as_dict() for d in decks])


@bp.route("/delete/<deck_id>", methods=["DELETE"])
def delete(deck_id):
    if not deck_id:
        return {"message": "Incorrect message"}, 400

    deck = db.session.query(Deck).filter_by(id=deck_id).first()
    db.session.delete(deck)

    cards = db.session.query(Card).filter_by(deck_id=deck_id).delete()
    db.session.commit()
    print(f"cards={cards}")
    return {"message": "Deck has been deleted successfully"}
