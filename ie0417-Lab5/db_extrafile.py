import time
import psycopg
from psycopg import OperationalError

MAX_RETRIES = 10

while True:
    try:
        conn = psycopg.connect(
            host="db",
            dbname="iotdb",
            user="postgres",
            password="postgres",
            port=5432
        )
        conn.close()
        break
    except OperationalError:
        MAX_RETRIES -= 1
        if MAX_RETRIES <= 0:
            print("No se pudo conectar ")
            exit(1)
        print("esperando conexión")
        time.sleep(1)