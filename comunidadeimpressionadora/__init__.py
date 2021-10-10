from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
application = Flask(__name__)


application.config['SECRET_KEY'] = 'd5e68a8b99473b5d602a6527010f266b'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(application)
bcrypt = Bcrypt(application)
login_manager = LoginManager(application)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor faça login para acessar esta página.'
login_manager.login_message_category = 'alert-info'

from comunidadeimpressionadora import routes

