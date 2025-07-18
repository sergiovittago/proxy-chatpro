from flask import Flask, request, make_response, jsonify
import requests

app = Flask(__name__)

APPSCRIPT_URL = 'https://script.google.com/macros/s/AKfycbwRvVVRHdhMJGUeVxeM59KZf5DiGos36HRZ2oyj2SWGaKmNnW0VIN-YsGIG9okIA5bscA/exec'

@app.route('/valida-cupom', methods=['GET'])
def valida_cupom():
    cupom = request.args.get('cupom', '').lower()

    if not cupom:
        return make_response('', 400)

    try:
        resposta = requests.get(APPSCRIPT_URL, params={'cupom': cupom})

        if not resposta.content or not resposta.text.strip():
            return make_response('', 400)

        try:
            dados = resposta.json()
        except:
            return make_response('', 400)

        if dados.get('status') == 'success':
            parceiro = dados.get('parceiro', 'nosso parceiro')
            mensagem = (
                f"*Achei o cupom do nosso parceiro {parceiro}!*\n"
                f"Parabéns, você acaba de desbloquear um desconto especial\n"
                f"A gente ama quando boas indicações geram bons cuidados"
            )
            return jsonify({"mensagem": mensagem}), 200
        else:
            return make_response('', 400)

    except:
        return make_response('', 400)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
