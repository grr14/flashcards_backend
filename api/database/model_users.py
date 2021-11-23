from api.app import db

class Users(db.Model):

    __tablename__ = "USERS"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    last_login = db.Column(db.DateTime(timezone=True),nullable=False)
    date_joined = db.Column(db.DateTime(timezone=True),nullable=False)

    def __repr__(self):
        return f"User('{self.id}','{self.username}', '{self.email}', '{self.password}', '{self.is_active}', '{self.last_login}', '{self.date_joined}')"