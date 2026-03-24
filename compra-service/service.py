import requests
from db import get_connection

INVENTARIO_SERVICE_URL = "http://127.0.0.1:5001"

def obtener_stock_producto(producto_id):
    try:
        response = requests.get(f"{INVENTARIO_SERVICE_URL}/stock/{producto_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print("Error al obtener stock:", repr(e))
        return None

def actualizar_stock_producto(producto_id, nuevo_stock):
    try:
        response = requests.put(
            f"{INVENTARIO_SERVICE_URL}/stock/{producto_id}",
            json={"stock": nuevo_stock}
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print("Error al actualizar stock:", repr(e))
        return None

def registrar_compra(producto_id, cantidad, precio_unitario):
    producto = obtener_stock_producto(producto_id)
    if producto is None:
        return {"error": "Producto no encontrado"}, 404

    stock_actual = producto["stock"]
    nuevo_stock = stock_actual + cantidad

    resultado_stock = actualizar_stock_producto(producto_id, nuevo_stock)
    if resultado_stock is None:
        return {"error": "No se pudo actualizar el stock"}, 500

    connection = get_connection()
    if connection is None:
        return {"error": "No se pudo conectar a la base de datos"}, 500

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO compras DEFAULT VALUES
        RETURNING id, fecha;
        """
    )
    compra_row = cursor.fetchone()
    compra_id = compra_row[0]

    cursor.execute(
        """
        INSERT INTO detalle_compras (compra_id, producto_id, cantidad, precio_unitario)
        VALUES (%s, %s, %s, %s)
        RETURNING id, compra_id, producto_id, cantidad, precio_unitario;
        """,
        (compra_id, producto_id, cantidad, precio_unitario)
    )
    detalle_row = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    return {
        "mensaje": "Compra registrada correctamente",
        "compra": {
            "id": compra_row[0],
            "fecha": str(compra_row[1])
        },
        "detalle": {
            "id": detalle_row[0],
            "compra_id": detalle_row[1],
            "producto_id": detalle_row[2],
            "cantidad": detalle_row[3],
            "precio_unitario": float(detalle_row[4])
        },
        "stock_actualizado": resultado_stock
    }, 201