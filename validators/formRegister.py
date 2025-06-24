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

    foto_filename = None
    if form.foto_perfil.data:
        filename = secure_filename(form.foto_perfil.data.filename)
        foto_path = os.path.join(upload_folder, filename)
        form.foto_perfil.data.save(foto_path)
        foto_filename = filename

    user = User(
        username=form.username.data,
        nome=form.nome.data,
        tipo=form.tipo.data,
        email=form.email.data,
        foto_perfil=foto_filename
    )
    user.set_password(form.senha.data)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Usuário criado com sucesso!'}), 200
