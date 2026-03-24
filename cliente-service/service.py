from db import get_connection

def obtener_clientes():
    connection = get_connection()
    if connection is None:
        return []

    cursor = connection.cursor()
    cursor.execute("SELECT id, nombre, telefono, email FROM clientes ORDER BY id;")
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    clientes = []
    for row in rows:
        clientes.append({
            "id": row[0],
            "nombre": row[1],
            "telefono": row[2],
            "email": row[3]
        })

    return clientes

def obtener_cliente_por_id(cliente_id):
    connection = get_connection()
    if connection is None:
        return None

    cursor = connection.cursor()
    cursor.execute(
        "SELECT id, nombre, telefono, email FROM clientes WHERE id = %s;",
        (cliente_id,)
    )
    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "nombre": row[1],
        "telefono": row[2],
        "email": row[3]
    }

def crear_cliente(nombre, telefono, email):
    connection = get_connection()
    if connection is None:
        return None

    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO clientes (nombre, telefono, email)
        VALUES (%s, %s, %s)
        RETURNING id, nombre, telefono, email;
        """,
        (nombre, telefono, email)
    )
    row = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    return {
        "id": row[0],
        "nombre": row[1],
        "telefono": row[2],
        "email": row[3]
    }

def actualizar_cliente(cliente_id, nombre, telefono, email):
    connection = get_connection()
    if connection is None:
        return None

    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE clientes
        SET nombre = %s, telefono = %s, email = %s
        WHERE id = %s
        RETURNING id, nombre, telefono, email;
        """,
        (nombre, telefono, email, cliente_id)
    )
    row = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "nombre": row[1],
        "telefono": row[2],
        "email": row[3]
    }