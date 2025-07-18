from flask import Flask, request, make_response, jsonify
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Configurações de acesso à planilha
SPREADSHEET_ID = '1nDt7X9pekO1q0hlr0NFOHbIM4bwi2lygMQXMLa2NN9E'
NOME_ABA = 'CUPONS'  # ou ajuste para o nome real da aba

# Autenticação com a conta de serviço
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
CREDENTIALS_FILE = 'credentials.json'

def buscar_parceiro_por_cupom(cupom):
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        client = gspread.authorize(creds)
        planilha = client.open_by_key(SPREADSHEET_ID)
        aba = planilha.worksheet(NOME_ABA)
        dados = aba.get_all_values()

        for linha in dados[1:]:  # Pula o cabeçalho
            codigo = (linha[0] or '').strip().upper()
            parceiro = (linha[1] or '').strip()

            if codigo == cupom:
                return parceiro
        return None
    except Exception as e:
        print("Erro ao acessar planilha:", e)
        return None

@app.route('/valida-cupom', methods=['GET'])
def valida_cupom():
    cupom = request.args.get('cupom', '').strip().upper()

    if not cupom:
        return make_response('', 400)

    parceiro = buscar_parceiro_por_cupom(cupom)

    if parceiro:
        mensagem = (
            f"*Achei o cupom do nosso parceiro {parceiro}!*\n"
            f"Parabéns, você acaba de desbloquear um desconto especial\n"
            f"A gente ama quando boas indicações geram bons cuidados"
        )
        return jsonify({'mensagem': mensagem}), 200
    else:
        return make_response('', 400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
