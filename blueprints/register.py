
# import os
#
# from flask import request, jsonify, Blueprint
# from flask_cors import CORS
# from werkzeug.utils import secure_filename
#
# from database import cursor, database_session as conn, execute_query
#
# register = Blueprint("register", __name__, static_folder="static", template_folder="templates")
# # CORS(register, resources={
# #     r"/*": {"origins": "http://localhost:3000"}})  # Allow CORS for the login blueprint (Cross-Origin Resource Sharing
#
# """
# @register.route('/register', methods=['POST'])
# def register_1():
#
# """
#
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
#
#
#
#
