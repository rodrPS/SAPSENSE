# extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Instancia as extensões sem vincular a uma aplicação ainda
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()