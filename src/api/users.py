from flask import Blueprint, jsonify, abort, request
from ..models import Post, User, Comment, db, posts_likes_table, comments_likes_table
import sqlalchemy

import hashlib
import secrets

def scramble(password: str):
    #Hash and salt the given password
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs
def index():
    users = User.query.all() # ORM performs SELECT query
    result = []
    for u in users:
        result.append(u.serialize()) # build list of users as dictionaries
    return jsonify(result) # return JSON response6.

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    t = User.query.get_or_404(id)
    return jsonify(t.serialize())

@bp.route('/<int:id>/comments', methods=['GET'])
def comments(id: int):
    comments = Comment.query.filter(Comment.user_id == id).all()
    result = []
    for c in comments:
        result.append(c.serialize()) # build list of comments as dictionaries
    return jsonify(result) # return JSON response6.

@bp.route('/<int:id>/posts', methods=['GET'])
def posts(id: int):
    posts = Post.query.filter(Post.user_id == id).all()
    result = []
    for p in posts:
        result.append(p.serialize()) # build list of posts as dictionaries
    return jsonify(result) # return JSON response6.

@bp.route('/<int:id>/likes/posts', methods=['POST'])
def post_like(id: int):
    u = User.query.get_or_404(id)
    p = Post.query.get_or_404(request.json['post_id'])
    stmt = sqlalchemy.insert(posts_likes_table).values(user_id=id, post_id=request.json['post_id'])
    try:
        db.session.execute(stmt)
        db.session.commit()
        return jsonify(True)
    except:
        db.session.rollback()
        return jsonify(False)
    
@bp.route('/<int:id>/unlike/posts', methods=['DELETE'])
def unlike_post(id: int):
    u = User.query.get_or_404(id)
    p = Post.query.get_or_404(request.json['post_id'])
    stmt = sqlalchemy.delete(posts_likes_table).where(posts_likes_table.c.user_id == id).where(posts_likes_table.c.post_id == request.json['post_id'])
    try:
        db.session.execute(stmt)
        db.session.commit()
        return jsonify(True)
    except:
        db.session.rollback()
        return jsonify(False)
    
@bp.route('/<int:id>/likes/comments', methods=['POST'])
def comment_like(id: int):
    u = User.query.get_or_404(id)
    c = Comment.query.get_or_404(request.json['comment_id'])
    stmt = sqlalchemy.insert(comments_likes_table).values(user_id=id, comment_id=request.json['comment_id'])
    try:
        db.session.execute(stmt)
        db.session.commit()
        return jsonify(True)
    except:
        db.session.rollback()
        return jsonify(False)
    
@bp.route('/<int:id>/unlike/comments', methods=['DELETE'])
def unlike_comment(id: int):
    u = User.query.get_or_404(id)
    c = Comment.query.get_or_404(request.json['comment_id'])
    stmt = sqlalchemy.delete(comments_likes_table).where(comments_likes_table.c.user_id == id).where(comments_likes_table.c.comment_id == request.json['comment_id'])
    try:
        db.session.execute(stmt)
        db.session.commit()
        return jsonify(True)
    except:
        db.session.rollback()
        return jsonify(False)


@bp.route('', methods=['POST'])
def create():
    # req body must contain username and password
    if 'username' not in request.json or 'password' not in request.json:
        return abort(400)
    # user with id of user_id must exist
    # construct Tweet
    t = User(
        username=request.json['username'],
        name=request.json['name'],
        password=scramble(request.json['password'])
    )
    db.session.add(t) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(t.serialize())

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):

    #Find the user
    user = User.query.get_or_404(id)
    
    if request.json.get('username'):
        user.username = request.json.get('username')
    if request.json.get('password'):
        user.password = scramble(request.json.get('password'))
    if request.json.get('name'):
        user.name = request.json.get('name')

    db.session.commit() # execute CREATE statement
    return jsonify(user.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    t = User.query.get_or_404(id)
    try:
        db.session.delete(t) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)