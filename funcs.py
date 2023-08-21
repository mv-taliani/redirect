from itertools import cycle, chain
# from contextlib import contextmanager
from models import USUARIOS, NUMEROS, MENSAGENS, LEADS, CNPJS


# from main import app, db


# def proximo_cons(dicio):
#     index = 0
#     try:
#         if len(dicio):
#
#         yield from proximo_tel(dicio, index)
#     except StopIteration:
#         index += 1
#
#
# todos = proximo_cons([['11111111111111111', '2222222222222222222222', '3333333333333333333333']])
# print(next(todos))
# print(next(todos))
# print(next(todos))
def proximo_num(empresa):
    # with app.app_context():
    users = USUARIOS.query.filter_by(hierarquia=1).filter(USUARIOS.numeros.any(NUMEROS.empresa == empresa),
                                                         USUARIOS.numeros.any(NUMEROS.campanha >= 1)).all()
    nums = [list(chain.from_iterable([[u.numero] * u.campanha
                                      for u in i.numeros
                                      if u.empresa == empresa and u.campanha
                                      ]))

            for i in users]
    return list(chain.from_iterable(nums))

# from main import app, db
# with open(r'C:\Users\Grupo Oren\Downloads\mensagens.txt', encoding='utf-8') as f:
#     with app.app_context():
#         for i in f:
#             linha = i.split(';')
#             mensagem = MENSAGENS(url=linha[0], mensagem=linha[1], empresa=linha[2])
#             db.session.add(mensagem)
#             db.session.commit()
#

# with app.app_context():
#     mensagem = MENSAGENS.query.all()
#     for i in mensagem:
#         i.empresa = 'OREN'
#         db.session.commit()


# from main import app, db
# from models import CNPJS
# with app.app_context():
#     for i in ['OREN', 'TECNICO', 'CRESCER']:
#         empresa = CNPJS(empresa=i, index=0)
#         db.session.add(empresa)
#     db.session.commit()
