from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_security import SQLAlchemyUserDatastore, Security
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# login = LoginManager(app)
# login.login_view = 'parent_login'
# login.login_message = 'Please log in to access this page.'
mail = Mail(app)
bootstrap = Bootstrap(app)

from app.models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from app import admin, models, parent
