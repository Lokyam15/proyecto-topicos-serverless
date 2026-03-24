from controller import (
    listar_productos_controller,
    obtener_stock_controller,
    actualizar_stock_controller
)

def registrar_rutas(app):
    @app.route('/productos', methods=['GET'])
    def listar_productos():
        return listar_productos_controller()

    @app.route('/stock/<int:producto_id>', methods=['GET'])
    def obtener_stock(producto_id):
        return obtener_stock_controller(producto_id)

    @app.route('/stock/<int:producto_id>', methods=['PUT'])
    def actualizar_stock_route(producto_id):
        return actualizar_stock_controller(producto_id)