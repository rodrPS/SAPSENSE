# routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from formSaps import Step1Form, Step2Form, Step3Form, Step4Form
from datetime import datetime

from models import User, Paciente, Internacao
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

    return render_template('login/index.html')

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

    return render_template('register/index.html')


@auth_bp.route('/home')
@login_required
def home_page():
    """Renderiza a home page, acessível apenas para usuários logados."""
    return render_template('home/index.html')

@auth_bp.route('/saps-form', methods=['GET', 'POST'])
@login_required
def saps_form():
    step = int(request.args.get('step', 1))

    if step == 1:
        form = Step1Form()
        if form.validate_on_submit():
            session['step1'] = form.data
            return redirect(url_for('auth.saps_form', step=2))
        return render_template('sapsForm/step1.html', form=form)

    elif step == 2:
        form = Step2Form()
        if form.validate_on_submit():
            session['step2'] = form.data
            return redirect(url_for('auth.saps_form', step=3))
        return render_template('sapsForm/step2.html', form=form)

    elif step == 3:
        form = Step3Form()
        if form.validate_on_submit():
            session['step3'] = form.data
            return redirect(url_for('auth.saps_form', step=4))
        return render_template('sapsForm/step3.html', form=form)

    elif step == 4:
        form = Step4Form()
        if form.validate_on_submit():
            session['step4'] = form.data
            return redirect(url_for('auth.resumo'))
        return render_template('sapsForm/step4.html', form=form)

    # fallback
    return redirect(url_for('auth.saps_form', step=1))

def str_to_bool(valor):
    return valor.lower() == 'sim'

@login_required
@auth_bp.route('/saps-form/resumo', methods=['GET', 'POST'])
def resumo():
    dados = {}
    dados.update(session.get('step1', {}))
    dados.update(session.get('step2', {}))
    dados.update(session.get('step3', {}))
    dados.update(session.get('step4', {}))

    # Verifica se o paciente já existe
    paciente = Paciente.query.filter_by(cpf=dados['cpf']).first()
    if not paciente:
        paciente = Paciente(
            cpf=dados['cpf'].replace('.', '').replace('-', ''),
            nome=dados['nome'],
            data_nascimento=datetime.strptime(dados['data_nascimento'], "%a, %d %b %Y %H:%M:%S GMT").date()
        )
        db.session.add(paciente)
        db.session.commit()

    # Converte lista de múltiplos motivos em string
    motivos_admissao_str = ",".join(dados.get('motivos_admissao', []))

    # Cria objeto Internacao com conversão de campos booleanos
    internacao = Internacao(
        paciente_id=paciente.id,
        leito=dados['leito'],
        procedencia=dados['procedencia'],
        data_admissao=datetime.strptime(dados['data_admissao'], "%a, %d %b %Y %H:%M:%S GMT").date(),
        reinternacao=str_to_bool(dados['reinternacao']),
        duracao_internacao=dados.get('duracao_internacao'),
        local_previo=dados.get('local_previo'),

        terapia_cancer=str_to_bool(dados['terapia_cancer']),
        cancer_metastatico=str_to_bool(dados['cancer_metastatico']),
        insuficiencia_cardiaca=str_to_bool(dados['insuficiencia_cardiaca']),
        cirrose=str_to_bool(dados['cirrose']),
        aids=str_to_bool(dados['aids']),
        drogas_vasoativas=str_to_bool(dados['drogas_vasoativas']),

        admissao_planejada=str_to_bool(dados['admissao_planejada']),
        motivos_admissao=motivos_admissao_str,

        cirurgia_realizada=str_to_bool(dados['cirurgia_realizada']),
        tipo_cirurgia=dados.get('tipo_cirurgia'),
        sitio_atomico=dados.get('sitio_atomico'),

        infeccao_aguda=str_to_bool(dados['infeccao_aguda']),
        tipo_infeccao=dados.get('tipo_infeccao'),

        glasgow=dados['glasgow'],
        temperatura=dados['temperatura'],
        frequencia_cardiaca=dados['frequencia_cardiaca'],
        pressao_sistolica=dados['pressao_sistolica'],
        bilirrubina=dados['bilirrubina'],
        creatinina=dados['creatinina'],
        leucocitos=dados['leucocitos'],
        ph=dados['ph'],
        plaquetas=dados['plaquetas'],
        oxigenacao=dados['oxigenacao']
    )

    db.session.add(internacao)
    db.session.commit()

    return render_template('sapsForm/resultado.html', dados=dados)

@auth_bp.route('/logout')
@login_required
def logout():
    """Processa o logout do usuário."""
    logout_user()
    return redirect(url_for('auth.login'))
