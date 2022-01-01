from flask import Blueprint, jsonify, request
from extensions import db
from api.database.model_card import Card

bp = Blueprint("card", __name__, url_prefix="/card")


@bp.route("/edit/<card_id>", methods=["PUT"])
def edit(card_id):
    req = request.get_json(force=True)
    front = req.get("front", None)
    back = req.get("back", None)
    review = req.get("review", None)
    is_active = req.get("is_active", None)
    print(f"front={front} back={back} review={review} is_active={is_active}")
    if front is None and back is None and review is None and is_active is None:
        return {"message": "Incorrect request."}, 400
    card = db.session.query(Card).filter_by(id=card_id).first()

    # we only update the fields that are present in the request
    if front is not None:
        card.front = front

    if back is not None:
        card.back = back

    if review is not None:
        card.review = review

    if is_active is not None:
        card.is_active = is_active

    db.session.commit()
    return {"message": f"Card edited successfully."}, 200


@bp.route("/create/<deck_id>", methods=["POST"])
def create(deck_id):
    req = request.get_json(force=True)
    front = req.get("front")
    back = req.get("back")

    print(f"front={front} back={back}")

    if (not front and not back) or not deck_id:
        return {"message": "Incorrect request"}, 400

    db.session.add(
        Card(front=front, back=back, review=4, is_active=True, deck_id=deck_id)
    )

    db.session.commit()

    return {"message": "Card added successfully."}, 200


@bp.route("/delete/<card_id>", methods=["DELETE"])
def delete(card_id):
    if not card_id:
        return {"message": "Incorrect request"}, 400
    card = db.session.query(Card).filter_by(id=card_id).first()
    db.session.delete(card)
    db.session.commit()

    return {"message": "Card has been deleted"}, 200
