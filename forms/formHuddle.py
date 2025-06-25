# SAPSENSE/forms/formHuddle.py
from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, RadioField, SubmitField
)
from wtforms.validators import InputRequired, Optional, NumberRange
from flask import session

class Step1Huddle(FlaskForm):
    turno = RadioField("Turno",
                       choices=[('Diurno', 'Diurno'), ('Noturno', 'Noturno')],
                       default='Diurno',
                       validators=[InputRequired()])
    equipe_compareceu = RadioField("Equipe Compareceu?",
                                   choices=[('sim', 'Sim'), ('nao', 'Não')],
                                   default='sim',
                                   validators=[InputRequired()])

    # Campos de quantidade
    qtd_medicos = IntegerField("Médicos", validators=[Optional(), NumberRange(min=0)], default=0)
    qtd_direcao = IntegerField("Direção", validators=[Optional(), NumberRange(min=0)], default=0)
    qtd_enfermeiros = IntegerField("Enfermeiros", validators=[Optional(), NumberRange(min=0)], default=0)
    qtd_nucleo_seguranca = IntegerField("Núcleo de Segurança", validators=[Optional(), NumberRange(min=0)], default=0)
    qtd_fisioterapeutas = IntegerField("Fisioterapeutas", validators=[Optional(), NumberRange(min=0)], default=0)
    qtd_nutricionistas = IntegerField("Nutricionistas", validators=[Optional(), NumberRange(min=0)], default=0)
    tecnicos_enfermagem = IntegerField("Técnicos de Enfermagem", validators=[Optional(), NumberRange(min=0)], default=0)
    qtd_fonoaudiologos = IntegerField("Fonoaudiólogos", validators=[Optional(), NumberRange(min=0)], default=0)
    qtd_coras = IntegerField("CORAS", validators=[Optional(), NumberRange(min=0)], default=0)
    qtd_assistente_social = IntegerField("Assistentes Sociais", validators=[Optional(), NumberRange(min=0)], default=0)
    qtd_nir = IntegerField("NIR", validators=[Optional(), NumberRange(min=0)], default=0)

    def validate(self, extra_validators=None):
        is_valid = super().validate(extra_validators=extra_validators)
        if not is_valid:
            return False

        if self.equipe_compareceu.data == 'sim':
            quantities = [
                self.qtd_medicos.data, self.qtd_direcao.data, self.qtd_enfermeiros.data,
                self.qtd_nucleo_seguranca.data, self.qtd_fisioterapeutas.data,
                self.qtd_nutricionistas.data, self.tecnicos_enfermagem.data,
                self.qtd_fonoaudiologos.data, self.qtd_coras.data,
                self.qtd_assistente_social.data, self.qtd_nir.data
            ]
            
            total_profissionais = sum(q for q in quantities if isinstance(q, int) and q > 0)
            
            if total_profissionais == 0:
                msg = "Se a equipe compareceu, informe a quantidade de pelo menos um profissional."
                # Adiciona o erro a um campo para exibição
                self.qtd_medicos.errors.append(msg)
                return False
        return True

class Step2Huddle(FlaskForm):
    ha_leitos_bloqueados = RadioField("Há leitos bloqueados?", choices=[('sim', 'Sim'), ('nao', 'Não')], default='nao', validators=[Optional()])
    qtd_leitos_bloqueados = IntegerField("Quantidade", validators=[Optional(), NumberRange(min=0)], default=0)
    motivo_bloqueio = StringField("Motivo", validators=[Optional()])
    altas_confirmadas = IntegerField("Altas confirmadas", validators=[Optional(), NumberRange(min=0)], default=0)
    altas_aval = IntegerField("Altas a avaliar", validators=[Optional(), NumberRange(min=0)], default=0)
    houve_solicitacao_vaga = RadioField("Solicitação de vaga/regulação?", choices=[('sim', 'Sim'), ('nao', 'Não')], default='nao', validators=[Optional()])
    qtd_solicitacoes = IntegerField("Quantidade de solicitações", validators=[Optional(), NumberRange(min=0)], default=0)
    origem_solicitacoes = StringField("Origem das solicitações", validators=[Optional()])
    exames_programados = RadioField("Exames programados?", choices=[('sim', 'Sim'), ('nao', 'Não')], default='nao', validators=[Optional()])
    qtd_exames = IntegerField("Quantidade de exames", validators=[Optional(), NumberRange(min=0)], default=0)
    quais_exames = StringField("Quais exames?", validators=[Optional()])

    def validate(self, extra_validators=None):
        is_valid = super().validate(extra_validators=extra_validators)
        if not is_valid: return False
        equipe_compareceu = session.get('step1', {}).get('equipe_compareceu') == 'sim'
        if equipe_compareceu:
            if self.altas_confirmadas.data is None: self.altas_confirmadas.errors.append("Campo obrigatório."); return False
            if self.altas_aval.data is None: self.altas_aval.errors.append("Campo obrigatório."); return False
        if self.ha_leitos_bloqueados.data == 'sim':
            if self.qtd_leitos_bloqueados.data is None: self.qtd_leitos_bloqueados.errors.append("Informe a quantidade."); return False
            if not self.motivo_bloqueio.data: self.motivo_bloqueio.errors.append("Informe o motivo."); return False
        if self.houve_solicitacao_vaga.data == 'sim':
            if self.qtd_solicitacoes.data is None: self.qtd_solicitacoes.errors.append("Informe a quantidade."); return False
            if not self.origem_solicitacoes.data: self.origem_solicitacoes.errors.append("Informe a origem."); return False
        if self.exames_programados.data == 'sim':
            if self.qtd_exames.data is None: self.qtd_exames.errors.append("Informe a quantidade."); return False
            if not self.quais_exames.data: self.quais_exames.errors.append("Descreva os exames."); return False
        return True

class Step3Huddle(FlaskForm):
    mais_graves = IntegerField("Pacientes mais graves", validators=[Optional(), NumberRange(min=0)], default=0)
    em_isolamento = IntegerField("Pacientes em isolamento", validators=[Optional(), NumberRange(min=0)], default=0)
    em_dialise = IntegerField("Pacientes em diálise", validators=[Optional(), NumberRange(min=0)], default=0)
    usando_svd = IntegerField("Pacientes usando SVD", validators=[Optional(), NumberRange(min=0)], default=0)
    usando_cvc = IntegerField("Pacientes usando CVC", validators=[Optional(), NumberRange(min=0)], default=0)
    retirada_svd = RadioField("Indicação de retirada de SVD?", choices=[('sim', 'Sim'), ('nao', 'Não')], default='nao', validators=[Optional()])
    pacientes_retirada_svd = StringField("Pacientes", validators=[Optional()])
    retirada_cvc = RadioField("Indicação de retirada de CVC?", choices=[('sim', 'Sim'), ('nao', 'Não')], default='nao', validators=[Optional()])
    pacientes_retirada_cvc = StringField("Pacientes", validators=[Optional()])
    despertar_diario = RadioField("Indicação de despertar diário?", choices=[('sim', 'Sim'), ('nao', 'Não')], default='nao', validators=[Optional()])
    pacientes_despertar_diario = StringField("Pacientes", validators=[Optional()])
    ventilacao_mecanica = IntegerField("Pacientes em ventilação mecânica", validators=[Optional(), NumberRange(min=0)], default=0)
    ims_maior_igual_4 = IntegerField("Pacientes com IMS ≥ 4", validators=[Optional(), NumberRange(min=0)], default=0)
    progressao_funcional = IntegerField("Pacientes com cond. de progressão funcional", validators=[Optional(), NumberRange(min=0)], default=0)

    def validate(self, extra_validators=None):
        is_valid = super().validate(extra_validators=extra_validators)
        if not is_valid: return False
        if self.retirada_svd.data == 'sim' and not self.pacientes_retirada_svd.data: self.pacientes_retirada_svd.errors.append("Informe os pacientes."); return False
        if self.retirada_cvc.data == 'sim' and not self.pacientes_retirada_cvc.data: self.pacientes_retirada_cvc.errors.append("Informe os pacientes."); return False
        if self.despertar_diario.data == 'sim' and not self.pacientes_despertar_diario.data: self.pacientes_despertar_diario.errors.append("Informe os pacientes."); return False
        equipe_compareceu = session.get('step1', {}).get('equipe_compareceu') == 'sim'
        if equipe_compareceu:
            obrigatorios = [
                (self.mais_graves, "Campo obrigatório."), (self.em_isolamento, "Campo obrigatório."),
                (self.em_dialise, "Campo obrigatório."), (self.usando_svd, "Campo obrigatório."),
                (self.usando_cvc, "Campo obrigatório."), (self.ventilacao_mecanica, "Campo obrigatório."),
                (self.ims_maior_igual_4, "Campo obrigatório."), (self.progressao_funcional, "Campo obrigatório.")
            ]
            for campo, msg in obrigatorios:
                if campo.data is None: campo.errors.append(msg); return False
        return True

class Step4Huddle(FlaskForm):
    evento_adverso = RadioField("Evento adverso nas últimas 24h?", choices=[('sim', 'Sim'), ('nao', 'Não')], default='nao', validators=[Optional()])
    problema_unidade = RadioField("Problemas da unidade?", choices=[('sim', 'Sim'), ('nao', 'Não')], default='nao', validators=[Optional()])
    descricao_unidade = StringField("Quais?", validators=[Optional()])
    problema_hospital = RadioField("Problemas no hospital?", choices=[('sim', 'Sim'), ('nao', 'Não')], default='nao', validators=[Optional()])
    descricao_hospital = StringField("Quais?", validators=[Optional()])
    outro_problema = StringField("Outro problema", validators=[Optional()])

    def validate(self, extra_validators=None):
        is_valid = super().validate(extra_validators=extra_validators)
        if not is_valid: return False
        if self.problema_unidade.data == 'sim' and not self.descricao_unidade.data: self.descricao_unidade.errors.append("Informe os problemas."); return False
        if self.problema_hospital.data == 'sim' and not self.descricao_hospital.data: self.descricao_hospital.errors.append("Informe os problemas."); return False
        equipe_compareceu = session.get('step1', {}).get('equipe_compareceu') == 'sim'
        if equipe_compareceu:
            if not self.evento_adverso.data: self.evento_adverso.errors.append("Informe se houve evento adverso."); return False
            if not self.problema_unidade.data: self.problema_unidade.errors.append("Informe se houve problema na unidade."); return False
            if not self.problema_hospital.data: self.problema_hospital.errors.append("Informe se houve problema no hospital."); return False
        return True