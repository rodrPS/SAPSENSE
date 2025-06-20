# routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    """Redireciona para a página de login."""
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Renderiza a página de login e processa a autenticação."""
    if current_user.is_authenticated:
        return redirect(url_for('auth.home_page'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Procura o usuário no banco de dados
        user = User.query.filter_by(username=username).first()

        # Verifica se o usuário existe e se a senha está correta
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('auth.home_page'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Renderiza a página de registro e cria novos usuários."""
    if current_user.is_authenticated:
        return redirect(url_for('auth.home_page'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Verifica se o usuário já existe
        if User.query.filter_by(username=username).first():
            flash('Este nome de usuário já está em uso. Por favor, escolha outro.', 'warning')
            return redirect(url_for('auth.register'))
        
        # Cria um novo usuário
        new_user = User(username=username)
        new_user.set_password(password) # Criptografa a senha

        # Adiciona ao banco de dados
        db.session.add(new_user)
        db.session.commit()

        flash('Conta criada com sucesso! Por favor, faça o login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/home')
@login_required
def home_page():
    """Renderiza a home page, acessível apenas para usuários logados."""
    return render_template('home.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Processa o logout do usuário."""
    logout_user()
    return redirect(url_for('auth.login'))