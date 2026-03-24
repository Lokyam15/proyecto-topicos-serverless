from db import get_connection

connection = get_connection()

if connection:
    print("Conexion exitosa a PostgreSQL")
    connection.close()
else:
    print("No se pudo conectar a PostgreSQL")