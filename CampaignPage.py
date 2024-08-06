from flask import Blueprint, request, jsonify
from flask_cors import CORS
from database import Users, dict_factory, Advertisers, Campaigns, Ad_Impressions, db, Wishlist
from flask_login import login_user, current_user, logout_user, login_required

campaign_page = Blueprint("campaign_page", __name__, static_folder="static")
CORS(campaign_page)


# create a route to check if user took offer or not
@campaign_page.route('/campaign_page/check_offer', methods=['POST'])
def check_offer():
    data = request.json
    user_id = data.get('user_id')
    campaign_id = data.get('campaign_id')
    #check in the ad_impression whether the last impression took the offer or not
    user_impression = Ad_Impressions.query.filter_by(user_id=user_id, campaign_id=campaign_id).order_by(
        Ad_Impressions.impression_date.desc()).first()
    if not user_impression:
        return jsonify({"error": "User impression not found"}), 400
    else:
        #check the take offer boolean
        if user_impression.took_offer:
            return jsonify({"message": "Offer already taken"}), 400
        else:
            return jsonify({"message": "User can take offer"}), 200


# create a route to take the offer
@campaign_page.route('/campaign_page/take_offer', methods=['POST'])
def take_offer():
    data = request.json
    user_id = data.get('user_id')
    campaign_id = data.get('campaign_id')
    #check in the ad_impression whether the last impression took the offer or not
    user_impression = Ad_Impressions.query.filter_by(user_id=user_id, campaign_id=campaign_id).order_by(
        Ad_Impressions.impression_date.desc()).first()
    if not user_impression:
        return jsonify({"error": "User impression not found"}), 400
    else:
        #check the take offer boolean
        if user_impression.took_offer:
            return jsonify({"message": "Offer already taken"}), 400
        else:
            user_impression.took_offer = True
            db.session.commit()
            return jsonify({"message": "Offer taken successfully"}), 200


# add to wishlist
@campaign_page.route('/campaign_page/add_to_wishlist', methods=['POST'])
def add_to_wishlist():
    data = request.json
    user_id = data.get('user_id')
    campaign_id = data.get('campaign_id')
    #check in the ad_impression whether the last impression took the offer or not
    campaign = Wishlist.query.filter_by(user_id=user_id, campaign_id=campaign_id).first()
    if campaign:
        #remove from wishlist
        db.session.delete(campaign)
        db.session.commit()
        return jsonify({"message": "Campaign removed from wishlist successfully"}), 200
    else:
        new_wishlist = Wishlist(user_id=user_id, campaign_id=campaign_id)
        db.session.add(new_wishlist)
        db.session.commit()
        return jsonify({"message": "Campaign added to wishlist successfully"}), 200
