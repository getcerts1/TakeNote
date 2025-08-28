from redis import Redis
import psycopg



r = Redis(host="localhost", port=6379, decode_responses=True)

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        conn = psycopg.connect(**config)
        print('Connected to the PostgreSQL server.')
        return conn
    except (psycopg.DatabaseError, Exception) as error:
        print(error)
        return {"error": error}

