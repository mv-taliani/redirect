from flask_login import UserMixin
from __init__ import db
from werkzeug.security import generate_password_hash


class USUARIOS(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(200), unique=True)
    nome = db.Column(db.String(255), unique=True)
    senha = db.Column(db.String(100))
    hierarquia = db.Column(db.Integer)
    empresa = db.Column(db.String(100))
    numeros = db.relationship('NUMEROS', backref='usuario', lazy=True)

    @staticmethod
    def set_user(username, nome, senha, hierarquia, empresa):
        user = USUARIOS(username=username, nome=nome, senha=generate_password_hash(senha, 'SHA256'), hierarquia=hierarquia,
                        empresa=empresa)
        db.session.add(user)
        db.session.commit()

    def get_id(self):
        return str(self.user_id)


class NUMEROS(db.Model):
    num_id = db.Column(db.Integer, primary_key=True, unique=True)
    vend_id = db.Column(db.Integer, db.ForeignKey(USUARIOS.user_id), nullable=False)
    numero = db.Column(db.String(20))
    empresa = db.Column(db.String(20))
    campanha = db.Column(db.Integer)
    data_att = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    def set_numero(vend, num):
        numero = NUMEROS(vend_id=vend, numero=num)
        db.session.add(numero)
        db.session.commit()


class MENSAGENS(db.Model):
    men_id = db.Column(db.Integer, primary_key=True, unique=True)
    url = db.Column(db.String(255))
    mensagem = db.Column(db.String(255))
    empresa = db.Column(db.String(25))


class LEADS(db.Model):
    lead_id = db.Column(db.Integer, primary_key=True, unique=True)
    numero = db.Column(db.String(20))
    vendedor = db.Column(db.Integer, db.ForeignKey(USUARIOS.user_id))
    origem = db.Column(db.Integer, db.ForeignKey(MENSAGENS.men_id))
    click_data = db.Column(db.DateTime)


class CNPJS(db.Model):
    emp_id = db.Column(db.Integer, primary_key=True, unique=True)
    empresa = db.Column(db.String(100), unique=True)
    index = db.Column(db.Integer)
