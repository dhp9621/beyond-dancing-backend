import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))
CLIENT_SECRETS_PATH = os.path.join(basedir, "client_secrets.json")
CLIENT_ID = json.loads(
    open(CLIENT_SECRETS_PATH, 'r').read())['web']['client_id']

BASE_S3_URL = 'https://s3.us-east-2.amazonaws.com'
VIDEO_BUCKET = 'bdvideobucket'
THUMBNAIL_BUCKET = 'bdthumbnail'

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://david:coboman@/beyond_dancing'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')