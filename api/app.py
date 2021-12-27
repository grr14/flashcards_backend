from flask import Flask
import os
from dotenv import load_dotenv
import api.database.model_users as users
from extensions import db, cors, migrate, guard

load_dotenv()


def register_extensions(app):
    db.init_app(app)
    cors.init_app(app)
    guard.init_app(app, users.Users)
    migrate.init_app(app, db)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DB_LINK"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "top secret"
    app.config["JWT_ACCESS_LIFESPAN"] = {"hours": 24}
    app.config["JWT_REFRESH_LIFESPAN"] = {"days": 30}

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    register_extensions(app)

    with app.app_context():
        db.create_all()

        if db.session.query(users.Users).filter_by(username="test").count() < 1:
            db.session.add(
                users.Users(
                    username="test",
                    hashed_password=guard.hash_password("password"),
                    email="test@test.fr",
                    roles="admin",
                )
            )
            db.session.commit()

    from api import api

    app.register_blueprint(api.bp)

    return app
