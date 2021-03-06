from datetime import datetime
from os import error
from time import sleep

from flask import Blueprint, jsonify, request
from flask_praetorian.exceptions import AuthenticationError, PraetorianError

from api.database.model_user import User
from extensions import guard, db

from flask_praetorian import auth_required, current_user
import pytz

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/time")
def time():
    sleep(0.25)
    return jsonify(now=datetime.now().replace(microsecond=0).isoformat())


@bp.route("/greet/<name>")
def greeting(name):
    sleep(0.25)
    user = User.query.filter_by(username=name).first()
    print(user)
    return jsonify(
        id=user.id,
        username=user.username,
        email=user.email,
        password=user.password,
        is_active=user.is_active,
        last_login=user.last_login,
        date_joined=user.date_joined,
        roles=user.roles,
    )


@bp.route("/login", methods=["POST"])
def login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.
    .. example::
       $ curl http://localhost:5000/api/login -X POST \
         -d '{"username":"Yasoob","password":"strongpassword"}'
    """
    req = request.get_json(force=True)
    print("req=", req)
    username = req.get("username", None)
    password = req.get("password", None)
    print(username, password)
    try:
        user = guard.authenticate(username, password)
        print("user=", user)
    except AuthenticationError as error:
        print(f"message={error.message} code={error.status_code}")
        return {"message": error.message}, error.status_code
    else:
        ret = {"access_token": guard.encode_jwt_token(user)}
        user = db.session.query(User).filter_by(username=username).first()
        user.last_login = datetime.now(pytz.timezone("Europe/Paris"))
        db.session.commit()
        print("ret=", ret)
        return (jsonify(ret), 200)


@bp.route("/refresh", methods=["POST"])
def refresh():
    """
    Refreshes an existing JWT by creating a new one that is a copy of the old
    except that it has a refrehsed access expiration.
    .. example::
       $ curl http://localhost:5000/api/refresh -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    print("refresh request")
    old_token = request.get_data()
    print(request)
    print(f"old_token = {old_token}")
    if old_token is None:
        print(f"Refresh token was not sent.")
    try:
        new_token = guard.refresh_jwt_token(old_token)
    except PraetorianError as err:
        print(f"error = {err}")
        return
    else:
        print(f"new token={new_token}")
        ret = {"access_token": new_token}
        return ret, 200


@bp.route("/register", methods=["GET", "POST"])
def register():

    username, email, password = request.get_json(force=True).values()
    print(f"username={username} email={email} password={password}")

    # check no missing fields
    if not username or not password or not email:
        return {"message": "Incorrect request"}, 400
    else:
        # check the user is not already in db
        if db.session.query(User).filter_by(username=username).count() > 0:
            return {"message": "Username is taken."}, 400
        elif db.session.query(User).filter_by(email=email).count() > 0:
            return {"message": "Email is already used."}, 400
        # add the user to the db
        else:
            timestamp = datetime.now(pytz.timezone("Europe/Paris"))
            db.session.add(
                User(
                    username=username,
                    email=email,
                    hashed_password=guard.hash_password(password),
                    is_active=True,
                    last_login=timestamp,
                    date_joined=timestamp,
                    roles="user",
                )
            )
            db.session.commit()

            return {"message": "User registered successfully."}, 200


@bp.route("/change-email", methods=["PUT"])
def change_email():
    username, newEmail, newEmailConfirmation = request.get_json(force=True).values()
    print(
        f"username={username} newEmail={newEmail} newEmailConfirmation={newEmailConfirmation}"
    )
    if not username or not newEmail or not newEmailConfirmation:
        return {"message": "Incorrect request"}, 400

    # pick user, change mail
    user = db.session.query(User).filter_by(username=username).first()
    user.email = newEmail
    db.session.commit()
    return {"message": f"Email changed successfully to {newEmail}."}, 200


@bp.route("/change-password", methods=["PUT"])
def change_password():
    username, oldPassword, newPassword, newPasswordConfirmation = request.get_json(
        force=True
    ).values()
    print(
        f"username={username} oldPassword={oldPassword} newPassword={newPassword} newPasswordConfirmation={newPasswordConfirmation}"
    )
    if (
        not username
        or not oldPassword
        or not newPassword
        or not newPasswordConfirmation
    ):
        return {"message": "Incorrect request"}, 400

    # check the oldPassword and newPassword are different
    if oldPassword == newPassword:
        return {"message": "New and old passwords must be different."}, 400
    # get the user
    user = db.session.query(User).filter_by(username=username).first()

    # check the old password
    try:
        guard.authenticate(username, oldPassword)
    except AuthenticationError:  # no match: reject
        return {"message": "Incorrect password."}, 400
    else:  # match: update the password
        user.hashed_password = guard.hash_password(newPassword)
        db.session.commit()
        return {"message": "Password has been changed."}, 200


# passing the username in body doesn't seem to word for DELETE method
@bp.route("/delete-account/<username>", methods=["DELETE"])
def delete_account(username):
    print(f"username={username}")
    if not username:
        return {"message": "Incorrect request"}, 400
    # delete the user
    user = db.session.query(User).filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    return {"message": "Account has been deleted"}, 200


@bp.route("/protected")
@auth_required
def protected():
    """
    A protected endpoint. The auth_required decorator will require a header
    containing a valid JWT
    .. example::
       $ curl http://localhost:5000/api/protected -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    print("protected")
    return {"message": f"protected endpoint (allowed user {current_user().username})"}


@bp.route("/me")
@auth_required
def me():
    print(current_user())
    user = current_user()
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "last_login": user.last_login,
        "date_joined": user.date_joined,
        "roles": user.roles,
        "biography": user.biography,
    }, 200


@bp.route("/biography", methods=["PUT"])
def edit_biography():
    username, biography = request.get_json(force=True).values()
    if not username or not biography:
        return {"message": "Incorrect request"}, 200
    print(f"username={username} biography={biography[0:25]}")
    user = db.session.query(User).filter_by(username=username).first()
    user.biography = biography
    db.session.commit()
    return {"message": "Biography changed with success."}, 200
