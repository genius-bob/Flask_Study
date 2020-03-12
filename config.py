from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf import CSRFProtect

app=Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY']='you-will-never-guess'
csrf = CSRFProtect(app)

app.config["SQLALCHEMY_DATABASE_URI"] = \
    'mysql+pymysql://root:Rbtc1992@localhost/dalsearch?charset=utf8'
SQLALCHEMY_COMMIT_TEARDOWN = True
db=SQLAlchemy(app)

login_manager.login_view='login'
