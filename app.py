from flask import Flask, jsonify, request, send_from_directory
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import os

app = Flask(__name__, static_folder='.')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'change-me-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)

jwt = JWTManager(app)

users = {}  # In-memory user storage (replace with a database in production)


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/formula')
def formula():
    return send_from_directory('.', 'formula.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({'msg': 'Username and password required'}), 400
    if username in users:
        return jsonify({'msg': 'User already exists'}), 409
    users[username] = password
    return jsonify({'msg': 'User registered successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username in users and users[username] == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({'msg': 'Bad username or password'}), 401


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
