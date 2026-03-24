from controller import crear_compra_controller

def registrar_rutas(app):
    @app.route('/compras', methods=['POST'])
    def crear_compra():
        return crear_compra_controller()