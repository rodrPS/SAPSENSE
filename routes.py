# SAPSENSE/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from forms.formInternacao import InternacaoForm
from forms.formSaps import Step1Form, Step2Form, Step3Form, Step4Form
from forms.formHuddle import Step1Huddle, Step2Huddle, Step3Huddle, Step4Huddle
from forms.formRegister import RegisterForm
from models import User, Paciente, Internacao, Huddle
from extensions import db, mail
from utils import gerar_token, validar_token, calcular_saps3, gerar_resumo_ia
from datetime import datetime, timedelta
from pytz import timezone
from sqlalchemy import desc

from validators.formHuddle import processar_huddle_basico, processar_huddle_completo
from validators.formInternacao import AtualizacaoInternacaoInvalida, atualizar_internacao_com_formulario
from validators.formSaps import FormularioIncompletoException, obter_dados_formulario, salvar_dados_saps

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.home_page'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('auth.home_page'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')
    return render_template('login/index.html')

@auth_bp.route('/home')
@login_required
def home_page():
    ultimo_huddle = Huddle.query.order_by(desc(Huddle.criado_em)).first()
    br_tz = timezone('America/Sao_Paulo')
    
    profissionais = {
        "Médicos": 0, "Direção": 0, "Enfermeiros": 0,
        "Núcleo de Segurança": 0, "Fisioterapeutas": 0,
        "Nutricionistas": 0, "Técnicos de Enfermagem": 0,
        "Fonoaudiólogos": 0, "CORAS": 0, "Assistentes Sociais": 0, "NIR": 0
    }

    if ultimo_huddle:
        data_ultimo_huddle = ultimo_huddle.criado_em.astimezone(br_tz).strftime("%d/%m/%Y")
        dados_huddle = {
            "mais_grave": ultimo_huddle.mais_graves or 0,
            "em_tratamento": ultimo_huddle.progressao_funcional or 0,
            "dialise": ultimo_huddle.em_dialise or 0,
            "sonda_vesical": ultimo_huddle.usando_svd or 0,
            "cateter_venoso": ultimo_huddle.usando_cvc or 0,
            "ventilacao_mecanica": ultimo_huddle.ventilacao_mecanica or 0,
            "im5_acima_4_4": ultimo_huddle.ims_maior_igual_4 or 0
        }
        dados_huddle["total"] = sum(dados_huddle.values())

        # Preenche as quantidades de profissionais
        profissionais.update({
            "Médicos": ultimo_huddle.qtd_medicos or 0,
            "Direção": ultimo_huddle.qtd_direcao or 0,
            "Enfermeiros": ultimo_huddle.qtd_enfermeiros or 0,
            "Núcleo de Segurança": ultimo_huddle.qtd_nucleo_seguranca or 0,
            "Fisioterapeutas": ultimo_huddle.qtd_fisioterapeutas or 0,
            "Nutricionistas": ultimo_huddle.qtd_nutricionistas or 0,
            "Técnicos de Enfermagem": ultimo_huddle.tecnicos_enfermagem or 0,
            "Fonoaudiólogos": ultimo_huddle.qtd_fonoaudiologos or 0,
            "CORAS": ultimo_huddle.qtd_coras or 0,
            "Assistentes Sociais": ultimo_huddle.qtd_assistente_social or 0,
            "NIR": ultimo_huddle.qtd_nir or 0
        })

    else:
        data_ultimo_huddle = "Nenhum Huddle registrado"
        dados_huddle = {key: 0 for key in ["mais_grave", "em_tratamento", "dialise", "sonda_vesical", "cateter_venoso", "ventilacao_mecanica", "im5_acima_4_4", "total"]}

    leitos_ocupados = Internacao.query.filter_by(data_desfecho=None).count()
    hoje = datetime.today().date()
    inicio_periodo = hoje - timedelta(days=6)
    entradas_por_dia, saidas_por_dia, dias_semana, dias_datas = [], [], [], []

    for i in range(7):
        dia = inicio_periodo + timedelta(days=i)
        entradas = Internacao.query.filter(Internacao.data_admissao == dia).count()
        saidas = Internacao.query.filter(Internacao.data_desfecho == dia).count()
        entradas_por_dia.append(entradas)
        saidas_por_dia.append(saidas)
        dias_semana.append(dia.strftime('%a'))
        dias_datas.append(dia.day)

    periodo = f"{inicio_periodo.strftime('%d/%m/%Y')} - {hoje.strftime('%d/%m/%Y')}"

    return render_template('home/index.html', ocupados=leitos_ocupados, entradas_por_dia=entradas_por_dia,
                           saidas_por_dia=saidas_por_dia, dias_semana=dias_semana, dias_datas=dias_datas,
                           periodo=periodo, dados_huddle=dados_huddle, data_ultimo_huddle=data_ultimo_huddle,
                           profissionais=profissionais)

@auth_bp.route('/saps-form', methods=['GET', 'POST'])
@login_required
def saps_form():
    step = int(request.args.get('step', 1))
    if step == 1:
        form = Step1Form()
        if form.validate_on_submit(): session['step1'] = form.data; return redirect(url_for('auth.saps_form', step=2))
        return render_template('sapsForm/step1.html', form=form)
    elif step == 2:
        form = Step2Form()
        if form.validate_on_submit(): session['step2'] = form.data; return redirect(url_for('auth.saps_form', step=3))
        return render_template('sapsForm/step2.html', form=form)
    elif step == 3:
        form = Step3Form()
        if form.validate_on_submit(): session['step3'] = form.data; return redirect(url_for('auth.saps_form', step=4))
        return render_template('sapsForm/step3.html', form=form)
    elif step == 4:
        form = Step4Form()
        if form.validate_on_submit(): session['step4'] = form.data; return redirect(url_for('auth.resumo'))
        return render_template('sapsForm/step4.html', form=form)
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
                    flash(f"Erro ao registrar o Huddle: {e}", "danger")
            return redirect(url_for('auth.huddle_form', step=2))
        return render_template('huddleForm/step1.html', form=form)
    elif step == 2:
        form = Step2Huddle()
        if form.validate_on_submit(): session['step2'] = form.data; return redirect(url_for('auth.huddle_form', step=3))
        return render_template('huddleForm/step2.html', form=form)
    elif step == 3:
        form = Step3Huddle()
        if form.validate_on_submit(): session['step3'] = form.data; return redirect(url_for('auth.huddle_form', step=4))
        return render_template('huddleForm/step3.html', form=form)
    elif step == 4:
        form = Step4Huddle()
        if form.validate_on_submit():
            session['step4'] = form.data
            if not all(k in session for k in ['step1', 'step2', 'step3']):
                flash("Sessão expirada ou incompleta. Por favor, preencha novamente.", "warning")
                return redirect(url_for('auth.huddle_form', step=1))
            dados = {**session.get('step1',{}), **session.get('step2',{}), **session.get('step3',{}), **form.data}
            try:
                processar_huddle_completo(dados)
                flash("Huddle completo registrado com sucesso!", "success")
                for key in ['step1', 'step2', 'step3', 'step4']: session.pop(key, None)
                return redirect(url_for('auth.home_page'))
            except Exception as e:
                flash(f"Erro ao salvar o Huddle: {e}", "danger")
        return render_template('huddleForm/step4.html', form=form)
    return redirect(url_for('auth.huddle_form', step=1))

@auth_bp.route('/saps-form/resumo', methods=['GET', 'POST'])
@login_required
def resumo():
    try:
        dados = obter_dados_formulario()
        saps_score, mortalidade_estimada = calcular_saps3(dados)
        salvar_dados_saps(dados, saps_score, mortalidade_estimada)
        resumo_ia = gerar_resumo_ia(dados, saps_score, mortalidade_estimada)
        flash("Formulário SAPS 3 salvo com sucesso!", "success")
        for key in ['step1', 'step2', 'step3', 'step4']: session.pop(key, None)
        return render_template('sapsForm/resultado.html', saps_score=saps_score, mortalidade=mortalidade_estimada, resumo_ia=resumo_ia)
    except (FormularioIncompletoException, RuntimeError) as e:
        flash(str(e), "danger")
        return redirect(url_for('auth.saps_form'))

@auth_bp.route('/pacientes')
@login_required
def lista_pacientes():
    page = request.args.get('page', 1, type=int)
    internacoes_paginated = Internacao.query.filter_by(data_desfecho=None).paginate(page=page, per_page=10)
    return render_template('pacientes/index.html', internacoes_paginated=internacoes_paginated)

@auth_bp.route('/pacientes/<int:id>/atualizar', methods=['GET', 'POST'])
@login_required
def atualizar_paciente(id):
    form = InternacaoForm()
    internacao = Internacao.query.get_or_404(id)
    dados_exibicao = {
        'nome': internacao.paciente.nome,
        'data_nascimento': internacao.paciente.data_nascimento.strftime("%d/%m/%Y"),
        'procedencia': internacao.procedencia,
        'data_admissao': internacao.data_admissao.strftime("%d/%m/%Y"),
        'reinternacao': "Sim" if internacao.reinternacao else "Não",
        'saps_score': internacao.saps_score or 0,
        'mortalidade_estimada': internacao.mortalidade_estimada or 0.0
    }
    if form.validate_on_submit():
        try:
            atualizar_internacao_com_formulario(form)
            flash("Dados do paciente atualizados com sucesso!", "success")
            return jsonify(success=True)
        except AtualizacaoInternacaoInvalida as e:
            return jsonify(success=False, error=str(e))
    elif request.method == "POST":
        html = render_template('pacientes/modal_editar.html', form=form, internacao_id=id, dados_exibicao=dados_exibicao)
        return jsonify(success=False, html=html)
    form.id.data = id
    form.diagnostico_atual.data = internacao.diagnostico_atual
    form.data_desfecho.data = internacao.data_desfecho
    form.desfecho.data = internacao.desfecho
    form.destino.data = internacao.destino
    if internacao.lpp_alta is not None: form.lpp_alta.data = "sim" if internacao.lpp_alta else "nao"
    if internacao.lpp_admissao is not None: form.lpp_admissao.data = "sim" if internacao.lpp_admissao else "nao"
    return render_template('pacientes/modal_editar.html', form=form, internacao_id=id, dados_exibicao=dados_exibicao)

@auth_bp.route('/atribuir-responsavel', methods=['POST'])
@login_required
def atribuir_responsavel():
    data = request.get_json()
    internacao_id = data.get('id')
    nome = data.get('responsavel')
    if not nome or len(nome.strip().split()) < 2:
        return jsonify({'success': False, 'message': 'Informe nome e sobrenome.'}), 400
    internacao = Internacao.query.get(internacao_id)
    if not internacao: return jsonify({'success': False, 'message': 'Internação não encontrada.'}), 404
    internacao.responsavel = nome.strip()
    db.session.commit()
    flash("Responsável atribuído com sucesso!", "success")
    return jsonify({'success': True})

@auth_bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    page = request.args.get('page', 1, type=int)
    users_paginated = User.query.paginate(page=page, per_page=10)
    form = RegisterForm()
    stats = {
        'total': User.query.count(),
        'medicos': User.query.filter_by(tipo='medico').count(),
        'enfermeiros': User.query.filter_by(tipo='enfermeiro').count(),
        'administradores': User.query.filter_by(tipo='administrador').count()
    }
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first(): return jsonify({'message': 'Email já em uso.'}), 400
        if User.query.filter_by(username=form.username.data).first(): return jsonify({'message': 'Usuário já em uso.'}), 400
        user = User(username=form.username.data, nome=form.nome.data, tipo=form.tipo.data, email=form.email.data)
        user.set_password(form.senha.data)
        db.session.add(user)
        db.session.commit()
        flash("Usuário criado com sucesso!", "success")
        return jsonify({'message': 'Usuário criado com sucesso!'}), 200
    if form.errors:
        field, error = list(form.errors.items())[0]
        return jsonify({'message': f'{field.capitalize()}: {error[0]}'}), 400
    return render_template('admin/index.html', users_paginated=users_paginated, form=form, stats=stats)

@auth_bp.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = gerar_token(email)
            reset_url = url_for('auth.redefinir_senha', token=token, _external=True)
            html = render_template('recuperar_senha/mail.html', reset_url=reset_url, user=user)
            msg = Message(subject='Redefinição de senha - SAPS sense', recipients=[email], html=html, sender=current_app.config['MAIL_USERNAME'])
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
        elif len(senha) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.', 'warning')
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                user.set_password(senha)
                db.session.commit()
                flash('Senha redefinida com sucesso!', 'success')
                return redirect(url_for('auth.login'))
        return redirect(request.url)
    return render_template('recuperar_nova_senha/index.html', token=token)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))