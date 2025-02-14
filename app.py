import json, hashlib, time
from flask import Flask, jsonify
from flask_cors import CORS
from database import DatabaseConfig
from dotenv import load_dotenv
load_dotenv() 

app = Flask(__name__)
CORS(app)

database = DatabaseConfig()

def gerar_md5(codigo):
    return hashlib.md5(codigo.encode()).hexdigest()

# Endpoint para buscar um CBO por codigo
@app.route("/cbo/<codigo>", methods=["GET"])
def get_cbo(codigo):
    # Verifica se o dado esta no cache Redis
    redis_client = database.get_redis_connection()
    key_md5 = gerar_md5(codigo)
    cache_key = f"cbo:{key_md5}"

    # Mede o tempo redis
    start_time_redis = time.perf_counter()
    cache_data = redis_client.get(cache_key)
    end_time_redis = time.perf_counter()
    time_redis = end_time_redis - start_time_redis

    if cache_data:
        data = json.loads(cache_data)
        data["tempo"] = time_redis
        return jsonify(data), 200 

    # Se não estiver no cache, busca no banco de dados
    conn = database.get_postgres_connection()
    cursor = conn.cursor()

    # Mede o tempo postgres
    start_time_postgres = time.perf_counter()
    cursor.execute("SELECT codigo, descricao FROM cbo WHERE codigo = %s", (codigo,))
    result = cursor.fetchone()
    end_time_postgres = time.perf_counter() 
    time_postgres = end_time_postgres - start_time_postgres

    cursor.close()
    conn.close()

    if not result:
        return jsonify({"erro": "CBO não encontrado"}), 404

    cbo_data = {"codigo": result[0], "descricao": result[1], "tempo": time_postgres}

    try:
        # Armazena no Redis por 10 minutos
        redis_client.setex(cache_key, 600, json.dumps(cbo_data))
    except Exception as e:
        print(f"Erro ao salvar no Redis: {e}")

    return jsonify(cbo_data), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
