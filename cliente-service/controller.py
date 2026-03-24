from flask import jsonify, request
from service import (
    obtener_clientes,
    obtener_cliente_por_id,
    crear_cliente,
    actualizar_cliente
)

def listar_clientes_controller():
    return jsonify(obtener_clientes())

def obtener_cliente_controller(cliente_id):
    cliente = obtener_cliente_por_id(cliente_id)

    if cliente is None:
        return jsonify({"error": "Cliente no encontrado"}), 404

    return jsonify(cliente)

def crear_cliente_controller():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Debe enviar datos en formato JSON"}), 400

    nombre = data.get("nombre")
    telefono = data.get("telefono")
    email = data.get("email")

    if not nombre:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400

    cliente = crear_cliente(nombre, telefono, email)

    if cliente is None:
        return jsonify({"error": "No se pudo crear el cliente"}), 500

    return jsonify({
        "mensaje": "Cliente creado correctamente",
        "cliente": cliente
    }), 201

def actualizar_cliente_controller(cliente_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Debe enviar datos en formato JSON"}), 400

    nombre = data.get("nombre")
    telefono = data.get("telefono")
    email = data.get("email")

    if not nombre:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400

    cliente = actualizar_cliente(cliente_id, nombre, telefono, email)

    if cliente is None:
        return jsonify({"error": "Cliente no encontrado"}), 404

    return jsonify({
        "mensaje": "Cliente actualizado correctamente",
        "cliente": cliente
    })