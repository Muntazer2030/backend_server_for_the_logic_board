# routes/auth.py
from flask import Blueprint, request, jsonify
from extensions import db
from models import User
from flask_jwt_extended import create_access_token


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(force=True)
    username = (data.get('username') or '').strip().lower()
    password = data.get('password')
    name = data.get('name')
    role = data.get('role') or None

    if not username or not password:
        return jsonify({'msg': 'username and password required'}), 400


    if User.query.filter_by(username=username).first():
        return jsonify({'msg': 'user already exists'}), 400


    user = User(username=username, name=name)
    user.set_password(password)


    # only allow specifying admin role if there are no users yet or via an admin endpoint
    if role:
        # simple safeguard: disallow creating admin via public register
        # If you want to allow creating admin in special cases, implement checks here
        user.role = 'user'


    db.session.add(user)
    db.session.commit()
   

    return jsonify({'msg': 'user created', 'user': user.to_dict()}), 201




@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    username = (data.get('username') or '').strip().lower()
    password = data.get('password')
    if not username or not password:
        return jsonify({'msg': 'username and password required'}), 400


    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'msg': 'invalid credentials'}), 401


    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token, 'user': user.to_dict()})