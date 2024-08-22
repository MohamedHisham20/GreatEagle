from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_cors import CORS
from database import Users, dict_factory, Advertisers, Campaigns, Ad_Impressions, db, Campaign_Locations, \
    Campaign_Images, Campaign_Videos
from flask_login import current_user, logout_user, login_required

home = Blueprint("home", __name__, static_folder="static")
CORS(home)


#create a route to retreive popular ads in the db (campaigns with offers)
@home.route('/home/popularCampaigns', methods=['GET'])
def popular_Campaigns():
    campaigns = Campaigns.query.filter(Campaigns.offer.isnot(None)).all()
    campaigns_dict = []
    #get the campaigns' locations and images
    for campaign in campaigns:
        campaign_locations = Campaign_Locations.get_locations(campaign.id)
        campaign_images = Campaign_Images.get_images(campaign.id)
        #get the advertiser of the campaign
        advertiser = Advertisers.query.filter_by(id=campaign.advertiser_id).first()
        #get campaign videos
        campaign_videos = Campaign_Videos.get_videos(campaign.id)
        campaign = dict_factory(campaign)
        campaign['locations'] = campaign_locations
        campaign['images'] = campaign_images
        campaign['advertiser'] = dict_factory(advertiser)
        campaign['videos'] = campaign_videos
        campaigns_dict.append(campaign)
    return jsonify({"campaigns": campaigns_dict}), 200


#create a route to retreive normal ads in the db (campaigns without offers)
@home.route('/home/normalCampaigns', methods=['GET'])
def normal_Campaigns():
    campaigns = Campaigns.query.filter(Campaigns.offer.is_(None)).all()
    campaigns_dict = []
    # get the campaigns' locations and images
    for campaign in campaigns:
        campaign_locations = Campaign_Locations.get_locations(campaign.id)
        campaign_images = Campaign_Images.get_images(campaign.id)
        # get the advertiser of the campaign
        advertiser = Advertisers.query.filter_by(id=campaign.advertiser_id).first()
        # get campaign videos
        campaign_videos = Campaign_Videos.get_videos(campaign.id)
        campaign = dict_factory(campaign)
        campaign['locations'] = campaign_locations
        campaign['images'] = campaign_images
        campaign['advertiser'] = dict_factory(advertiser)
        campaign['videos'] = campaign_videos
        campaigns_dict.append(campaign)
    return jsonify({"campaigns": campaigns_dict}), 200


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
    #get the campaign's locations and images
    campaign_locations = Campaign_Locations.get_locations(campaign.id)
    campaign_images = Campaign_Images.get_images(campaign.id)
    #get campaign videos
    campaign_videos = Campaign_Videos.get_videos(campaign.id)
    campaign = dict_factory(campaign)
    campaign['locations'] = campaign_locations
    campaign['images'] = campaign_images
    campaign['advertiser'] = dict_factory(advertiser)
    campaign['videos'] = campaign_videos

    #add to the impression that the user entered the ad
    new_impression = Ad_Impressions(campaign_id=campaign_id, user_id=current_user.id, impression_date=datetime.now())
    db.session.add(new_impression)
    db.session.commit()

    return jsonify({"ad": campaign, "advertiser": dict_factory(advertiser)}), 200
