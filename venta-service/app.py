from flask import Flask, jsonify
from routes import registrar_rutas

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "service": "venta-service"
    })

registrar_rutas(app)

if __name__ == '__main__':
    print("Iniciando venta-service...")
    app.run(port=5004, debug=True)