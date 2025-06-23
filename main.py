# main.py

from flask import Flask
from config import Config
from extensions import db, migrate, login_manager, mail
from routes import auth_bp
import models # Apenas importe o módulo para que o SQLAlchemy reconheça os modelos

def create_app():
    """Cria e configura uma instância da aplicação Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # --- Inicializa as extensões com a aplicação ---
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    # Define a view de login para o LoginManager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Por favor, faça o login para acessar esta página."
    login_manager.login_message_category = "info"

    # O DECORADOR @login_manager.user_loader NÃO FICA MAIS AQUI.
    # Ele foi movido para o arquivo models.py.

    # Registra o Blueprint
    app.register_blueprint(auth_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
