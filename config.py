import os
from dotenv import load_dotenv
import secrets
load_dotenv(".env")


CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
API_URL = os.environ.get('API_URL')


if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("CLIENT_ID and CLIENT_SECRET must be set as environment variables.")


'''SQLAlchemy configuration'''
SQLALCHEMY_DATABASE_URI = "sqlite:///movies.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False


'''JWT configuration'''
JWT_SECRET_KEY = str(secrets.SystemRandom().getrandbits(128))
