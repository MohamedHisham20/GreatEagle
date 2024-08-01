from flask import Blueprint, request, jsonify
from flask_cors import CORS
from database import Users, dict_factory, Advertisers, Campaigns
from extensions import bcrypt
from flask_login import login_user, current_user, logout_user, login_required

home = Blueprint("home", __name__, static_folder="static")
CORS(home)

#create a route to retreive all ads in the db
@home.route('/home/allCampaigns', methods=['GET'])
def all_Campaigns():
    campaigns = Campaigns.query.all()
    return jsonify({"ads": dict_factory(campaigns)}), 200

#create a route to retreive specific ad in the db
@home.route('/home/getCampaign', methods=['POST'])
def get_campaign():
    data = request.json
    campaign_id = data.get('campaign_id')
    campaign = Campaigns.query.filter_by(id=campaign_id).first()

    if not campaign:
        return jsonify({"error": "Ad does not exist"}), 400
    return jsonify({"ad": dict_factory(campaign)}), 200
