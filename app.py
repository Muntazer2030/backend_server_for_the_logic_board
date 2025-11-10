# app.py - application factory
import os
from flask import Flask
from extensions import db, jwt
from config import Config
from routes.auth import auth_bp
from routes.users import users_bp




def create_app(config_object: str = None):
    app = Flask(__name__)
    app.config.from_object(config_object or Config)


    # initialize extensions
    db.init_app(app)
    jwt.init_app(app)


    # register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')


    @app.route('/')
    def index():
        return {'msg': 'API is running'}

    

       
        
    with app.app_context():
        #db.drop_all()
        #db.create_all()
        
        print("Creating database tables...")
        
        # create tables for demo (use migrations in prod)
        db.create_all()


    return app