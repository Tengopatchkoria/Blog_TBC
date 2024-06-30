from ext import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    subtitle = db.Column(db.String(), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.String())
    author = db.Column(db.String(), nullable=False)
    img = db.Column(db.String(), default='default_photo.png')
    user_id = db.Column(db.Integer(), nullable=False)
    likes = db.Column(db.Integer())

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    fname = db.Column(db.String(), nullable = False)
    lname = db.Column(db.String(), nullable = False)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    gmail = db.Column(db.String(), nullable = False)

    def __init__(self, fname, lname, username , password, gmail):
        self.fname = fname
        self.lname = lname
        self.username = username
        self.password = generate_password_hash(password)
        self.gmail = gmail
    
    def check_pass(self, fpass):
        return check_password_hash(self.password, fpass)

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(db.Integer(), nullable=False)
    usern = db.Column(db.String(), nullable=False)
    content = db.Column(db.Text(), nullable=False)
      

class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(db.Integer(), nullable=False)
    u_id = db.Column(db.Integer(), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)  


