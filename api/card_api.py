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
    if not front and not back and not review and not is_active:
        return {"message": "Incorrect request."}, 400
    card = db.session.query(Card).filter_by(id=card_id).first()

    # we only update the fields that are present in the request
    if front:
        card.front = front

    if back:
        card.back = back

    if review:
        card.review = review

    if is_active:
        card.is_active = is_active

    db.session.commit()
    return {"message": f"Card edited successfully."}, 200
