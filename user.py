import vercel_blob

from database import db, Advertisers, Campaigns, dict_factory, User_Wishlist, Campaign_Images, Ad_Impressions, \
    Advertiser_Phones, Users, check_data, Ad_Clicks, Campaign_Locations, Campaign_Videos, Advertiser_Wishlist
from flask import request, jsonify, Blueprint, json
from flask_cors import CORS

from extensions import bcrypt

user = Blueprint("user", __name__, static_folder="static")
CORS(user)


#get the wishlist of the user
@user.route('/user/get_wishlist', methods=['POST'])
def get_wishlist():
    data = request.json
    user_id = data.get('user_advertiser_id')
    role = data.get('role')
    if not user_id:
        #return unauthorized if the user is not logged in
        return jsonify({"error": "Unauthorized"}), 401
    if role == 'user':
        wishlist = User_Wishlist.query.filter_by(user_id=user_id).all()
    else:
        wishlist = Advertiser_Wishlist.query.filter_by(advertiser_id=user_id).all()
    wishlist_dict = []
    # get the campaigns' locations and images
    for item in wishlist:
        campaign_locations = Campaign_Locations.get_locations(item.campaign_id)
        campaign_images = Campaign_Images.get_images(item.campaign_id)
        # get the campaign with campaign id
        campaign = Campaigns.query.filter_by(id=item.campaign_id).first()
        #get the campaign videos
        campaign_videos = Campaign_Videos.get_videos(campaign.id)
        advertiser = Advertisers.query.filter_by(id=campaign.advertiser_id).first()
        campaign = dict_factory(campaign)
        campaign['locations'] = campaign_locations
        campaign['images'] = campaign_images
        campaign['advertiser'] = dict_factory(advertiser)
        campaign['videos'] = campaign_videos
        wishlist_dict.append(campaign)
    return jsonify({"campaigns": wishlist_dict}), 200


#recently viewed ads
@user.route('/user/recently_viewed', methods=['POST'])
def recently_viewed():
    data = request.json
    user_id = data.get('user_id')
    #get the last 5 viewed ads
    viewed_ads = Ad_Impressions.query.filter_by(user_id=user_id).order_by(
        Ad_Impressions.campaign_id, Ad_Impressions.impression_date.desc()).distinct(
        Ad_Impressions.campaign_id).limit(
        5).all()
    viewed_ads_dict = []
    for item in viewed_ads:
        campaign = Campaigns.query.filter_by(id=item.campaign_id).first()
        campaign_locations = Campaign_Locations.get_locations(item.campaign_id)
        # get the campaign images
        campaign_images = Campaign_Images.get_images(campaign.id)
        #get campaign videos
        campaign_videos = Campaign_Videos.get_videos(campaign.id)
        advertiser = Advertisers.query.filter_by(id=campaign.advertiser_id).first()
        campaign = dict_factory(campaign)
        advertiser = dict_factory(advertiser)
        campaign['advertiser'] = advertiser
        campaign['images'] = campaign_images
        campaign['locations'] = campaign_locations
        campaign['videos'] = campaign_videos
        viewed_ads_dict.append(campaign)
    return jsonify({"campaigns": viewed_ads_dict}), 200


#used offers by the user
@user.route('/user/used_offers', methods=['POST'])
def used_offers():
    data = request.json
    user_id = data.get('user_id')
    #get the last 5 viewed ads
    viewed_ads = Ad_Impressions.query.filter_by(user_id=user_id, took_offer=True).order_by(
        Ad_Impressions.campaign_id, Ad_Impressions.impression_date.desc()).distinct(
        Ad_Impressions.campaign_id).limit(
        5).all()
    # no ads found
    if not viewed_ads:
        return jsonify({"message": "No offers used"}), 200
    viewed_ads_dict = []
    for item in viewed_ads:
        campaign = Campaigns.query.filter_by(id=item.campaign_id).first()
        campaign_locations = Campaign_Locations.get_locations(item.campaign_id)
        # get the campaign images
        campaign_images = Campaign_Images.get_images(campaign.id)
        #get campaign videos
        campaign_videos = Campaign_Videos.get_videos(campaign.id)
        advertiser = Advertisers.query.filter_by(id=campaign.advertiser_id).first()
        campaign = dict_factory(campaign)
        advertiser = dict_factory(advertiser)
        campaign['locations'] = campaign_locations
        campaign['advertiser'] = advertiser
        campaign['images'] = campaign_images
        campaign['videos'] = campaign_videos
        viewed_ads_dict.append(campaign)
    return jsonify({"campaigns": viewed_ads_dict}), 200


#user contact advertiser
@user.route('/user/contact_advertiser', methods=['POST'])
def contact_advertiser():
    data = request.json
    campaign_id = data.get('campaign_id')

    #get the advertiser of the campaign
    campaign = Campaigns.query.filter_by(id=campaign_id).first()
    advertiser = Advertisers.query.filter_by(id=campaign.advertiser_id).first()

    #get advertiser email and phone
    email = advertiser.contact_email
    phone = Advertiser_Phones.get_phones(advertiser.id)
    return jsonify({"email": email, "phone": phone}), 200


#edit user profile
@user.route('/user/edit_profile', methods=['POST'])
def edit_profile():
    data = json.loads(request.form['data'])
    user_id = data.get('user_id')
    user = Users.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 400
    user_image = request.files['image'] if 'image' in request.files else None

    if user_image:
        # upload the image to the cloudinary
        resp = vercel_blob.put(user_image.filename, user_image.read())
        # get the image url
        profile_pic = resp.get('url')
        #remove old pic if there's new one
        if user.profile_pic:
            vercel_blob.delete(user.profile_pic)
        #add the new pic to the user profile
        user.profile_pic = profile_pic

    #update the user profile
    user.username = check_data(user.username, data.get('username'))
    user.name = check_data(user.name, data.get('name'))
    user.age = check_data(user.age, data.get('age'))
    user.email = check_data(user.email, data.get('email'))
    #hash the password if given
    password = data.get('password')
    if password:
        #hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user.password = check_data(user.password, hashed_password)
    db.session.commit()
    return jsonify({"message": "User profile updated successfully"}), 200


#delete user profile
@user.route('/user/delete_profile', methods=['POST'])
def delete_profile():
    data = request.json
    user_id = data.get('user_id')
    user = Users.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 400
    #remove the user profile pic
    if user.profile_pic:
        vercel_blob.delete(user.profile_pic)
    #delete the user impressions
    Ad_Impressions.query.filter_by(user_id=user_id).delete()
    #delete the user wishlist
    User_Wishlist.query.filter_by(user_id=user_id).delete()
    #delete ad clicks
    Ad_Clicks.query.filter_by(user_id=user_id).delete()

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User profile deleted successfully"}), 200

##################### add the follow advertiser logic #####################
