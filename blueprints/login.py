from flask import Blueprint, request, jsonify
from flask_cors import CORS
from database import cursor

login = Blueprint("login", __name__, static_folder="static", template_folder="templates")
CORS(login)


@login.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Please provide both email and password"}), 400

    cursor.execute('SELECT * FROM employee WHERE emailaddress = %s', (email,))
    user = cursor.fetchone()
    if user and user['password'] == password:
        #Successful login
        sessionn = dict(user)
        return jsonify({"message": "Login successful", "user": sessionn}), 200
    else:
        #unsuccessful login
        return jsonify({"error": "Login unsuccessful. Please check email and password"}), 401
