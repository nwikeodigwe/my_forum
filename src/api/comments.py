from flask import Blueprint, jsonify, abort, request
from ..models import User, Comment, db

bp = Blueprint('comments', __name__, url_prefix='/comments')

@bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs
def index():
    comments = Comment.query.all() # ORM performs SELECT query
    result = [c.serialize() for c in comments]
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    c = Comment.query.get_or_404(id)
    return jsonify(c.serialize())

@bp.route('/<int:id>/likes', methods=['GET'])
def likes(id: int):
    c = Comment.query.get_or_404(id)
    result = []
    for u in c.liking_users:
        result.append(u.serialize())
    return jsonify(result)

@bp.route('', methods=['POST'])
def create():
    # req body must contain user_id and content
    if 'user_id' not in request.json or 'post_id' not in request.json or 'description' not in request.json:
        return abort(400)
    # user with id of user_id must exist
    User.query.get_or_404(request.json['user_id'])
    # construct Tweet
    c = Comment(
        user_id=request.json['user_id'],
        post_id=request.json['post_id'],
        description=request.json['description']
    )
    db.session.add(c) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(c.serialize())

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    # user with id of user_id must exist
    comment = Comment.query.get_or_404(id)

    if request.json.get('description'):
        comment.description = request.json.get('description')
    db.session.commit() # execute statement
    return jsonify(comment.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    t = Comment.query.get_or_404(id)
    try:
        db.session.delete(t) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)

