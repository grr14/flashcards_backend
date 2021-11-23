from datetime import datetime
from time import sleep

from flask import Blueprint, jsonify

from api.database.model_users import Users

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
    return jsonify(id=user.id,username=user.username,email=user.email,password=user.password,is_active=user.is_active,last_login=user.last_login,date_joined=user.date_joined)