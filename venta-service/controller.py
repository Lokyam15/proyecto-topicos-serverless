from flask import request, jsonify
from service import registrar_venta

def crear_venta_controller():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Debe enviar datos en formato JSON"}), 400

    cliente_id = data.get("cliente_id")
    producto_id = data.get("producto_id")
    cantidad = data.get("cantidad")
    precio_unitario = data.get("precio_unitario")

    if cliente_id is None or producto_id is None or cantidad is None or precio_unitario is None:
        return jsonify({
            "error": "Debe enviar cliente_id, producto_id, cantidad y precio_unitario"
        }), 400

    resultado, status = registrar_venta(cliente_id, producto_id, cantidad, precio_unitario)
    return jsonify(resultado), status