from flask import Flask, jsonify, request

app = Flask(__name__)

# Endpoint de ejemplo
@app.route('/hola')
def home():
    return "¡Hola, Mundo!"

# Endpoint para manejar la autorización OAuth (puedes adaptarlo más tarde)
@app.route('/authorize', methods=['GET'])
def authorize():
    # Aquí iría la lógica de OAuth para PSD2
    return jsonify({"message": "Autorización OAuth pendiente"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
