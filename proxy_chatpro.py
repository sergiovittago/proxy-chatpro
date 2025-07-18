from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)

# Log simples no console
def log(msg):
    print(f"[LOG] {msg}")

@app.route('/')
def home():
    return "API do Proxy ChatPro no ar"

@app.route('/valida-cupom')
def valida_cupom():
    cupom = request.args.get('cupom')
    if not cupom:
        return jsonify({"error": "Cupom não fornecido"}), 400

    log(f"Recebendo validação para o cupom: {cupom}")

    try:
        # Escopo e autenticação
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('credenciais.json', scope)
        client = gspread.authorize(creds)

        # Nome ou URL da planilha
        sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1nDt7X9pekO1q0hlr0NFOHbIM4bwi2lygMQXMLa2NN9E/edit#gid=0")
        aba = sheet.sheet1  # Ou sheet.worksheet("nome_da_aba")

        dados = aba.get_all_records()
        log(f"{len(dados)} registros carregados da planilha.")

        for linha in dados:
            if str(linha.get("Cupom")).strip().upper() == cupom.strip().upper():
                log("Cupom encontrado e válido.")
                return jsonify({
                    "cupom": linha.get("Cupom"),
                    "status": "válido",
                    "descricao": linha.get("Descrição"),
                    "desconto": linha.get("Desconto")
                })

        log("Cupom não encontrado.")
        return jsonify({"cupom": cupom, "status": "inválido"}), 404

    except Exception as e:
        log(f"Erro ao validar cupom: {e}")
        return jsonify({"error": "Erro ao acessar planilha", "details": str(e)}), 500

# Executa localmente (não usado no Render)
if __name__ == '__main__':
    app.run(debug=True)