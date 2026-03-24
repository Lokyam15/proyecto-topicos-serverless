from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'service': 'inventario-service'
    })

@app.route('/productos', methods=['GET'])
def listar_produtos():
    productos = [
        {"id": 1, "nombre": "Laptop", "stock": 10},
        {"id": 2, "nombre": "Mouse", "stock": 25}
    ]
    return jsonify(productos)

if __name__ == '__main__':
    app.run(debug=True, port=5001)