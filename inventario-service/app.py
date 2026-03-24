from flask import Flask, jsonify
from routes import registrar_rutas

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'service': 'inventario-service'
    })

registrar_rutas(app)
  

if __name__ == '__main__':
    app.run(host = '127.0.0.1' , port=5001, debug=True)