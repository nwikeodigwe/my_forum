import datetime
from flask_sqlalchemy import SQLAlchemy # type: ignore

db = SQLAlchemy()

# Association tables for likes
posts_likes_table = db.Table(
    'post_likes',
    db.Column(
        'user_id', db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),
    db.Column(
        'post_id', db.Integer,
        db.ForeignKey('posts.id'),
        primary_key=True
    ),
    db.Column(
        'created_at', db.DateTime,
        default=datetime.datetime.now(datetime.UTC),
        nullable=False
    )
)

comments_likes_table = db.Table(
    'comment_likes',
    db.Column(
        'user_id', db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),
    db.Column(
        'comment_id', db.Integer,
        db.ForeignKey('comments.id'),
        primary_key=True
    ),
    db.Column(
        'created_at', db.DateTime,
        default=datetime.datetime.now(datetime.UTC),
        nullable=False
    )
)

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    image_url = db.Column(db.String(280), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.now(datetime.UTC),
        nullable=False
    )

    def __init__(self, user_id: int, post_id: int, image_url: str):
        self.user_id = user_id
        self.post_id = post_id
        self.image_url = image_url

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat()
        }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=True)
    password = db.Column(db.String(128), nullable=False)
    posts = db.relationship('Post', backref='user', cascade="all,delete")
    comments = db.relationship('Comment', backref='user', cascade="all,delete")
    images = db.relationship('Image', backref='user', cascade="all,delete")

    def __init__(self, username: str, name: str, password: str):
        self.username = username
        self.name = name
        self.password = password

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
        }

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(280), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.now(datetime.UTC),
        nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    liking_users = db.relationship(
        'User', secondary=comments_likes_table,
        lazy='subquery',
        backref=db.backref('liked_comments', lazy=True)
    )

    def __init__(self, description: str, user_id: int, post_id: int):
        self.description = description
        self.user_id = user_id
        self.post_id = post_id
        self.created_at = datetime.datetime.now(datetime.UTC)

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id,
            'post_id': self.post_id
        }

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=True, default='Untitled')
    description = db.Column(db.String(280), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.now(datetime.UTC),
        nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', cascade="all,delete")
    images = db.relationship('Image', backref='post', cascade="all,delete")
    liking_users = db.relationship(
        'User', secondary=posts_likes_table,
        lazy='subquery',
        backref=db.backref('liked_posts', lazy=True)
    )

    def __init__(self, title: str, description: str, user_id: int):
        self.title = title
        self.description = description
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id
        }
