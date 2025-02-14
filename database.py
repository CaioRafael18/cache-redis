import os
import psycopg2
import redis

class DatabaseConfig:
    def __init__(self):
        # Configuração do Redis
        self.redis_host = os.getenv("REDIS_HOST")
        self.redis_port = os.getenv("REDIS_PORT")
        self.redis_db = os.getenv("REDIS_DB")

        # Configuração do PostgreSQL
        self.postgres_dbname = os.getenv("POSTGRES_DB")
        self.postgres_user = os.getenv("POSTGRES_USER")
        self.postgres_password = os.getenv("POSTGRES_PASSWORD")
        self.postgres_host = os.getenv("POSTGRES_HOST")
        self.postgres_port = os.getenv("POSTGRES_PORT")

    # Retorna conexão com o postgres
    def get_postgres_connection(self, use_localhost=False):
        host = "localhost" if use_localhost else self.postgres_host

        db_params = {
            "dbname": self.postgres_dbname,
            "user": self.postgres_user,
            "password": self.postgres_password,
            "host": host,
            "port": self.postgres_port,
        }
        return psycopg2.connect(**db_params)

    # Retorna conexão com o redis
    def get_redis_connection(self):
        return redis.StrictRedis(
            host=self.redis_host, port=self.redis_port, db=self.redis_db
        )