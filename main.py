# main.py

from flask import Flask
from flask_login import LoginManager
from routes import auth_bp
from models import find_user_by_id

def create_app():
    """Cria e configura uma instância da aplicação Flask."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-segura'

    # --- Configuração do Flask-Login ---
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Define a view para a qual usuários não logados são redirecionados.
    # 'auth.home' é o nome da função da nossa rota de login ('/').
    login_manager.login_view = 'auth.home'
    
    # Mensagem customizada para o redirecionamento
    login_manager.login_message = "Por favor, faça o login para acessar esta página."
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        """
        Esta função é usada pelo Flask-Login para carregar um usuário
        a partir do ID armazenado na sessão.
        """
        return find_user_by_id(user_id)

    # Registra o Blueprint na aplicação
    app.register_blueprint(auth_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)