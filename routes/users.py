# routes/users.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User, UserProfile
from decorators import role_required


users_bp = Blueprint('users', __name__)



# Get current user info
@users_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'msg': 'user not found'}), 404
    out = user.to_dict()
    out['profile'] = user.profile.to_dict() if user.profile else None
    return jsonify(out)




# Admin only: list users
@users_bp.route('/', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_users():
    users = User.query.limit(200).all()
    return jsonify([u.to_dict() for u in users])




# Get user by id - admin or the user themself
@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'user not found'}), 404


    if current_user_id != user_id:
    # not owner - allow only admin
        current_user = User.query.get(current_user_id)
    if not current_user or current_user.role != 'admin':
        return jsonify({'msg': 'forbidden'}), 403


    out = user.to_dict()
    out['profile'] = user.profile.to_dict() if user.profile else None
    return jsonify(out)




# Profile CRUD: owner only
@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    profile = UserProfile.query.filter_by(user_id=current_user_id).first()
    if not profile:
        return jsonify({'msg': 'profile not found'}), 404
    return jsonify(profile.to_dict())




@users_bp.route('/profile', methods=['POST'])
@jwt_required()
def create_profile():
    current_user_id = get_jwt_identity()
    data = request.get_json(force=True) or {}
    if UserProfile.query.filter_by(user_id=current_user_id).first():
        return jsonify({'msg': 'profile exists'}), 400
    profile = UserProfile(user_id=current_user_id, bio=data.get('bio'), age=data.get('age'), extra=data.get('extra'))
    db.session.add(profile)
    db.session.commit()
    return jsonify({'msg': 'profile updated', 'profile': profile.to_dict()})

@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    data = request.get_json(force=True) or {}
    profile = UserProfile.query.filter_by(user_id=current_user_id).first()
    if not profile:
        return jsonify({'msg': 'profile not found'}), 404
    profile.bio = data.get('bio', profile.bio)
    profile.age = data.get('age', profile.age)
    profile.extra = data.get('extra', profile.extra)
    db.session.commit()
    return jsonify({'msg': 'profile updated', 'profile': profile.to_dict()})

@users_bp.route('/profile', methods=['DELETE'])
@jwt_required()
def delete_profile():
    current_user_id = get_jwt_identity()
    profile = UserProfile.query.filter_by(user_id=current_user_id).first()
    if not profile:
        return jsonify({'msg': 'profile not found'}), 404
    db.session.delete(profile)
    db.session.commit()
    return jsonify({'msg': 'profile deleted'})