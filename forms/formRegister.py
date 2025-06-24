from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed
import re

class RegisterForm(FlaskForm):

    # def senha_forte(form, field):
    #     senha = field.data
    #     if len(senha) < 8:
    #         raise ValidationError('A senha deve ter pelo menos 8 caracteres.')
    #     if not re.search(r'[A-Z]', senha):
    #         raise ValidationError('A senha deve conter pelo menos uma letra maiúscula.')
    #     if not re.search(r'[a-z]', senha):
    #         raise ValidationError('A senha deve conter pelo menos uma letra minúscula.')
    #     if not re.search(r'\\d', senha):
    #         raise ValidationError('A senha deve conter pelo menos um número.')
    #     if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', senha):
    #         raise ValidationError('A senha deve conter pelo menos um caractere especial.')

    nome = StringField('Nome completo', validators=[DataRequired(), Length(min=4)])
    tipo = SelectField('Tipo de Usuário', choices=[
        ('medico', 'Médico'),
        ('enfermeiro', 'Enfermeiro'),
        ('administrador', 'Administrador')
    ], validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[
        DataRequired(),
        Length(min=8),
    ])
    foto_perfil = FileField('Foto de Perfil (opcional)', validators=[FileAllowed(['jpg', 'png'], 'Apenas imagens JPG/PNG')])
