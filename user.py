import vercel_blob

from database import db, Advertisers, Campaigns, dict_factory, Wishlist, Campaign_Images
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