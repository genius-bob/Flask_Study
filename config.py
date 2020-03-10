from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = \
    'mysql+pymysql://root:Rbtc1992@localhost/dalsearch?charset=utf8'
SQLALCHEMY_COMMIT_TEARDOWN = True
db=SQLAlchemy(app)


