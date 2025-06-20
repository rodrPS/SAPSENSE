# routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import find_user_by_username

auth_bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

@auth_bp.route('/')
def home():
    """Renderiza a página de login."""
    # Se o usuário já estiver logado, redireciona para a home page
    if current_user.is_authenticated:
        return redirect(url_for('auth.home_page'))
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    """Processa a tentativa de login."""
    username = request.form.get('username')
    password = request.form.get('password')
    user = find_user_by_username(username)

    if user and user.password == password:
        # A função login_user registra o usuário como logado
        login_user(user)
        flash('Login realizado com sucesso!', 'success')
        # Redireciona para a nova rota '/home'
        return redirect(url_for('auth.home_page'))
    else:
        flash('Usuário ou senha inválidos.', 'danger')
        return redirect(url_for('auth.home'))

# --- Novas Rotas ---

@auth_bp.route('/home')
@login_required # Este decorador protege a rota
def home_page():
    """Renderiza a home page, acessível apenas para usuários logados."""
    return render_template('home.html')

@auth_bp.route('/logout')
@login_required # Usuário precisa estar logado para deslogar
def logout():
    """Processa o logout do usuário."""
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('auth.home'))