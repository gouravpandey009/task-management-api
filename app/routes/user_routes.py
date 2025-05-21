from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from app.utils.auth import require_api_key

user_bp = Blueprint('user_bp', __name__, url_prefix='/users')


# POST /users - Create a user
@user_bp.route('', methods=['POST'])
@require_api_key
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({'error': 'Name and email are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 409

    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully', 'user': new_user.to_dict()}), 201


# GET /users/:id - Get user by ID
@user_bp.route('/<int:user_id>', methods=['GET'])
@require_api_key
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200

# GET /users - List all users
@user_bp.route('', methods=['GET'])
@require_api_key
def list_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

