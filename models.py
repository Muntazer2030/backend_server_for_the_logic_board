from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import Text
import json
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120))
    role = db.Column(db.String(20), default="user")
    password_hash = db.Column(db.String(200))
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "role": self.role
        }


    
class JSONEncodedDict(db.TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return json.loads(value)
    
class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    #bio = db.Column(db.Text, nullable=True)
    #age = db.Column(db.Integer, nullable=True)
    extra = db.Column(JSONEncodedDict)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


    def to_dict(self):
        return {
        'id': self.id,
        'user_id': self.user_id,
        #'bio': self.bio,
        #'age': self.age,
        'extra': self.extra,
        'updated_at': None if not self.updated_at else self.updated_at.isoformat()
        }