from datetime import datetime
from time import sleep

from flask import Blueprint, jsonify, request

from api.database.model_users import Users
from extensions import guard, db

from flask_praetorian import auth_required, current_user
import pytz

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/time')
def time():
    sleep(0.25)
    return jsonify(now=datetime.now().replace(microsecond=0).isoformat())


@bp.route('/greet/<name>')
def greeting(name):
    sleep(0.25)
    user = Users.query.filter_by(username=name).first()
    print(user)
    return jsonify(id=user.id,username=user.username,email=user.email,password=user.password,is_active=user.is_active,last_login=user.last_login,date_joined=user.date_joined,roles=user.roles)

@bp.route('/login', methods=['POST'])
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
    username = req.get('username', None)
    password = req.get('password', None)
    print(username,password)
    user = guard.authenticate(username, password)
    print("user=",user)
    ret = {'access_token': guard.encode_jwt_token(user)}
    print("ret=",ret)
    return (jsonify(ret), 200)

@bp.route('/refresh', methods=['POST'])
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
    new_token = guard.refresh_jwt_token(old_token)
    ret = {'access_token': new_token}
    return ret, 200
  
@bp.route('/register', methods=['GET','POST'])
def register():

    username, email, password = request.get_json(force=True).values()
    print(f'username={username} email={email} password={password}')

    # check no missing fields
    if not username or not password or not email:
        ret = {'message':'incorrect request'}
        return ret, 400
    else:
        # check the user is not already in db
        if db.session.query(Users).filter_by(username=username).count() > 0:
            return {'message':'user already exists'}
        # add the user to the db
        else:
            timestamp = datetime.now(pytz.timezone('Europe/Paris'))
            db.session.add(Users(
                username=username,
                email=email,
                hashed_password=guard.hash_password(password),
                is_active=True,
                last_login=timestamp,
                date_joined=timestamp,
                roles='user'
            ))
            db.session.commit()

            return {'message':'user registered successfully'}, 200


@bp.route('/protected')
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
    return {'message': f'protected endpoint (allowed user {current_user().username})'}