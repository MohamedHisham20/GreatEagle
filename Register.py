from database import Users, db
from extensions import bcrypt
from flask import request, jsonify, Blueprint
from flask_cors import CORS


register = Blueprint("register", __name__, static_folder="static")
# CORS(register, resources={
#     r"/*": {"origins": "http://localhost:3000"}})  # Allow CORS for the login blueprint (Cross-Origin Resource Sharing

"""
@register.route('/register', methods=['POST'])
def register_1():

"""

#register route using sqlalchemy and add the user into the database
@register.route('/register', methods=['POST'])
def register_1():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    age = data.get('age')
    email = data.get('email')

    #check if email and password are provided
    if not email or not password:
        return jsonify({"error": "Please provide both email and password"}), 400

    #check if user exists in the db
    user = Users.query.filter_by(email=email).first()
    if user:
        return jsonify({"error": "User already exists"}), 400

    #hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    #add the user to the database
    new_user = Users(username=username, password=hashed_password, name=name, age=age, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201



# @register.route('/check_user', methods=['POST'])
# def check_user():
#         data = request.json
#         NID = data.get('NID')
#
#         cursor.execute("SELECT nationalid FROM Admins WHERE nationalid = %s", (NID,))
#         valid_user = cursor.fetchone()
#
#         if valid_user: # nid exists in the db
#             return jsonify({"message": "Valid user"}), 200
#         else: # nid dont exist in the db
#             return jsonify({"message": "User does not exist"}), 400
#
# @register.route('/Register', methods=['POST'])
# def Register_2():
#     data = request.json
#     print(data)
#     NID = data.get('NID')
#     username = data.get('username')
#     password = data.get('password')
#     firstname = data.get('firstName')
#     lastname = data.get('lastName')
#     dateofbirth = data.get('dob')
#     address = data.get('address')
#     gender = data.get('gender')
#     email = data.get('email')
#     phone = data.get('phone')
#     datehired = data.get('dateHired')
#     role = "Admin"
#
#     cursor.execute("SELECT nid FROM employee WHERE nid = %s", (NID,))
#     user_exists = cursor.fetchone()
#     if user_exists:  # user with that nid already has an acc
#         return jsonify({"error": "User already exists"}), 400
#     else:
#         query = """INSERT INTO employee (nid, role, username, password, firstname, lastname, dateofbirth, address, gender, emailaddress, phonenumber, datehired)
#                                        VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                                        """
#
#         params = (
#             NID, role, username, password, firstname, lastname, dateofbirth, address, gender, email, phone,
#             datehired)
#
#         return execute_query(query, params)
#
#
# #
# # try:
# #     os.makedirs(app.instance_path)
# # except OSError:
# #     pass
# #
# # @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return 'No file part'
#     file = request.files['file']
#     if file.filename == '':
#         return 'No selected file'
#     if file:
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(register.instance_path, 'static/images', filename))
#         return 'File saved successfully'
#




