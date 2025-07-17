from flask import Flask, request, jsonify, make_response
import requests
import re
import json

app = Flask(__name__)

APPSCRIPT_URL = 'https://script.google.com/macros/s/AKfycbwRvVVRHdhMJGUeVxeM59KZf5DiGos36HRZ2oyj2SWGaKmNnW0VIN-YsGIG9okIA5bscA/exec'

@app.route('/valida-cupom', methods=['GET'])
def valida_cupom():
    cupom = request.args.get('cupom', '').lower()

    if not cupom:
        return make_response(jsonify({'erro': 'Cupom não informado'}), 400)

    try:
        resposta = requests.get(APPSCRIPT_URL, params={'cupom': cupom})
        texto_resposta = resposta.text.strip()

        if not texto_resposta:
            return make_response(jsonify({'erro': 'Resposta vazia do App Script'}), 400)

        # Tenta decodificar como JSON válido
        try:
            dados = resposta.json()
            if isinstance(dados, dict) and dados.get('status') == 'success':
                return jsonify(dados)
            else:
                return make_response(jsonify({'erro': dados.get('mensagem', 'Cupom inválido')}), 400)
        except Exception:
            # Caso seja HTML, tenta extrair JSON embutido
            match = re.search(r'Error:\s*(\{.*\})\s*\(', texto_resposta)
            if match:
                try:
                    erro_embutido = json.loads(match.group(1))
                    return make_response(jsonify({'erro': erro_embutido.get('mensagem', 'Cupom inválido')}), 400)
                except:
                    pass

            return make_response(jsonify({'erro': 'Resposta inválida'}), 400)

    except Exception as e:
        return make_response(jsonify({'erro': 'Erro inesperado'}), 400)

if __name__ == '__main__':
    app.run(port=8080)
