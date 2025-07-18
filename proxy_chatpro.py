from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Caminho do arquivo de credenciais
CREDENTIALS_FILE = 'credentials.json'

# ID da planilha (retirado da URL)
SPREADSHEET_ID = '1nDt7X9pekO1q0hlr0NFOHbIM4bwi2IygMQXMLa2NN9E'
SHEET_NAME = 'CUPONS'

@app.route('/verificar_cupom', methods=['GET'])
def verificar_cupom():
    cupom = request.args.get('cupom', '').strip().upper()

    if not cupom:
        return jsonify({'error': 'Cupom não informado'}), 400

    try:
        print("🟡 Iniciando autenticação com Google Sheets...")
        scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
        client = gspread.authorize(credentials)
        print("✅ Autenticação realizada com sucesso.")

        print(f"🟡 Acessando planilha com ID: {SPREADSHEET_ID}")
        spreadsheet = client.open_by_key(SPREADSHEET_ID)

        print(f"🟡 Acessando aba '{SHEET_NAME}'")
        sheet = spreadsheet.worksheet(SHEET_NAME)

        print("🟡 Buscando todas as linhas da aba...")
        data = sheet.get_all_records()
        print(f"✅ {len(data)} registros encontrados.")

        for row in data:
            if str(row['CUPOM']).strip().upper() == cupom:
                print(f"✅ Cupom encontrado: {row}")
                return jsonify({'cupom': cupom, 'nome': row['NOME']})

        print("⚠️ Cupom não encontrado na planilha.")
        return jsonify({'error': 'Cupom não encontrado'}), 404

    except Exception as e:
        print(f"❌ Erro ao acessar planilha: {e}")
        return jsonify({'error': f'Erro ao acessar planilha: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
