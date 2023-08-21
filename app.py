from flask import Blueprint, request, jsonify
import requests
from urllib.parse import urlparse


sdr = Blueprint('sdr', __name__)

pos = {'oren': 0, 'crescer': 0, 'tecnico': 0}
@sdr.post('/bot_conversa')
def receive():
    resposta = request.get_json()
    visitor = resposta.get('visitor')
    fone, nome = visitor.get('phone'), visitor.get('name')
    match urlparse(resposta.get('page').get('url')).netloc:
        case 'www.preparatorioeja.com':
            with open('/home/orengroup/gerador/oren.csv') as f:
                arquivo = f.readlines()
            empresa = 'oren'

        case 'www.crescereja.com.br':
            with open('/home/orengroup/gerador/crescer.csv') as f:
                arquivo = f.readlines()
            empresa = 'crescer'

        case 'www.orengroup.com.br':
            with open('/home/orengroup/gerador/tecnico.csv') as f:
                arquivo = f.readlines()
            empresa = 'tecnico'
        case _:
            return None, 403

    header = {'Content-Type': 'application/json'}
    global pos
    if pos[empresa] == len(arquivo):
        pos[empresa] = 0

    url = arquivo[pos[empresa]].split(';')[1]

    pos[empresa] += 1

    requests.post(url,
                  json={'phone': fone, 'first_name': nome},
                  headers=header)

    return jsonify(resposta)

