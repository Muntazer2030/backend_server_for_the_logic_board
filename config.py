# config.py
import os
from datetime import timedelta
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY',)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)


    # Optional: role names
    ROLE_ADMIN = 'admin'
    ROLE_USER = 'user'