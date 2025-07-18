from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

@app.route('/valida-cupom', methods=['GET'])
def valida_cupom():
    try:
        cupom = request.args.get('cupom', '').strip().upper()
        print(f"[INFO] Cupom recebido: {cupom}")

        if not cupom:
            print("[ERROR] Cupom não informado na URL.")
            return jsonify({"error": "Parâmetro 'cupom' obrigatório"}), 400

        # Autenticando com Google Sheets
        try:
            print("[INFO] Iniciando autenticação no Google Sheets...")
            scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
            creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
            gc = gspread.authorize(creds)
        except Exception as e:
            print(f"[ERROR] Erro na autenticação com o Google Sheets: {e}")
            return jsonify({"error": "Falha na autenticação com Google Sheets"}), 500

        try:
            print("[INFO] Acessando planilha...")
            sh = gc.open_by_key("1nDt7X9pekO1q0hlr0NFOHbIM4bwi2lygMQXMLa2NN9E")
            worksheet = sh.get_worksheet(0)  # primeira aba
            registros = worksheet.get_all_values()
            print(f"[INFO] Total de linhas encontradas: {len(registros)}")
        except Exception as e:
            print(f"[ERROR] Erro ao acessar planilha: {e}")
            return jsonify({"error": "Erro ao acessar planilha"}), 500

        for linha in registros[1:]:  # Ignora o cabeçalho
            codigo_planilha = linha[0].strip().upper()
            nome_parceiro = linha[1].strip()

            if codigo_planilha == cupom:
                print(f"[INFO] Cupom encontrado: {codigo_planilha} - Parceiro: {nome_parceiro}")
                return jsonify({"status": "ok", "parceiro": nome_parceiro}), 200

        print("[INFO] Cupom não encontrado na planilha.")
        return jsonify({"error": "Cupom não localizado"}), 400

    except Exception as e:
        print(f"[ERROR] Erro inesperado: {e}")
        return jsonify({"error": "Erro interno"}), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
