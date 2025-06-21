from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, DateField, SelectMultipleField, widgets, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, InputRequired, ValidationError
import re


motivos_choices = [
    ('CARDIO/NEURO: DISTURBIOS DO RITMO CARDIACO', 'CARDIO/NEURO: DISTÚRBIOS DO RITMO CARDÍACO'),
    ('CARDIO/NEURO: CONVULSOES', 'CARDIO/NEURO: CONVULSÕES'),
    ('CARDIO: CHOQUE HIPOVOLEMICO (HEMORRAGICO OU NAO)', 'CARDIO: CHOQUE HIPOVOLÊMICO (HEMORRÁGICO OU NÃO)'),
    ('CARDIO: CHOQUE SEPTICO', 'CARDIO: CHOQUE SÉPTICO'),
    ('CARDIO: CHOQUE ANAFILATICO/MISTO OU INDEFINIDO', 'CARDIO: CHOQUE ANAFILÁTICO/MISTO OU INDEFINIDO'),
    ('NEURO: COMA/ESTUPOR/CONFUSAO/AGITAÇAO/DELIRIUM/DISTÚRBIOS SONO–VIGILIA', 'NEURO: COMA/ESTUPOR/CONFUSÃO/AGITAÇÃO/DELIRIUM/DISTÚRBIOS SONO–VIGÍLIA'),
    ('NEURO: DEFICIT NEUROLOGICO FOCAL', 'NEURO: DÉFICIT NEUROLÓGICO FOCAL'),
    ('NEURO: EFEITO DE MASSA INTRACRANIANA', 'NEURO: EFEITO DE MASSA INTRACRANIANA'),
    ('DIGESTIVO: ABDOMEN AGUDO/OUTR', 'DIGESTIVO: ABDÔMEN AGUDO/OUTRO'),
    ('DIGESTIVO: PANCREATITE SEVERA', 'DIGESTIVO: PANCREATITE SEVERA'),
    ('HEPATO: INSUFICIENCIA HEPATICA', 'HEPATO: INSUFICIÊNCIA HEPÁTICA')
]

class Step1Form(FlaskForm):
    """Etapa 1: Identificação do Paciente"""

    def CPFValido(form, field):
        cpf = re.sub(r'\D', '', field.data or '')
        if len(cpf) != 11:
            raise ValidationError('CPF deve conter 11 dígitos numéricos.')

    cpf = StringField('CPF',
                      validators=[DataRequired(message="CPF é obrigatório"), CPFValido])
    nome = StringField('Nome', validators=[DataRequired(message="Nome é obrigatório")])
    leito = SelectField('Leito', choices=[('', 'Selecione'),
                                              ('1', '1'),
                                              ('2', '2'),
                                              ('3', '3')],
                                     validators=[DataRequired(message="O leito é obrigatório")])
    data_nascimento = DateField('Data de Nascimento', validators=[DataRequired(message="Data de nascimento é obrigatória")])
    # tipo_paciente = RadioField('Tipo de Paciente',
    #                            choices=[('civil', 'Civil'), ('militar', 'Militar')],
    #                            validators=[DataRequired(message="Tipo de paciente é obrigatório")])

    procedencia = SelectField('Procedência',
                              choices=[('', 'Selecione'), ('emergencia', 'Emergência'),
                                       ('transferencia', 'Transferência'), ('cirurgia', 'Cirurgia'),
                                       ('ambulatorio', 'Ambulatório')],
                              validators=[DataRequired(message="Procedência é obrigatória")])

    data_admissao = DateField('Data de Admissão', validators=[DataRequired(message="Data de admissão é obrigatória")])
    registro = StringField('Nº de Registro', validators=[DataRequired(message="Número de registro é obrigatório")])
    reinternacao = RadioField('Reinternação em Menos de 24h',
                              choices=[('sim', 'Sim'), ('nao', 'Não')],
                              validators=[DataRequired(message="Informe se houve reinternação")])



class Step2Form(FlaskForm):
    """Etapa 2: Quadro I - Comorbidades Pré-existentes"""
    duracao_internacao = SelectField('Duração da Internação',
                                     choices=[('', 'Selecione'),
                                              ('<1d', 'Menos de 1 dia'),
                                              ('1-2d', '1 a 2 dias'),
                                              ('>2d', 'Mais de 2 dias')],
                                     validators=[DataRequired(message="Campo obrigatório")])
    local_previo = SelectField('Local de Internação',
                                     choices=[('', 'Selecione'),
                                              ('pronto-socorro/emergencia', 'Pronto-Socorro/Emergência'),
                                              ('uti', 'Outra UTI'),
                                              ('ala', 'Outra ALA')],
                                     validators=[DataRequired(message="Campo obrigatório")])
    terapia_cancer = RadioField('Terapia contra Câncer',
                                choices=[('sim', 'Sim'), ('nao', 'Não')],
                                validators=[DataRequired(message="Campo obrigatório")])
    cancer_metastatico = RadioField('Câncer Metastático',
                                    choices=[('sim', 'Sim'), ('nao', 'Não')],
                                    validators=[DataRequired(message="Campo obrigatório")])
    insuficiencia_cardiaca = RadioField('Insuficiência Cardíaca (CLASSE NYHA IV)',
                                        choices=[('sim', 'Sim'), ('nao', 'Não')],
                                        validators=[DataRequired(message="Campo obrigatório")])
    cirrose = RadioField('Cirrose',
                         choices=[('sim', 'Sim'), ('nao', 'Não')],
                         validators=[DataRequired(message="Campo obrigatório")])
    aids = RadioField('AIDS',
                      choices=[('sim', 'Sim'), ('nao', 'Não')],
                      validators=[DataRequired(message="Campo obrigatório")])
    drogas_vasoativas = RadioField('Uso de Drogas Vasoativas antes da Admissão',
                      choices=[('sim', 'Sim'), ('nao', 'Não')],
                      validators=[DataRequired(message="Campo obrigatório")])


class Step3Form(FlaskForm):
    """Etapa 3: Quadro II - Motivo da Admissão, Cirurgia e Infecção"""
    admissao_planejada = RadioField('Admissão Planejada?',
                                    choices=[('sim', 'Sim'), ('nao', 'Não')],
                                    validators=[DataRequired(message="Campo obrigatório")])
    motivos_admissao = SelectMultipleField(
        'Motivos de Admissão na UTI',
        choices=motivos_choices,
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False),
        validators=[InputRequired(message="Selecione pelo menos um motivo.")]
    )
    cirurgia_realizada = RadioField('Cirurgia realizada nas últimas 24h?',
                                    choices=[('sim', 'Sim'), ('nao', 'Não')],
                                    validators=[DataRequired(message="Campo obrigatório")])
    tipo_cirurgia =  SelectField('Tipo de Cirurgia',
                                     choices=[('', 'Selecione'),
                                              ('CIRURGIA PROGRAMADA', 'Cirurgia Programada'),
                                              ('CIRURGIA DE EMERGENCIA', 'Cirurgia de Emergência')],
                                     validators=[Optional()])
    sitio_atomico =  SelectField('Sítio Atômico da Cirurgia',
                                     choices=[('', 'Selecione'),
                                              ('CIRURGIA DE TRANSPLANTE', 'Cirurgia de Transplante'),
                                              ('CIRURGIA DE TRAUMA', 'Cirurgia de Trauma'),
                                              ('CIRURGIA CARDIACA (REVASCULARIZAÇÃO)', 'Cirugia Cardíaca (Revascularização)'),
                                              ('NEUROCIRURGIA', 'Neurocirurgia'),
                                              ('OUTRA CIRURGIA', 'Outra Cirugia'),],
                                     validators=[Optional()])
    infeccao_aguda = RadioField('Presença de Infecção Aguda?',
                                choices=[('sim', 'Sim'), ('nao', 'Não')],
                                validators=[DataRequired(message="Campo obrigatório")])
    tipo_infeccao =   SelectField('Tipo de Infecção',
                                     choices=[('', 'Selecione'),
                                              ('NOSOCOMIAL', 'Nosocomial'),
                                              ('RESPIRATORIA', 'Respiratória')],
                                     validators=[Optional()])

    def validate(self, extra_validators=None):
        rv = super().validate(extra_validators=extra_validators)
        if not rv:
            return False

        if self.cirurgia_realizada.data == "sim":
            if not (self.tipo_cirurgia.data or "").strip():
                self.tipo_cirurgia.errors.append("Campo obrigatório se cirurgia foi realizada.")
                rv = False
            if not self.sitio_atomico.data.strip():
                self.sitio_atomico.errors.append("Campo obrigatório se cirurgia foi realizada.")
                rv = False

        if self.infeccao_aguda.data == "sim":
            if not (self.tipo_infeccao.data or "").strip():
                self.tipo_infeccao.errors.append("Informe o tipo de infecção.")
                rv = False

        return rv

class Step4Form(FlaskForm):
    """Etapa 4: Quadro III - Dados categorizados SAPS"""

    glasgow = RadioField('Escala de Glasgow estimada (MENOR valor)', choices=[
        ('>=13', 'Maior ou igual a 13'),
        ('7-12', '7 a 12'),
        ('6', '6'),
        ('5', '5'),
        ('3-4', '3 a 4')
    ], validators=[DataRequired()])

    temperatura = RadioField('Temperatura corpórea (MAIOR valor)', choices=[
        ('>=35', 'Maior ou igual a 35º'),
        ('<35', 'Menor que 35º')
    ], validators=[DataRequired()])

    frequencia_cardiaca = RadioField('Frequência cardíaca (MAIOR valor)', choices=[
        ('<120', 'Menor que 120'),
        ('120-159', '120 a 159'),
        ('>=159', 'Maior que 159')
    ], validators=[DataRequired()])

    pressao_sistolica = RadioField('PA Sistólica (MENOR valor)', choices=[
        ('>120', 'Maior que 120'),
        ('70-119', '70 a 119'),
        ('40-69', '40 a 69'),
        ('<40', 'Menor que 40')
    ], validators=[DataRequired()])

    bilirrubina = RadioField('Bilirrubina Total (MAIOR valor)', choices=[
        ('<2.0', 'Menor que 2.0'),
        ('2.0-5.9', 'De 2.0 a 5.9'),
        ('>6.0', 'Maior que 6.0')
    ], validators=[DataRequired()])

    creatinina = RadioField('Creatinina (MAIOR valor)', choices=[
        ('<1.2', 'Menor que 1.2'),
        ('1.2-1.9', '1.2 a 1.9'),
        ('2.0-3.4', '2 a 3.4'),
        ('>=3.5', 'Maior ou igual a 3.5')
    ], validators=[DataRequired()])

    leucocitos = RadioField('Leucócitos (MENOR valor)', choices=[
        ('<15000', 'Menor que 15000'),
        ('>=15000', 'Maior que 15000')
    ], validators=[DataRequired()])

    ph = RadioField('pH', choices=[
        ('>7.25', 'Maior que 7.25'),
        ('<7.25', 'Menor que 7.25')
    ], validators=[DataRequired()])

    plaquetas = RadioField('Plaquetas (MENOR valor)', choices=[
        ('>=100000', 'Maior ou igual a 100000'),
        ('50000-99000', '50000 a 99000'),
        ('20000-49000', '20000 a 49000'),
        ('<20000', 'Menor que 20000')
    ], validators=[DataRequired()])

    oxigenacao = RadioField('Oxigenação (PaO₂ ou PaO₂/FiO₂)', choices=[
        ('PaO2>=60_sem_VM', 'PaO₂ ≥60 e sem VM'),
        ('PaO2<60_sem_VM', 'PaO₂ <60 e sem VM'),
        ('PaO2FIO2>=100_com_VM', 'PaO₂/FiO₂ ≥100 e VM'),
        ('PaO2FIO2<100_com_VM', 'PaO₂/FiO₂ <100 e VM')
    ], validators=[DataRequired()])
