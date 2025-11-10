# decorators.py - role-based access decorator
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models import User
from extensions import db




def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({'msg': 'missing jwt identity'}), 401
            user = db.session.get(User, user_id)
            if not user:
                return jsonify({'msg': 'user not found'}), 404
            if user.role not in allowed_roles:
                return jsonify({'msg': 'forbidden - insufficient role'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator