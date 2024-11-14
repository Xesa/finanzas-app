from flask import Flask, jsonify, request
import code.config

app = Flask(__name__)

@app.route('/authorize', methods=['GET'])
def authorize():
    # Aquí iría la lógica de OAuth para PSD2
    return jsonify({"message": "Autorización OAuth pendiente"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
