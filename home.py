from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_cors import CORS
from database import Users, dict_factory, Advertisers, Campaigns, Ad_Impressions, db
from extensions import bcrypt
from flask_login import login_user, current_user, logout_user, login_required

home = Blueprint("home", __name__, static_folder="static")
CORS(home)


#create a route to retreive popular ads in the db (campaigns with offers)
@home.route('/home/popularCampaigns', methods=['GET'])
def popular_Campaigns():
    campaigns = Campaigns.query.filter(Campaigns.offer.isnot(None)).all()
    return jsonify({"campaigns": dict_factory(campaigns)}), 200


#create a route to retreive normal ads in the db (campaigns without offers)
@home.route('/home/normalCampaigns', methods=['GET'])
def normal_Campaigns():
    campaigns = Campaigns.query.filter(Campaigns.offer.is_(None)).all()
    return jsonify({"campaigns": dict_factory(campaigns)}), 200


#create a route to retreive specific ad in the db
@home.route('/home/getCampaign', methods=['POST'])
def get_campaign():
    data = request.json
    campaign_id = data.get('campaign_id')
    campaign = Campaigns.query.filter_by(id=campaign_id).first()

    if not campaign:
        return jsonify({"error": "Ad does not exist"}), 400
    #get the advertiser of the campaign
    advertiser = Advertisers.query.filter_by(id=campaign.advertiser_id).first()

    #add to the impression that the user entered the ad
    new_impression = Ad_Impressions(campaign_id=campaign_id, user_id=current_user.id, impression_date=datetime.now())
    db.session.add(new_impression)
    db.session.commit()

    return jsonify({"ad": dict_factory(campaign), "advertiser": dict_factory(advertiser)}), 200
