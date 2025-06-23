# models.py

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db, login_manager
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users' # Nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Ex: Médico, Enfermeiro, etc.
    email = db.Column(db.String(120), unique=True, nullable=False)
    foto_perfil = db.Column(db.String(255), nullable=True)


    def set_password(self, password):
        """Cria um hash da senha e o armazena."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)

    internacoes = db.relationship('Internacao', backref='paciente', lazy=True)

class Internacao(db.Model):
    __tablename__ = 'internacao'

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)

    leito = db.Column(db.String(50), nullable=False)
    procedencia = db.Column(db.String(50), nullable=False)
    data_admissao = db.Column(db.Date, nullable=False)
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)

    reinternacao = db.Column(db.Boolean, nullable=False)  # sim/nao
    duracao_internacao = db.Column(db.String(50), nullable=True)
    local_previo = db.Column(db.String(255), nullable=True)

    terapia_cancer = db.Column(db.Boolean, nullable=False)
    cancer_metastatico = db.Column(db.Boolean, nullable=False)
    insuficiencia_cardiaca = db.Column(db.Boolean, nullable=False)
    cirrose = db.Column(db.Boolean, nullable=False)
    aids = db.Column(db.Boolean, nullable=False)
    drogas_vasoativas = db.Column(db.Boolean, nullable=False)

    admissao_planejada = db.Column(db.Boolean, nullable=False)
    motivos_admissao = db.Column(db.String(512), nullable=False)

    cirurgia_realizada = db.Column(db.Boolean, nullable=False)
    tipo_cirurgia = db.Column(db.String(255), nullable=True)
    sitio_atomico = db.Column(db.String(255), nullable=True)


    infeccao_aguda = db.Column(db.Boolean, nullable=False)
    tipo_infeccao = db.Column(db.String(255), nullable=True)

    glasgow = db.Column(db.String(50), nullable=False)
    temperatura = db.Column(db.String(50), nullable=False)
    frequencia_cardiaca = db.Column(db.String(50), nullable=False)
    pressao_sistolica = db.Column(db.String(50), nullable=False)
    bilirrubina = db.Column(db.String(50), nullable=False)
    creatinina = db.Column(db.String(50), nullable=False)
    leucocitos = db.Column(db.String(50), nullable=False)
    ph = db.Column(db.String(50), nullable=False)
    plaquetas = db.Column(db.String(50), nullable=False)
    oxigenacao = db.Column(db.String(50), nullable=False)

    responsavel = db.Column(db.String(120), nullable=True)
    desfecho = db.Column(db.String(120), nullable=True)
    data_desfecho = db.Column(db.Date, nullable=True)
    destino = db.Column(db.String(120), nullable=True)

    saps_score = db.Column(db.Integer, nullable=True)
    mortalidade_estimada = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Internacao {self.id} - Paciente {self.paciente_id}>"

# O user_loader é movido para cá para ficar junto do modelo User.
# Ele informa ao Flask-Login como encontrar um usuário específico a partir do ID
# que é armazenado em sua sessão.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
