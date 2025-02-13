import csv
from database import DatabaseConfig

def inserir_dados():
    try:
        # Conectar ao banco
        conn = DatabaseConfig().get_postgres_connection()
        cursor = conn.cursor()

        # Abrir CSV e inserir no banco
        with open('db/dados.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=";")
            next(reader)  # Pular cabeçalho

            for row in reader:
                try:
                    cursor.execute("INSERT INTO CBO (codigo, descricao) VALUES (%s, %s)", row)
                except Exception as e:
                    print(f"Erro ao inserir {row}: {e}")

        conn.commit()
        print("Dados inseridos com sucesso!")
    except Exception as e:
        print(f"Erro na conexão com o banco: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    inserir_dados()
