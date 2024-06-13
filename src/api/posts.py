from flask import Blueprint, jsonify, abort, request
from ..models import Post, User, Comment, db

bp = Blueprint('posts', __name__, url_prefix='/posts')

@bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs
def index():
    posts = Post.query.all() # ORM performs SELECT query
    result = []
    for u in posts:
        result.append(u.serialize()) # build list of Posts as dictionaries
    return jsonify(result) # return JSON response6.

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    p = Post.query.get_or_404(id)
    return jsonify(p.serialize())

@bp.route('/<int:id>/likes', methods=['GET'])
def likes(id: int):
    p = Post.query.get_or_404(id)
    result = []
    for u in p.liking_users:
        result.append(u.serialize())
    return jsonify(result)

@bp.route('/<int:id>/comments', methods=['GET'])
def comments(id: int):
    comments = Comment.query.filter(Comment.post_id == id).all()
    table = []
    for c in comments:
        table.append(c.serialize())
    return jsonify(table)

@bp.route('', methods=['POST'])
def create():
    # req body must contain user_id and content
    if 'user_id' not in request.json or 'description' not in request.json:
        return abort(400)
    # user with id of user_id must exist
    User.query.get_or_404(request.json['user_id'])
    # construct Tweet
    t = Post(
        user_id=request.json['user_id'],
        title=request.json['title'],
        description=request.json['description']
    )
    db.session.add(t) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(t.serialize())

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    # Find post with id of id
    post = Post.query.get_or_404(id)
    # user with id of user_id must exist
    
    if request.json.get('title'):
        post.title = request.json.get('title')
    if request.json.get('description'):
        post.description = request.json.get('description')

    db.session.commit() # execute CREATE statement
    return jsonify(post.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    t = Post.query.get_or_404(id)
    try:
        db.session.delete(t) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)