from flask import Blueprint, request, jsonify
from flask_cors import CORS
from database import Users, dict_factory, Advertisers, Campaigns, Ad_Impressions, db, Wishlist
from flask_login import login_user, current_user, logout_user, login_required

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
    return jsonify({"campaigns": dict_factory(campaigns)}), 200
