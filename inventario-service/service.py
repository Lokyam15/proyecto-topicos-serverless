from db import get_connection

def obtener_productos():
    connection = get_connection()
    if connection is None:
        return []

    cursor = connection.cursor()
    cursor.execute("SELECT id, nombre, stock FROM productos ORDER BY id;")
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    productos = []
    for row in rows:
        productos.append({
            "id": row[0],
            "nombre": row[1],
            "stock": row[2]
        })

    return productos

def obtener_stock_por_id(producto_id):
    connection = get_connection()
    if connection is None:
        return None

    cursor = connection.cursor()
    cursor.execute(
        "SELECT id, nombre, stock FROM productos WHERE id = %s;",
        (producto_id,)
    )
    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "nombre": row[1],
        "stock": row[2]
    }

def actualizar_stock(producto_id, nuevo_stock):
    connection = get_connection()
    if connection is None:
        return None

    cursor = connection.cursor()
    cursor.execute(
        "UPDATE productos SET stock = %s WHERE id = %s RETURNING id, nombre, stock;",
        (nuevo_stock, producto_id)
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
        "stock": row[2]
    }