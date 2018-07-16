import os
import json

CLIENT_SECRETS_PATH = "/Users/david/Projects/beyond-dancing/backend/app/client_secrets.json"
CLIENT_ID = json.loads(
    open(CLIENT_SECRETS_PATH, 'r').read())['web']['client_id']

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://david:coboman@/beyond_dancing'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'