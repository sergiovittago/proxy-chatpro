from flask import Flask, request, jsonify, make_response
import requests

app = Flask(__name__)

APPSCRIPT_URL = 'https://script.google.com/macros/s/SEU_ID/exec'  # substitua pela URL do App Script

@app.route('/valida-cupom', methods=['GET'])
def valida_cupom():
    cupom = request.args.get('cupom', '').lower()

    if not cupom:
        return '', 400  # Cupom não informado

    try:
        resposta = requests.get(APPSCRIPT_URL, params={'cupom': cupom})

        if not resposta.content or not resposta.text.strip():
            return '', 400  # Resposta vazia

        try:
            dados = resposta.json()
        except:
            return '', 400  # Resposta não é JSON

        if dados.get('status') == 'success':
            parceiro = dados.get('parceiro', 'nosso parceiro')

            mensagem = (
                f":confete_e_serpentina: Achei o cupom do nosso parceiro {parceiro}!\n"
                f"Parabéns, você acaba de desbloquear um desconto especial :brilhos:\n"
                f"A gente ama quando boas indicações geram bons cuidados :coração_azul:"
            )

            return jsonify({"mensagem": mensagem}), 200

        return '', 400  # Cupom inválido

    except:
        return '', 400  # Erro inesperado

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
