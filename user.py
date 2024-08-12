import vercel_blob

from database import db, Advertisers, Campaigns, dict_factory, Wishlist, Campaign_Images, Ad_Impressions, \
    Advertiser_Phones
from flask import request, jsonify, Blueprint, json
from flask_cors import CORS

user = Blueprint("user", __name__, static_folder="static")
CORS(user)


#get the wishlist of the user
@user.route('/user/get_wishlist', methods=['POST'])
def get_wishlist():
    data = request.json
    user_id = data.get('user_id')
    wishlist = Wishlist.query.filter_by(user_id=user_id).all()
    wishlist_dict = []
    for item in wishlist:
        campaign = Campaigns.query.filter_by(id=item.campaign_id).first()
        # get the campaign images
        campaign_images = Campaign_Images.get_images(campaign.id)
        advertiser = Advertisers.query.filter_by(id=campaign.advertiser_id).first()
        campaign = dict_factory(campaign)
        advertiser = dict_factory(advertiser)
        campaign['advertiser'] = advertiser
        campaign['images'] = campaign_images
        wishlist_dict.append(campaign)
    return jsonify({"wishlist": wishlist_dict}), 200


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
        # get the campaign images
        campaign_images = Campaign_Images.get_images(campaign.id)
        # advertiser = Advertisers.query.filter_by(id=campaign.advertiser_id).first()
        campaign = dict_factory(campaign)
        # advertiser = dict_factory(advertiser)
        # campaign['advertiser'] = advertiser
        campaign['images'] = campaign_images
        viewed_ads_dict.append(campaign)
    return jsonify({"recently_viewed": viewed_ads_dict}), 200


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
    viewed_ads_dict = []
    for item in viewed_ads:
        campaign = Campaigns.query.filter_by(id=item.campaign_id).first()
        # get the campaign images
        campaign_images = Campaign_Images.get_images(campaign.id)
        advertiser = Advertisers.query.filter_by(id=campaign.advertiser_id).first()
        campaign = dict_factory(campaign)
        advertiser = dict_factory(advertiser)
        campaign['advertiser'] = advertiser
        campaign['images'] = campaign_images
        viewed_ads_dict.append(campaign)
    return jsonify({"used_offers": viewed_ads_dict}), 200


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
