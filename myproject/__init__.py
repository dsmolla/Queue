import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from datetime import timedelta
from flask_mail import Mail


login_manager = LoginManager()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['REMEMBER_COOKIE_NAME'] = "queue_token"
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=31)
app.config['REMEMBER_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_REFRESH_EACH_REQUEST'] = True


db = SQLAlchemy(app)
Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.session_protection = 'strong'
login_manager.login_message = None

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_UNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PWD')
mail = Mail(app)