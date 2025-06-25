from flask import jsonify
from werkzeug.utils import secure_filename
from models import User
from extensions import db
import os


def validar_e_criar_usuario(form, upload_folder='static/uploads'):
    if not form.validate():
        mensagens = [f"{field}: {errs[0]}" for field, errs in form.errors.items()]
        return jsonify({'message': ' '.join(mensagens)}), 400

    if User.query.filter_by(email=form.email.data).first():
        return jsonify({'message': 'Email já está em uso.'}), 400

    if User.query.filter_by(username=form.username.data).first():
        return jsonify({'message': 'Nome de usuário já está em uso.'}), 400


    user = User(
        username=form.username.data,
        nome=form.nome.data,
        tipo=form.tipo.data,
        email=form.email.data
    )
    user.set_password(form.senha.data)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Usuário criado com sucesso!'}), 200
