from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from models import USUARIOS

auth = Blueprint('auth', __name__)

EMPRESAS = 'OREN TECNICO'.split(' ')


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        senha = request.form.get('senha')
        usuario = USUARIOS.query.filter_by(username=user).first()
        if not usuario:
            flash('Você deve logar!')
            return redirect(url_for('auth.login'))
        elif not check_password_hash(usuario.senha, senha):
            flash('Você deve logar!')
            return redirect(url_for('auth.login'))
        login_user(usuario)
        print(f'{user=}, {senha=}')
        return redirect(url_for('index'))
    return render_template('login.html')


@auth.route('/create_user', methods=['GET', 'POST'])
@login_required
def cadastrar():
    if request.method == 'POST':
        nome = request.form.get('nome')
        user = request.form.get('user')
        hierarquia = request.form.get('hierarquia')
        senha = request.form.get('senha')
        empresa = request.form.get('empresa')

        usu = USUARIOS.query.filter_by(username=user).first()
        if usu:
            flash('Usuário já existe!')
            return redirect(url_for('cadastrar'))
        USUARIOS.set_user(user, nome, senha, hierarquia, empresa=empresa)

        flash('Usuário criado com sucesso!')
    return render_template('cadastro.html', empresas=EMPRESAS)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

