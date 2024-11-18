from flask import Flask, jsonify, request


app = Flask(__name__)
import code.crypto

@app.route('/transactions', methods=['GET'])
def transactions():
    token = request.args.get('token')
    bankName = request.args.get('bankName')
    lastDate = request.args.get('lastDate')



    return "ok", 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)