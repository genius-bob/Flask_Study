from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from config import db

class BlogPost(db.Model):
    __tablename__="posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    author_id = db.Column(db.Integer, ForeignKey('users.id'))
    def __init__(self,title,description):
        self.title = title
        self.description = description

class User(db.Model):
    __tablename__= "users"
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(120), nullable=False)
    email= db.Column(db.String(144), nullable=False)
    password= db.Column(db.String(128))
    posts = relationship("BlogPost",backref="author") #reverse link to posts,like foreignkey

    def __init__(self,name,email,password):
        self.name = name
        self.email = email
        self.password = password
