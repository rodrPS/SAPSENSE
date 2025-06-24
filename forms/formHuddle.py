from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, RadioField, SelectMultipleField, SubmitField, widgets
)
from wtforms.validators import InputRequired, Optional
from flask import session

choices_equipe = [
            ('Médico', 'Médico'),
            ('Direção', 'Direção'),
            ('Enfermeiro', 'Enfermeiro'),
            ('Núcleo de segurança do paciente', 'Núcleo de segurança do paciente'),
            ('Fisioterapeuta', 'Fisioterapeuta'),
            ('Nutricionista', 'Nutricionista'),
            ('Técnicos em Enfermagem', 'Técnicos em Enfermagem'),
            ('Fonoaudiólogo', 'Fonoaudiólogo'),
            ('CORAS', 'CORAS'),
            ('Assistente Social', 'Assistente Social'),
            ('NIR', 'NIR')
        ]

class Step1Huddle(FlaskForm):
    def validate(self, extra_validators=None):
        is_valid = super().validate(extra_validators=extra_validators)
        if not is_valid:
            return False

        if self.equipe_compareceu.data == 'sim':
            if not self.equipe_huddle.data or len(self.equipe_huddle.data) == 0:
                self.equipe_huddle.errors.append("Selecione pelo menos um membro da equipe.")
                return False
            if self.tecnicos_enfermagem.data is None:
                self.tecnicos_enfermagem.errors.append("Informe a quantidade de técnicos de enfermagem.")
                return False

        return True
    turno = RadioField("Turno",
                       choices=[('Diurno', 'Diurno'),
                                ('Noturno', 'Noturno')],
                       default='Diurno',
                       validators=[InputRequired()])
    equipe_compareceu = RadioField("Equipe Compareceu?",
                                   choices=[('sim', 'Sim'),
                                            ('nao', 'Não')],
                                   default='sim',
                                   validators=[InputRequired()])

    equipe_huddle = SelectMultipleField(
        'Equipe do Huddle',
        choices=choices_equipe,
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False),
        validators=[Optional()]
    )

    tecnicos_enfermagem = IntegerField("Quantidade de Técnicos de Enfermagem", validators=[Optional()])

class Step2Huddle(FlaskForm):

    ha_leitos_bloqueados = RadioField(
        "Há leitos bloqueados?",
        choices=[('sim', 'Sim'), ('nao', 'Não')],
        default='sim',
        validators=[Optional()]
    )
    qtd_leitos_bloqueados = IntegerField("Quantidade", validators=[Optional()])
    motivo_bloqueio = StringField("Motivo", validators=[Optional()])

    altas_confirmadas = IntegerField("Altas confirmadas", validators=[Optional()])
    altas_aval = IntegerField("Altas a avaliar", validators=[Optional()])

    houve_solicitacao_vaga = RadioField(
        "Solicitação de vaga/regulação?",
        choices=[('sim', 'Sim'), ('nao', 'Não')],
        default='sim',
        validators=[Optional()]
    )
    qtd_solicitacoes = IntegerField("Quantidade de solicitações", validators=[Optional()])
    origem_solicitacoes = StringField("Origem das solicitações", validators=[Optional()])

    exames_programados = RadioField(
        "Exames programados?",
        choices=[('sim', 'Sim'), ('nao', 'Não')],
        default='sim',
        validators=[Optional()]
    )
    qtd_exames = IntegerField("Quantidade de exames", validators=[Optional()])
    quais_exames = StringField("Quais exames?", validators=[Optional()])

    def validate(self, extra_validators=None):
        is_valid = super().validate(extra_validators=extra_validators)
        if not is_valid:
            return False

        equipe_compareceu = session.get('step1', {}).get('equipe_compareceu') == 'sim'

        if equipe_compareceu:
            if self.altas_confirmadas.data is None:
                self.altas_confirmadas.errors.append("Campo obrigatório.")
                return False
            if self.altas_aval.data is None:
                self.altas_aval.errors.append("Campo obrigatório.")
                return False

        # Valida bloqueio de leitos
        if self.ha_leitos_bloqueados.data == 'sim':
            if self.qtd_leitos_bloqueados.data is None:
                self.qtd_leitos_bloqueados.errors.append("Informe a quantidade.")
                return False
            if not self.motivo_bloqueio.data:
                self.motivo_bloqueio.errors.append("Informe o motivo do bloqueio.")
                return False

        # Valida solicitação de vaga
        if self.houve_solicitacao_vaga.data == 'sim':
            if self.qtd_solicitacoes.data is None:
                self.qtd_solicitacoes.errors.append("Informe a quantidade de solicitações.")
                return False
            if not self.origem_solicitacoes.data:
                self.origem_solicitacoes.errors.append("Informe a origem das solicitações.")
                return False

        # Valida exames
        if self.exames_programados.data == 'sim':
            if self.qtd_exames.data is None:
                self.qtd_exames.errors.append("Informe a quantidade de exames.")
                return False
            if not self.quais_exames.data:
                self.quais_exames.errors.append("Descreva os exames.")
                return False

        return True

class Step3Huddle(FlaskForm):
    mais_graves = IntegerField("Pacientes mais graves", validators=[Optional()])
    em_isolamento = IntegerField("Pacientes em isolamento", validators=[Optional()])
    em_dialise = IntegerField("Pacientes em diálise", validators=[Optional()])
    usando_svd = IntegerField("Pacientes usando SVD", validators=[Optional()])
    usando_cvc = IntegerField("Pacientes usando CVC", validators=[Optional()])

    retirada_svd = RadioField("Indicação de retirada de SVD?", choices=[('sim', 'Sim'), ('nao', 'Não')],
    default='nao',
    validators=[Optional()])
    pacientes_retirada_svd = StringField("Pacientes", validators=[Optional()])

    retirada_cvc = RadioField("Indicação de retirada de CVC?", choices=[('sim', 'Sim'), ('nao', 'Não')],
    default='nao', validators=[Optional()])
    pacientes_retirada_cvc = StringField("Pacientes", validators=[Optional()])

    despertar_diario = RadioField("Indicação de despertar diário?", choices=[('sim', 'Sim'), ('nao', 'Não')],
    default='nao', validators=[Optional()])
    pacientes_despertar_diario = StringField("Pacientes", validators=[Optional()])

    ventilacao_mecanica = IntegerField("Quantidade de Pacientes em ventilação mecânica", validators=[Optional()])
    ims_maior_igual_4 = IntegerField("Quantidade de Pacientes com IMS ≥ 4", validators=[Optional()])
    progressao_funcional = IntegerField("Quantidade de Pacientes com cond. de progressão funcional", validators=[Optional()])

    def validate(self, extra_validators=None):
        is_valid = super().validate(extra_validators=extra_validators)
        if not is_valid:
            return False

        equipe_compareceu = session.get('step1', {}).get('equipe_compareceu') == 'sim'

        if self.retirada_svd.data == 'sim' and not self.pacientes_retirada_svd.data:
            self.pacientes_retirada_svd.errors.append("Informe os pacientes com indicação de retirada de SVD.")
            return False

        if self.retirada_cvc.data == 'sim' and not self.pacientes_retirada_cvc.data:
            self.pacientes_retirada_cvc.errors.append("Informe os pacientes com indicação de retirada de CVC.")
            return False

        if self.despertar_diario.data == 'sim' and not self.pacientes_despertar_diario.data:
            self.pacientes_despertar_diario.errors.append("Informe os pacientes com indicação de despertar diário.")
            return False

        if equipe_compareceu:
            obrigatorios = [
                (self.mais_graves, "Informe a quantidade de pacientes mais graves."),
                (self.em_isolamento, "Informe a quantidade de pacientes em isolamento."),
                (self.em_dialise, "Informe a quantidade de pacientes em diálise."),
                (self.usando_svd, "Informe a quantidade de pacientes usando SVD."),
                (self.usando_cvc, "Informe a quantidade de pacientes usando CVC."),
                (self.ventilacao_mecanica, "Informe a quantidade de pacientes em ventilação mecânica."),
                (self.ims_maior_igual_4, "Informe a quantidade de pacientes com IMS ≥ 4."),
                (self.progressao_funcional, "Informe a quantidade de pacientes com progressão funcional.")
            ]
            for campo, mensagem in obrigatorios:
                if campo.data is None:
                    campo.errors.append(mensagem)
                    return False

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
        if not is_valid:
            return False

        equipe_compareceu = session.get('step1', {}).get('equipe_compareceu') == 'sim'

        # Campos condicionais aos radios
        if self.problema_unidade.data == 'sim' and not self.descricao_unidade.data:
            self.descricao_unidade.errors.append("Informe os problemas da unidade.")
            return False

        if self.problema_hospital.data == 'sim' and not self.descricao_hospital.data:
            self.descricao_hospital.errors.append("Informe os problemas do hospital.")
            return False

        # Campos obrigatórios apenas se equipe compareceu
        if equipe_compareceu:
            if not self.evento_adverso.data:
                self.evento_adverso.errors.append("Informe se houve evento adverso.")
                return False

            if not self.problema_unidade.data:
                self.problema_unidade.errors.append("Informe se houve problema na unidade.")
                return False

            if not self.problema_hospital.data:
                self.problema_hospital.errors.append("Informe se houve problema no hospital.")
                return False

        return True


