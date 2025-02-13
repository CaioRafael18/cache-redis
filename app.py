import json
from flask import Flask, jsonify
from flask_cors import CORS
from database import DatabaseConfig
from dotenv import load_dotenv
load_dotenv() 

app = Flask(__name__)
CORS(app)

database = DatabaseConfig()

# Endpoint para buscar um CBO por codigo
@app.route("/cbo/<codigo>", methods=["GET"])
def get_cbo(codigo):
    # Verifica se o dado esta no cache Redis
    redis_client = database.get_redis_connection()
    cache_key = f"cbo:{codigo}"
    cache_data = redis_client.get(cache_key)

    if cache_data:
        return jsonify(json.loads(cache_data)), 200 

    # Se não estiver no cache, busca no banco de dados
    conn = database.get_postgres_connection()
    cur = conn.cursor()
    cur.execute("SELECT codigo, descricao FROM cbo WHERE codigo = %s", (codigo,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if not result:
        return jsonify({"erro": "CBO não encontrado"}), 404

    cbo_data = {"codigo": result[0], "descricao": result[1]}

    try:
        # Armazena no Redis por 10 minutos
        redis_client.setex(cache_key, 600, json.dumps(cbo_data))
    except Exception as e:
        print(f"Erro ao salvar no Redis: {e}")

    return jsonify(cbo_data), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
