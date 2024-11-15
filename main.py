from flask import Flask, jsonify, request
from code.auth_service import AuthService

app = Flask(__name__)
service = AuthService()

@app.route('/authorize', methods=['GET'])
def authorize():
    return service.getAuthorizationUrl(), 200

@app.route('/token', methods=['GET'])
def token():
    authorizationCode = request.args.get("code")
    state = request.args.get("state")
    return service.getToken(authorizationCode, state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)