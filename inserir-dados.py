import csv
from database import DatabaseConfig

def inserir_dados():
    cursor = None
    conn = None
    try:
        # Conectando com o banco
        conn = DatabaseConfig().get_postgres_connection(use_localhost=True)  
        cursor = conn.cursor() 
        dadosInseridos = False 

        with open('db/dados.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=";")
            next(reader)  # Pular cabeçalho

            for row in reader:
                codigo = row[0]
                if not buscar_codigo(cursor, codigo):  
                    cursor.execute("INSERT INTO CBO (codigo, descricao) VALUES (%s, %s)", row)
                    dadosInseridos = True  

        if dadosInseridos:  
            conn.commit()
            print("Dados inseridos com sucesso!")
        else:
            print("Dados já foram inseridos anteriormente!")

    except Exception as e:
        print(f"Erro na conexão ou inserção de dados: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Verifica se o código já existe no banco
def buscar_codigo(cursor, codigo):
    try:
        cursor.execute("SELECT 1 FROM cbo WHERE codigo = %s", (codigo,))
        return cursor.fetchone() is not None  # Retorna True se já existir
    except Exception as e:
        print(f"Erro ao buscar {codigo}: {e}")
        return False

if __name__ == "__main__":
    inserir_dados()
