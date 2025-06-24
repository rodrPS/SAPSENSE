# routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from flask_wtf.csrf import CSRFProtect
from forms.formSaps import Step1Form, Step2Form, Step3Form, Step4Form
from forms.formHuddle import Step1Huddle, Step2Huddle, Step3Huddle, Step4Huddle
from forms.formRegister import RegisterForm
from datetime import datetime
from sqlalchemy import asc
from models import User, Paciente, Internacao, Huddle
from extensions import db, mail
from werkzeug.utils import secure_filename
import os
from utils import str_to_bool, gerar_token, validar_token, calcular_saps3, gerar_resumo_ia
from datetime import datetime

from validators.formHuddle import processar_huddle_basico, processar_huddle_completo


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


@auth_bp.route('/home')
@login_required
def home_page():
    """Renderiza a home page, acessível apenas para usuários logados."""
    # Conta o número de leitos ocupados (internações sem data de desfecho)
    leitos_ocupados = Internacao.query.filter_by(data_desfecho=None).count()

    # Busca as 5 internações mais recentes para exibir na tabela
    # Use um limite razoável para a home, a paginação completa fica em /pacientes
    internacoes_recentes = Internacao.query.filter_by(data_desfecho=None).order_by(Internacao.data_admissao.desc()).limit(5).all()

    #Pacientes
    page = request.args.get('page', 1, type=int)
    internacoes_paginated = Internacao.query.filter_by(data_desfecho=None).paginate(page=page, per_page=10)

    return render_template('home/index.html',
                           ocupados=leitos_ocupados,
                           internacoes=internacoes_recentes, internacoes_paginated=internacoes_paginated)

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

@auth_bp.route('/huddle-form', methods=['GET', 'POST'])
@login_required
def huddle_form():
    step = int(request.args.get('step', 1))

    if step == 1:
        form = Step1Huddle()
        if form.validate_on_submit():
            session['step1'] = form.data

            if form.equipe_compareceu.data == 'nao':
                    try:
                        processar_huddle_basico(form.data)
                        flash("Huddle registrado com sucesso!", "success")
                        return redirect(url_for('auth.home_page'))
                    except Exception as e:
                        flash("Erro ao registrar o Huddle: " + str(e), "danger")
                        return redirect(url_for('auth.huddle_form', step=1))
            return redirect(url_for('auth.huddle_form', step=2))
        return render_template('huddleForm/step1.html', form=form)

    elif step == 2:
        form = Step2Huddle()
        if form.validate_on_submit():
            session['step2'] = form.data
            return redirect(url_for('auth.huddle_form', step=3))
        return render_template('huddleForm/step2.html', form=form)

    elif step == 3:
        form = Step3Huddle()
        if form.validate_on_submit():
            session['step3'] = form.data
            return redirect(url_for('auth.huddle_form', step=4))
        return render_template('huddleForm/step3.html', form=form)

    elif step == 4:
        form = Step4Huddle()
        if form.validate_on_submit():
            session['step4'] = form.data
            dados = {**session['step1'], **session['step2'], **session['step3'], **form.data}
            try:
                processar_huddle_completo(dados)
                flash("Huddle completo registrado com sucesso!", "success")
                session.pop('step1', None)
                session.pop('step2', None)
                session.pop('step3', None)
                session.pop('step4', None)
                return redirect(url_for('auth.huddle_confirmado'))
            except Exception as e:
                flash("Erro ao salvar o Huddle: " + str(e), "danger")
                return redirect(url_for('auth.huddle_form', step=4))
        return render_template('huddleForm/step4.html', form=form)

    # fallback
    return redirect(url_for('auth.huddle_form', step=1))

@login_required
@auth_bp.route('/saps-form/resumo', methods=['GET', 'POST'])
def resumo():
    dados = {}
    dados.update(session.get('step1', {}))
    dados.update(session.get('step2', {}))
    dados.update(session.get('step3', {}))
    dados.update(session.get('step4', {}))

    saps_score, mortalidade_estimada = calcular_saps3(dados)

    resumo_ia = gerar_resumo_ia(dados, saps_score, mortalidade_estimada)

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
        oxigenacao=dados['oxigenacao'],
        saps_score=saps_score,
        mortalidade_estimada=mortalidade_estimada
    )

    db.session.add(internacao)
    db.session.commit()

    session.pop('step1', None)
    session.pop('step2', None)
    session.pop('step3', None)
    session.pop('step4', None)

    return render_template('sapsForm/resultado.html', saps_score=saps_score, mortalidade=mortalidade_estimada, resumo_ia=resumo_ia)

@auth_bp.route('/pacientes')
@login_required
def lista_pacientes():
    page = request.args.get('page', 1, type=int)

    internacoes_paginated = Internacao.query.filter_by(data_desfecho=None).paginate(page=page, per_page=10)

    return render_template('pacientes/index.html', internacoes_paginated=internacoes_paginated)

@auth_bp.route('/atribuir-responsavel', methods=['POST'])
@login_required
def atribuir_responsavel():
    data = request.get_json()
    internacao_id = data.get('id')
    nome = data.get('responsavel')

    if not nome or len(nome.strip().split()) < 2:
        return jsonify({'success': False, 'message': 'Nome inválido. Informe nome e sobrenome.'}), 400

    internacao = Internacao.query.get(internacao_id)
    if not internacao:
        return jsonify({'success': False, 'message': 'Internação não encontrada.'}), 404

    internacao.responsavel = nome.strip()
    db.session.commit()
    return jsonify({'success': True})

@auth_bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    page = request.args.get('page', 1, type=int)

    users_paginated = User.query.paginate(page=page, per_page=10)
    form = RegisterForm()

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            return jsonify({'message': 'Email já está em uso.'}), 400

        if User.query.filter_by(username=form.username.data).first():
            return jsonify({'message': 'Nome de usuário já está em uso.'}), 400

        # Salvar imagem (se enviada)
        foto_filename = None
        if form.foto_perfil.data:
            filename = secure_filename(form.foto_perfil.data.filename)
            foto_path = os.path.join('static/uploads', filename)
            form.foto_perfil.data.save(foto_path)
            foto_filename = filename

        user = User(
            username=form.username.data,
            nome=form.nome.data,
            tipo=form.tipo.data,
            email=form.email.data,
            foto_perfil=foto_filename
        )
        user.set_password(form.senha.data)
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'Usuário criado com sucesso!'}), 200

    for field, errors in form.errors.items():
        return jsonify({'message': f'{field}: {errors[0]}'}), 400

    return render_template('admin/index.html', users_paginated=users_paginated, form=form)

@auth_bp.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user:
            token = gerar_token(email)
            reset_url = url_for('auth.redefinir_senha', token=token, _external=True)

            # Renderiza o template de e-mail HTML
            html = render_template('recuperar_senha/mail.html', reset_url=reset_url, user=user)

            msg = Message(subject='Redefinição de senha - SAPS sense',
                          recipients=[email],
                          html=html,
                          sender=current_app.config['MAIL_USERNAME'])

            mail.send(msg)
            flash('Um e-mail com instruções foi enviado.', 'info')
        else:
            flash('E-mail não encontrado.', 'warning')

        return redirect(url_for('auth.login'))

    return render_template('recuperar_senha/index.html')

@auth_bp.route('/redefinir-senha/<token>', methods=['GET', 'POST'])
def redefinir_senha(token):
    email = validar_token(token)
    if not email:
        flash('Token expirado ou inválido.', 'danger')
        return redirect(url_for('auth.recuperar_senha'))

    if request.method == 'POST':
        senha = request.form.get('senha')
        confirmar = request.form.get('confirmar')

        if senha != confirmar:
            flash('As senhas não coincidem.', 'warning')
            return redirect(request.url)

        if len(senha) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.', 'warning')
            return redirect(request.url)

        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(senha)
            db.session.commit()
            flash('Senha redefinida com sucesso!', 'success')
            return redirect(url_for('auth.login'))

    return render_template('recuperar_nova_senha/index.html', token=token)

@auth_bp.route('/logout')
@login_required
def logout():
    """Processa o logout do usuário."""
    logout_user()
    return redirect(url_for('auth.login'))

