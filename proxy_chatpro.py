from flask import Flask, request, jsonify, make_response
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Autenticação com Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
CREDS = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
client = gspread.authorize(CREDS)

# Abre a planilha e a aba correta
sheet = client.open_by_key('1nDt7X9pekO1q0hlr0NFOHbIM4bwi2lygMQXMLa2NN9E')
worksheet = sheet.worksheet('CUPONS')

@app.route('/valida-cupom', methods=['GET'])
def valida_cupom():
    cupom = request.args.get('cupom', '').strip().upper()

    if not cupom:
        return make_response('', 400)

    try:
        # Lê todas as linhas da aba
        dados = worksheet.get_all_values()

        # Ignora o cabeçalho e procura o cupom na coluna A
        for linha in dados[1:]:
            if len(linha) >= 2 and linha[0].strip().upper() == cupom:
                parceiro = linha[1].strip()
                mensagem = (
                    f"*Achei o cupom do nosso parceiro {parceiro}!*\n"
                    f"Parabéns, você acaba de desbloquear um desconto especial\n"
                    f"A gente ama quando boas indicações geram bons cuidados"
                )
                return jsonify({"mensagem": mensagem}), 200

        return make_response('', 400)

    except Exception as e:
        print(f'Erro: {e}')
        return make_response('', 400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)