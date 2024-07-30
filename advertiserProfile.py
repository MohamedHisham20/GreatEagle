from database import db, Advertisers, Advertiser_Phones, Advertiser_Locations, Campaigns
from extensions import bcrypt
from flask import request, jsonify, Blueprint
from flask_cors import CORS


advertiser = Blueprint("advertiserProfile", __name__, static_folder="static")
# CORS(register, resources={
#     r"/*": {"origins": "http://localhost:3000"}})  # Allow CORS for the login blueprint (Cross-Origin Resource Sharing

@advertiser.route('/advertiser/getInfo', methods=['POST'])
def get_info():     # get advertiser info (remaining the campaign info)
    data = request.json
    advertiser_id = data.get('advertiser_id')
    advertiser = Advertisers.query.filter_by(advertiser_id=advertiser_id).first()

    if not advertiser:
        return jsonify({"error": "Advertiser does not exist"}), 400
    # get advertiser phones
    advertiser_phones = Advertiser_Phones.query.filter_by(advertiser_id=advertiser_id).all()
    advertiser_locations = Advertiser_Locations.query.filter_by(advertiser_id=advertiser_id).all()
    advertiser_phones = [phone.to_dict() for phone in advertiser_phones]
    advertiser_locations = [location.to_dict() for location in advertiser_locations]
    advertiser = advertiser.to_dict()
    advertiser['phones'] = advertiser_phones
    advertiser['locations'] = advertiser_locations
    return jsonify({"advertiser": advertiser}), 200

@advertiser.route('/advertiser/addCampaign', methods=['POST'])
def add_campaign():
    data = request.json
    advertiser_id = data.get('advertiser_id')
    campaign_name = data.get('campaign_name')
    campaign_description = data.get('campaign_description')
    campaign_start_date = data.get('campaign_start_date')
    campaign_end_date = data.get('campaign_end_date')
    campaign_budget = data.get('campaign_budget')
    campaign_type = data.get('campaign_type')
    campaign_image = data.get('campaign_image')
    campaign = Campaigns.query.filter_by(campaign_name=campaign_name).first()

    if campaign:
        return jsonify({"error": "Campaign already exists"}), 400

    new_campaign = Campaigns(advertiser_id=advertiser_id, campaign_name=campaign_name, campaign_description=campaign_description, campaign_start_date=campaign_start_date, campaign_end_date=campaign_end_date, campaign_budget=campaign_budget, campaign_type=campaign_type, campaign_image=campaign_image)
    db.session.add(new_campaign)
    db.session.commit()

    return jsonify({"message": "Campaign created successfully"}), 201

@advertiser.route('/advertiser/editCampaign', methods=['POST'])
def edit_campaign():
    data = request.json
    campaign_id = data.get('campaign_id')
    advertiser_id = data.get('advertiser_id')
    campaign_name = data.get('campaign_name')
    campaign_description = data.get('campaign_description')
    campaign_start_date = data.get('campaign_start_date')
    campaign_end_date = data.get('campaign_end_date')
    campaign_budget = data.get('campaign_budget')
    campaign_type = data.get('campaign_type')
    campaign_image = data.get('campaign_image')
    campaign = Campaigns.query.filter_by(campaign_id=campaign_id).first()

    if not campaign:
        return jsonify({"error": "Campaign does not exist"}), 400

    campaign.advertiser_id = advertiser_id
    campaign.campaign_name = campaign_name
    campaign.campaign_description = campaign_description
    campaign.campaign_start_date = campaign_start_date
    campaign.campaign_end_date = campaign_end_date
    campaign.campaign_budget = campaign_budget
    campaign.campaign_type = campaign_type
    campaign.campaign_image = campaign_image
    db.session.commit()

    return jsonify({"message": "Campaign updated successfully"}), 200

@advertiser.route('/advertiser/deleteCampaign', methods=['POST'])
def delete_campaign():
    data = request.json
    campaign_id = data.get('campaign_id')
    campaign = Campaigns.query.filter_by(campaign_id=campaign_id).first()

    if not campaign:
        return jsonify({"error": "Campaign does not exist"}), 400

    db.session.delete(campaign)
    db.session.commit()

    return jsonify({"message": "Campaign deleted successfully"}), 200

@advertiser.route('/advertiser/getCampaigns', methods=['GET'])
def get_campaigns():
    campaigns = Campaigns.query.all()
    return jsonify({"campaigns": [campaign.to_dict() for campaign in campaigns]}), 200

@advertiser.route('/advertiser/getCampaign', methods=['POST'])
def get_campaign():
    data = request.json
    campaign_id = data.get('campaign_id')
    campaign = Campaigns.query.filter_by(campaign_id=campaign_id).first()

    if not campaign:
        return jsonify({"error": "Campaign does not exist"}), 400

    return jsonify({"campaign": campaign.to_dict()}), 200

@advertiser.route('/advertiser/editAdvertiser', methods=['POST'])
def edit_advertiser():
    data = request.json
    advertiser_id = data.get('advertiser_id')
    company_name = data.get('company_name')
    advertiser_name = data.get('advertiser_name')
    contact_email = data.get('contact_email')
    advertiser_type = data.get('advertiser_type')
    about = data.get('about')
    visa_number = data.get('visa_number')
    advertiser = Advertisers.query.filter_by(advertiser_id=advertiser_id).first()

    if not advertiser:
        return jsonify({"error": "Advertiser does not exist"}), 400

    advertiser.company_name = company_name
    advertiser.advertiser_name = advertiser_name
    advertiser.contact_email = contact_email
    advertiser.advertiser_type = advertiser_type
    advertiser.about = about
    advertiser.visa_number = visa_number
    db.session.commit()

    return jsonify({"message": "Advertiser updated successfully"}), 200