from flask import Blueprint, jsonify
from api.database.model_deck import Deck

bp = Blueprint("deck", __name__, url_prefix="/deck")


@bp.route("/get/<deck_id>")
def get_deck(deck_id):
    deck = Deck.query.filter_by(id=deck_id).first()
    print(deck)
    return jsonify(
        id=deck.id,
        creator_id=deck.creator_id,
        name=deck.name,
        theme=deck.theme,
        created_at=deck.created_at,
        updated_at=deck.updated_at,
        is_public=deck.is_public,
    )


@bp.route("/get_all/<user_id>", methods=["GET"])
def get_all_decks(user_id):
    decks = Deck.query.filter_by(creator_id=user_id).all()
    print(decks)
    return {"count": len(decks), "decks": [d.as_dict() for d in decks]}, 200
