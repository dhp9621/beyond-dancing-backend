from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import url_for

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models, routes