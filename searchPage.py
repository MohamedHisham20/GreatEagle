from flask import Blueprint, request, jsonify
from flask_cors import CORS
from database import dict_factory, Advertisers, Campaigns, db, Campaign_Locations, Campaign_Images

search_page = Blueprint("search_page", __name__, static_folder="static")
CORS(search_page)


# create a route to search for ads
@search_page.route('/search_page/search', methods=['POST'])
def search():
    data = request.json
    search = data.get('search')
    # search for the campaign
    campaigns = db.session.query(Campaigns).join(Advertisers).filter(
        (Campaigns.campaign_name.ilike(f'%{search}%')) |
        (Advertisers.advertiser_name.ilike(f'%{search}%')) | (Advertisers.company_name.ilike(f'%{search}%'))
    ).all()
    if not campaigns:
        return jsonify({"error": "No campaigns found"}), 400
    # get the campaigns' locations and images
    campaigns_dict = []
    for campaign in campaigns:
        campaign_locations = Campaign_Locations.get_locations(campaign.id)
        campaign_images = Campaign_Images.get_images(campaign.id)
        campaign = dict_factory(campaign)
        campaign['locations'] = campaign_locations
        campaign['images'] = campaign_images
        campaigns_dict.append(campaign)
    return jsonify({"campaigns": campaigns_dict}), 200
