# #testing the database using sqlalchmey
# from database import db, Users, Advertisers
# from app import app
#
# #testing the login function with enum
# with app.app_context():
#     data = {
#         "email": "H@gmail.com",
#         "password":"H2003",
#         "role":"advertiser"
#     }
#     email = data.get('email')
#     password = data.get('password')
#     role = data.get('role')
#     # check if email and password are provided
#     if not email or not password:
#         print({"error": "Please provide both email and password"}), 400
#     # check if user or advertiser exists in the db
#     if role == 'user':
#         user = Users.query.filter_by(email=email).first()
#     elif role == 'advertiser':
#         user = Advertisers.query.filter_by(contact_email=email).first()
#     else:
#         print({"error": "Role not found"}), 400
#
#     if user:
#         print(f"User found: {user}")
#         print(f"User type: {type(user)}")
#         if hasattr(user, 'advertiser_type'):
#             print(f"Advertiser type: {user.advertiser_type}")

# check if user exists and password is correct
# if user and bcrypt.check_password_hash(user.password, password):
#     # Successful login
#     login_user(user, remember=True)
#     return jsonify({"message": "Login successful", "user": dict_factory(user)}), 200
# else:
#     return jsonify({'Login Unsuccessful. Please check email and password'}), 401

import uuid

# def generate_referral_code():
#     return str(uuid.uuid3(uuid.NAMESPACE_DNS, '2'))
#     return str(uuid.uuid4())
# print(generate_unique_id()) # 4b1e1b3b-0b3b-4b1e-8b1b-0b3b4b1e1b3b
