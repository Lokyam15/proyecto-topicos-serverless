import psycopg2

def get_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            port="5432",
            database="topicos_db",
            user="postgres",    
            password="123456"
        )
        return connection
    except Exception as e:
        print("Error de conexion:", repr(e))
        return None