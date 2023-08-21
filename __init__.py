from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from sshtunnel import SSHTunnelForwarder


db = SQLAlchemy()


def create_app() -> Flask:
    """
    Isso é uma APP Factory.
    Ela cria uma instância do Flask() com __name__, a chave secreta configurada, a url de conexão do banco de dados,
    instância o gerenciador de logins do Flask-Login e registra todas as blueprints.

    Caso queira mudar o banco de dados, basta alterar a url.

    Returns:
        Uma instância de Flask(__name__)
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = r'8d556009626817653162ae2bece5b1f9de3fe765373ce2fdd7f4b074619735f9'

    # ssh = subprocess.Popen(f'ssh africa@192.168.15.28', shell=False,
    #                    stdout=subprocess.PIPE,
    #                    stderr=subprocess.PIPE)
    #
    # result = ssh.stdout.readlines()
    # if result == []:
    #     error = ssh.stderr.readlines()
    #     print(error)
    # else:
    #     print(result)

    app.config[
        'SQLALCHEMY_DATABASE_URI'
    ] = f'mysql+mysqlconnector://orengroup:mvt20052604@orengroup.mysql.pythonanywhere-services.com/orengroup$LINKS'
    #server = SSHTunnelForwarder(
    #('187.11.77.156', 35666),
    #ssh_username="africa",
    #ssh_password="pypy!123456Ab",
    #remote_bind_address=('192.168.15.28', 5432)
    #)

    #server.start()

    # app.config[
    #     'SQLALCHEMY_DATABASE_URI'
    # ] = 'postgresql+psycopg2://python:py!123456A@187.11.77.156:5432/LINKS'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle' : 280}
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Você precisa logar para acessar essa página'
    login_manager.init_app(app)
    from models import USUARIOS

    @login_manager.user_loader
    def load_user(user_id):
        return USUARIOS.query.get(int(user_id))

    from auth import auth
    from app import sdr
    # from .views import views
    #
    # app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(sdr, url_prefix='/sdr/')


    return app
