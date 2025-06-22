from flask import current_app
from itsdangerous import URLSafeTimedSerializer

from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def gerar_token(email):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(email, salt='recuperar-senha')

def validar_token(token, expiration=3600):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='recuperar-senha', max_age=expiration)
        return email
    except Exception:
        return None

def str_to_bool(valor):
    return valor.lower() == 'sim'
