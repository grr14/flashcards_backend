from os import times
from flask import Blueprint, jsonify, request
from api.database.model_deck import Deck
from api.database.model_card import Card
from extensions import db
from datetime import datetime
import pytz

bp = Blueprint("deck", __name__, url_prefix="/deck")


@bp.route("/get/<deck_id>")
def get_deck(deck_id):
    if not deck_id:
        return {"message": "Incorrect request"}, 400
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


@bp.route("/create/<creator_id>", methods=["POST"])
def create(creator_id):
    req = request.get_json(force=True)
    name = req.get("name")
    theme = req.get("theme")
    is_public = req.get("is_public")

    print(f"name={name} theme={theme} is_public={is_public} creator_id={creator_id}")

    if creator_id is None and name is None and theme is None and not is_public is None:
        return {"message": "Incorrect request"}, 400

    timestamp = datetime.now(pytz.timezone("Europe/Paris"))

    db.session.add(
        Deck(
            name=name,
            theme=theme,
            created_at=timestamp,
            updated_at=timestamp,
            creator_id=creator_id,
            is_public=is_public,
        )
    )

    db.session.commit()
    return {"message": "Deck has been created successfully."}


@bp.route("/get_all/<user_id>", methods=["GET"])
def get_all_decks(user_id):
    if not user_id:
        return {"message": "Incorrect request"}, 400
    decks = db.session.query(Deck).filter_by(creator_id=user_id).all()

    decks = [d.as_dict() for d in decks]
    decks_id = [d["id"] for d in decks]  # for each deck we get its id
    counts = [
        db.session.query(Card).filter_by(deck_id=id).count() for id in decks_id
    ]  # for each deck we get its number of cards

    for index, deck in enumerate(decks):
        deck["nb_cards"] = counts[
            index
        ]  # we add the number of card of each deck to the response

    print(decks)

    return jsonify(count=len(decks), decks=decks)


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
