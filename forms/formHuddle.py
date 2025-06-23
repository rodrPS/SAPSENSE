from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, RadioField, SelectMultipleField, SubmitField, widgets
)
from wtforms.validators import InputRequired, Optional

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
    turno = RadioField("Turno",
                       choices=[('Diurno', 'Diurno'),
                                ('Noturno', 'Noturno')],
                       default='Diurno',
                       validators=[InputRequired()])
    equipe_compareceu = RadioField("Equipe Compareceu",
                                   choices=[('Sim', 'Sim'),
                                            ('Não', 'Não')],
                                   default='Sim',
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
    leitos_ocupados = IntegerField("Leitos ocupados", validators=[Optional()])

    ha_leitos_bloqueados = RadioField(
        "Há leitos bloqueados?",
        choices=[('Sim', 'Sim'), ('Não', 'Não')],
        default='Sim',
        validators=[Optional()]
    )
    qtd_leitos_bloqueados = IntegerField("Quantidade", validators=[Optional()])
    motivo_bloqueio = StringField("Motivo", validators=[Optional()])

    altas_confirmadas = IntegerField("Altas confirmadas", validators=[Optional()])
    altas_aval = IntegerField("Altas a avaliar", validators=[Optional()])

    houve_solicitacao_vaga = RadioField(
        "Solicitação de vaga/regulação?",
        choices=[('Sim', 'Sim'), ('Não', 'Não')],
        default='Sim',
        validators=[Optional()]
    )
    qtd_solicitacoes = IntegerField("Quantidade de solicitações", validators=[Optional()])
    origem_solicitacoes = StringField("Origem das solicitações", validators=[Optional()])

    exames_programados = RadioField(
        "Exames programados?",
        choices=[('Sim', 'Sim'), ('Não', 'Não')],
        default='Sim',
        validators=[Optional()]
    )
    qtd_exames = IntegerField("Quantidade de exames", validators=[Optional()])
    quais_exames = StringField("Quais exames?", validators=[Optional()])

class Step3Huddle(FlaskForm):
    mais_graves = IntegerField("Mais graves", validators=[Optional()])
    em_isolamento = IntegerField("Em isolamento", validators=[Optional()])
    em_dialise = IntegerField("Em diálise", validators=[Optional()])
    usando_svd = IntegerField("Usando SVD", validators=[Optional()])
    usando_cvc = IntegerField("Usando CVC", validators=[Optional()])

    retirada_svd = RadioField("Indicação de retirada de SVD?", choices=[('Sim', 'Sim'), ('Não', 'Não')], validators=[Optional()])
    pacientes_retirada_svd = StringField("Pacientes", validators=[Optional()])

    retirada_cvc = RadioField("Indicação de retirada de CVC?", choices=[('Sim', 'Sim'), ('Não', 'Não')], validators=[Optional()])
    pacientes_retirada_cvc = StringField("Pacientes", validators=[Optional()])

    despertar_diario = RadioField("Indicação de despertar diário?", choices=[('Sim', 'Sim'), ('Não', 'Não')], validators=[Optional()])
    pacientes_despertar_diario = StringField("Pacientes", validators=[Optional()])

    ventilacao_mecanica = IntegerField("Ventilação mecânica", validators=[Optional()])
    ims_maior_igual_4 = IntegerField("IMS ≥ 4", validators=[Optional()])
    progressao_funcional = IntegerField("Cond. de progressão funcional", validators=[Optional()])

class Step4Huddle(FlaskForm):
    evento_adverso = RadioField("Evento adverso nas últimas 24h?", choices=[('Sim', 'Sim'), ('Não', 'Não')], validators=[Optional()])

    problema_unidade = RadioField("Problemas da unidade?", choices=[('Sim', 'Sim'), ('Não', 'Não')], validators=[Optional()])
    descricao_unidade = StringField("Quais?", validators=[Optional()])

    problema_hospital = RadioField("Problemas no hospital?", choices=[('Sim', 'Sim'), ('Não', 'Não')], validators=[Optional()])
    descricao_hospital = StringField("Quais?", validators=[Optional()])

    outro_problema = StringField("Outro problema", validators=[Optional()])

