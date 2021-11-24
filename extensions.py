from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_praetorian import Praetorian
from flask_cors import CORS

db = SQLAlchemy()
cors = CORS()
migrate = Migrate()
guard = Praetorian()