from flask import request, jsonify
from service import registrar_compra

def crear_compra_controller():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Debe enviar datos en formato JSON"}), 400

    producto_id = data.get("producto_id")
    cantidad = data.get("cantidad")
    precio_unitario = data.get("precio_unitario")

    if producto_id is None or cantidad is None or precio_unitario is None:
        return jsonify({
            "error": "Debe enviar producto_id, cantidad y precio_unitario"
        }), 400

    resultado, status = registrar_compra(producto_id, cantidad, precio_unitario)
    return jsonify(resultado), status