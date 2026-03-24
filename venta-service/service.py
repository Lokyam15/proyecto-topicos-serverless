import requests
from db import get_connection

CLIENTE_SERVICE_URL = "http://127.0.0.1:5002"
INVENTARIO_SERVICE_URL = "http://127.0.0.1:5001"

def validar_cliente(cliente_id):
    try:
        response = requests.get(f"{CLIENTE_SERVICE_URL}/clientes/{cliente_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print("Error al validar cliente:", repr(e))
        return None

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

def registrar_venta(cliente_id, producto_id, cantidad, precio_unitario):
    cliente = validar_cliente(cliente_id)
    if cliente is None:
        return {"error": "Cliente no encontrado"}, 404

    producto = obtener_stock_producto(producto_id)
    if producto is None:
        return {"error": "Producto no encontrado"}, 404

    stock_actual = producto["stock"]

    if stock_actual < cantidad:
        return {"error": "Stock insuficiente"}, 400

    nuevo_stock = stock_actual - cantidad
    resultado_stock = actualizar_stock_producto(producto_id, nuevo_stock)

    if resultado_stock is None:
        return {"error": "No se pudo actualizar el stock"}, 500

    connection = get_connection()
    if connection is None:
        return {"error": "No se pudo conectar a la base de datos"}, 500

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO ventas (cliente_id)
        VALUES (%s)
        RETURNING id, cliente_id, fecha;
        """,
        (cliente_id,)
    )
    venta_row = cursor.fetchone()
    venta_id = venta_row[0]

    cursor.execute(
        """
        INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario)
        VALUES (%s, %s, %s, %s)
        RETURNING id, venta_id, producto_id, cantidad, precio_unitario;
        """,
        (venta_id, producto_id, cantidad, precio_unitario)
    )
    detalle_row = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    return {
        "mensaje": "Venta registrada correctamente",
        "venta": {
            "id": venta_row[0],
            "cliente_id": venta_row[1],
            "fecha": str(venta_row[2])
        },
        "detalle": {
            "id": detalle_row[0],
            "venta_id": detalle_row[1],
            "producto_id": detalle_row[2],
            "cantidad": detalle_row[3],
            "precio_unitario": float(detalle_row[4])
        },
        "stock_actualizado": resultado_stock
    }, 201