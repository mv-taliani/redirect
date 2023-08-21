from __init__ import create_app, db
from flask import request, render_template, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import USUARIOS, NUMEROS, MENSAGENS, LEADS, CNPJS
from operator import add
from itertools import chain
from urllib.parse import quote

from auth import EMPRESAS
from funcs import proximo_num
import requests

app = create_app()


@app.route('/', methods=['GET'])
def index():
    # env = request.form.to_dict()
    if current_user.is_authenticated:
        match current_user.hierarquia < 2:
            case False:
                return redirect(url_for('vendedores'))
            case True:
                return redirect(url_for('numeros', id=current_user.user_id))
    return redirect(url_for('auth.login'))


@app.route('/numeros', methods=['GET', 'POST'])
@login_required
def numeros():
    u_id = request.form.get('id') or request.args.get('id')
    vendedor = USUARIOS.query.filter_by(user_id=u_id if current_user.hierarquia > 1 else current_user.user_id).first()

    if request.method == 'POST':
        num = request.form.get('num')
        empresa = request.form.get('empresa')
        numero = NUMEROS(vend_id=u_id, numero=num, empresa=empresa)
        db.session.add(numero)
        db.session.commit()

    numeros = NUMEROS.query.filter_by(vend_id=u_id).all()

    return render_template('vendedor.html', vendedor=vendedor, telefones=numeros, empresas=EMPRESAS)


@app.get('/del_num')
@login_required
def del_num():
    num = request.args.get('num')
    uid = request.args.get('id')
    NUMEROS.query.filter_by(num_id=num).delete()
    db.session.commit()
    return redirect(url_for('numeros', id=uid))


@app.route('/vendedores', methods=['GET'])
@login_required
def vendedores():
    if not current_user.hierarquia < 2:
        empresa = request.args.get('emp')
        if empresa:
            em_campanha = USUARIOS.query.filter(USUARIOS.numeros.any(NUMEROS.campanha >= 1),
                                                USUARIOS.numeros.any(NUMEROS.empresa == empresa)).all()
            print(em_campanha)

            sem_campanha = USUARIOS.query.filter((NUMEROS.campanha == None) | (NUMEROS.campanha == 0),
                                                 USUARIOS.numeros.any(NUMEROS.empresa == empresa)) \
                .order_by(USUARIOS.nome).all()
        else:
            em_campanha = USUARIOS.query.filter(USUARIOS.numeros.any(NUMEROS.campanha >= 1)) \
                .order_by(USUARIOS.nome).all()

            sem_campanha = USUARIOS.query.filter((USUARIOS.numeros.any(db.not_(NUMEROS.campanha >= 1))) |
                                                 (USUARIOS.hierarquia <= 2)).all()
        return render_template('vendedores.html', campanha=em_campanha, sem_campanha=sem_campanha, empresas=EMPRESAS,
                               empresa=empresa)
    return redirect(url_for('numeros'))


@app.get('/up_vend')
def atualizar():
    vend = request.args.get('id')
    numero = db.session.query(NUMEROS).filter_by(num_id=vend).first()
    numero.campanha = add(NUMEROS.campanha, int(request.args.get('up'))) if numero.campanha != None else 1
    db.session.commit()
    return redirect(url_for('vendedores', emp=numero.empresa))


@app.post('/redirecionar')
def redirecionar():
    payload = request.get_json()
    usr = payload.get('usr')
    pwd = payload.get('pwd')
    link = payload.get('url')
    if usr == '_0r3l0g1n0-' and pwd == '9j#$09KlasdOIL)000':
        empresa = MENSAGENS.query.filter_by(url=link).order_by(db.func.random()).first()
        print(f'{link=}, {empresa=}')
        indice = CNPJS.query.filter_by(empresa=empresa.empresa).first()
        num = proximo_num(empresa.empresa)
        if indice.index >= len(num):
            indice.index = 0
        print(indice.index)
        proximo = num[indice.index]
        user = NUMEROS.query.filter_by(numero=proximo).first()
        url = f'https://api.whatsapp.com/send?phone={proximo}&text={quote(empresa.mensagem)}'
        indice.index += 1
        cnpj = LEADS(numero=int(user.numero), vendedor=user.vend_id, origem=empresa.men_id, click_data=db.func.now())
        db.session.add(cnpj)
        db.session.commit()

        r = jsonify(url)
        #r.headers.add('Access-Control-Allow-Origin', "*")
        return r

    return jsonify('error'), 403


@app.after_request
def add_security_headers(resp):
    resp.headers['Access-Control-Allow-Origin'] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS,POST,PUT"
    resp.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept, Authorization"
    return resp
