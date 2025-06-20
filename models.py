# models.py

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users' # Nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        """Cria um hash da senha e o armazena."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# O user_loader é movido para cá para ficar junto do modelo User.
# Ele informa ao Flask-Login como encontrar um usuário específico a partir do ID
# que é armazenado em sua sessão.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))