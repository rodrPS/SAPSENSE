from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileField, FileAllowed

class RegisterForm(FlaskForm):
    nome = StringField('Nome completo', validators=[DataRequired(), Length(min=4)])
    tipo = SelectField('Tipo de Usuário', choices=[
        ('medico', 'Médico'),
        ('enfermeiro', 'Enfermeiro'),
        ('administrador', 'Administrador')
    ], validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    foto_perfil = FileField('Foto de Perfil (opcional)', validators=[FileAllowed(['jpg', 'png'], 'Apenas imagens JPG/PNG')])
