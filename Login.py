from flask import Blueprint, request, jsonify
from flask_cors import CORS
from database import Users, dict_factory, Advertisers, User_Wishlist, Advertiser_Wishlist
from extensions import bcrypt
from flask_login import login_user, logout_user

login = Blueprint("login", __name__, static_folder="static")
CORS(login)


#create api for a mobile app
#login route
@login.route('/login', methods=['POST', 'GET'])
def login_view():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    #check if email and password are provided
    if not email or not password:
        return jsonify({"error": "Please provide both email and password"}), 400
    #check if user or advertiser exists in the db
    if role == 'user':
        user = Users.query.filter_by(email=email).first()
    elif role == 'advertiser':
        user = Advertisers.query.filter_by(contact_email=email).first()
    else:
        return jsonify({"error": "Role not found"}), 400

    #check if user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, password):
        #Successful login
        login_user(user, remember=True)
        #add the wishlist of the user
        user_id = user.id
        #get the user's wishlist
        if role == 'user':
            wishlist = User_Wishlist.query.filter_by(user_id=user_id).all()
        else:
            wishlist = Advertiser_Wishlist.query.filter_by(advertiser_id=user_id).all()

        wishlist_dict = []
        if wishlist:
            # get the campaigns' locations and images
            for item in wishlist:
                wishlist_dict.append(item.campaign_id)
        #add the role to the dictionary
        user = dict_factory(user)
        user['role'] = role
        user['wishlist'] = wishlist_dict
        return jsonify({"message": "Login successful", "person": user}), 200
    else:
        return jsonify({"error": 'Login Unsuccessful. Please check email and password'}), 401


# logout route
@login.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200


@login.route('/users', methods=['GET'])
def users():
    userss = Users.query.all()
    return jsonify({"users": dict_factory(userss)}), 200
