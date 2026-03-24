from controller import (
    listar_clientes_controller,
    obtener_cliente_controller,
    crear_cliente_controller,
    actualizar_cliente_controller
)

def registrar_rutas(app):
    @app.route('/clientes', methods=['GET'])
    def listar_clientes():
        return listar_clientes_controller()

    @app.route('/clientes/<int:cliente_id>', methods=['GET'])
    def obtener_cliente(cliente_id):
        return obtener_cliente_controller(cliente_id)

    @app.route('/clientes', methods=['POST'])
    def crear_cliente():
        return crear_cliente_controller()

    @app.route('/clientes/<int:cliente_id>', methods=['PUT'])
    def actualizar_cliente(cliente_id):
        return actualizar_cliente_controller(cliente_id)