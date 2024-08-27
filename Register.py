import vercel_blob
from database import Users, db, Advertisers, Advertiser_Phones, Advertiser_Locations, get_advertiser_image, \
    generate_referral_code
from extensions import bcrypt
from flask import request, jsonify, Blueprint, json
from flask_cors import CORS

register = Blueprint("register", __name__, static_folder="static")
CORS(register)

#get advertiser by id
@register.route('/get_advertiser', methods=['POST'])
def get_advertiser():
    data = request.json
    advertiser_id = data.get('id')
    advertiser = Advertisers.query.filter_by(id=advertiser_id).first()
    #return the advertiser data and its image from get_advertiser_image function
    return jsonify({"advertiser": advertiser.to_dict()}), 200


#register route using sqlalchemy and add the user into the database
@register.route('/register', methods=['POST'])
def register_1():
    data = json.loads(request.form['data'])
    role = data.get('role')
    password = data.get('password')
    #hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    image = request.files.get('image')
    if image:
        # upload the image to the cloudinary
        resp = vercel_blob.put(image.filename, image.read())
        # get the image url
        image_url = resp.get('url')
    else:
        image_url = None

    if role == 'user':
        username = data.get('username')
        name = data.get('name')
        age = data.get('age')
        email = data.get('email')
        referral_code = None
        check_referral_code = data.get('referral_code')


        #check if email and password are provided
        if not email or not password:
            return jsonify({"error": "Please provide both email and password"}), 400

        user = Users.query.filter_by(email=email).first()
        #check if user exists in the db
        if user:
            return jsonify({"error": "User already exists"}), 400

        #add the user to the database
        new_user = Users(username=username, password=hashed_password, name=name, age=age,
                         email=email, profile_pic=image_url)
        db.session.add(new_user)
        user_id = new_user.id
        if check_referral_code != "":
            referral_code = generate_referral_code(user_id)
            new_user.referral_code = referral_code
        db.session.commit()
        #get the user id
            # db.session.commit()

        return jsonify({"message": "User created successfully"}), 201

    elif role == 'advertiser':
        company_name = data.get('name')
        advertiser_name = data.get('username')
        contact_email = data.get('email')
        about = data.get('about')
        visa = data.get('visa')
        referral_code = data.get('referral_code')
        advertiser_phones = data.get('advertiser_phones')
        advertiser_location = data.get('advertiser_location')
        advertiser_type = data.get('advertiser_type')
        advertiser = Advertisers.query.filter_by(contact_email=contact_email).first()

        #check if advertiser exists in the db
        if advertiser:
            return jsonify({"error": "Advertiser already exists"}), 400

        #add the advertiser to the database
        new_advertiser = Advertisers(company_name=company_name, advertiser_name=advertiser_name,
                                     contact_email=contact_email,
                                     password=hashed_password, about=about, visa_number=visa,
                                     advertiser_type=advertiser_type, referral_code=referral_code,
                                     advertiser_pic=image_url)

        db.session.add(new_advertiser)
        db.session.commit()
        #get the new added advertiser id to use it in the advertiser_phones table
        advertiser_id = new_advertiser.id
        #add the advertiser phones to the database
        for phone in advertiser_phones:
            new_phone = Advertiser_Phones(advertiser_id=advertiser_id, phone=phone)
            db.session.add(new_phone)
            # db.session.commit()
        #add the advertiser location to the database
        for location in advertiser_location:
            new_location = Advertiser_Locations(advertiser_id=advertiser_id, location=location)
            db.session.add(new_location)
        db.session.commit()
        return jsonify({"message": "Advertiser created successfully"}), 201


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
#route to upload images to db
# @register.route('/upload', methods=['POST'])
# def upload_image():
#     img = request.files['image']
#     data = json.loads(request.form['id'])
#     id = data.get('id')
#     image = Image.open(img)
#     image.save('compressed_image.jpg', 'JPEG', quality=40)
#     with open('compressed_image.jpg', 'rb') as file:
#         binary_image = file.read()
#     #insert the image to the database for advertiser with id 1
#     advertiser = Advertisers.query.filter_by(id=id).first()
#     advertiser.advertiser_pic = binary_image
#     db.session.commit()
#
#     return jsonify({"message": "Image uploaded successfully"}), 200


#route to get the image from the db
# @register.route('/get_image', methods=['GET'])
# def get_image():
#     advertiser = Advertisers.query.filter_by(id=1).first()
#     #convert the image from binary to image
#     with open('image.jpg', 'wb') as file:
#         file.write(advertiser.advertiser_pic)
#     #return the image to display in the frontend
#     return send_file('image.jpg', mimetype='image/jpg')
#     # return Response(advertiser.advertiser_pic, mimetype='image/jpg')