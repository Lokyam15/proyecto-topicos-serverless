from flask import jsonify, request
from service import obtener_productos, obtener_stock_por_id, actualizar_stock

def listar_productos_controller():
    return jsonify(obtener_productos())

def obtener_stock_controller(producto_id):
    producto = obtener_stock_por_id(producto_id)

    if producto is None:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify(producto)

def actualizar_stock_controller(producto_id):
    data = request.get_json()

    if not data or "stock" not in data:
        return jsonify({"error": "Debe enviar el campo 'stock'"}), 400

    nuevo_stock = data["stock"]

    producto_actualizado = actualizar_stock(producto_id, nuevo_stock)

    if producto_actualizado is None:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({
        "mensaje": "Stock actualizado correctamente",
        "producto": producto_actualizado
    })