from controller import crear_venta_controller

def registrar_rutas(app):
    @app.route('/ventas', methods=['POST'])
    def crear_venta():
        return crear_venta_controller()