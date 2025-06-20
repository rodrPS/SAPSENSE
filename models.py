# models.py

from flask_login import UserMixin

# Nossa classe User agora herda de UserMixin para ser compatível com o Flask-Login
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    # Flask-Login usa o método get_id(), que UserMixin já implementa
    # usando o atributo 'id' que definimos.

    def __repr__(self):
        return f'<User: {self.username}>'

# Simulação de um banco de dados de usuários
# Em um projeto real, isso viria de um banco de dados
users_db = {
    "1": User(id="1", username='admin', password='senha123'),
    "2": User(id="2", username='saps', password='sense')
}

def find_user_by_username(username):
    """Função auxiliar para encontrar um usuário pelo nome."""
    for user in users_db.values():
        if user.username == username:
            return user
    return None

def find_user_by_id(user_id):
    """Função auxiliar para encontrar um usuário pelo ID."""
    return users_db.get(user_id)