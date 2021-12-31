from flask import Blueprint, jsonify
from api.database.model_deck import Deck
from api.database.model_card import Card

bp = Blueprint("deck", __name__, url_prefix="/deck")


@bp.route("/get/<deck_id>")
def get_deck(deck_id):
    deck = Deck.query.filter_by(id=deck_id).first()
    cards = Card.query.filter_by(deck_id=deck_id).all()
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
    decks = Deck.query.filter_by(creator_id=user_id).all()
    print(decks)
    return jsonify(count=len(decks), decks=[d.as_dict() for d in decks])
