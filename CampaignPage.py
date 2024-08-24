from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_cors import CORS
from sqlalchemy import select, func, alias

from database import Campaigns, Ad_Impressions, db, User_Wishlist, Ad_Clicks, Advertiser_Wishlist

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
    advertiser_id = data.get('qr_advertiser_id')  #qr output
    #check in the ad_impression whether the last impression took the offer or not
    #check the advertiser has the campaign id that we give it
    check_campaign = Campaigns.query.filter_by(advertiser_id=advertiser_id, id=campaign_id).first()
    if not check_campaign:
        return jsonify({"error": "Campaign not found"}), 400

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
    user_advertiser_id = data.get('user_advertiser_id')
    campaign_id = data.get('campaign_id')
    role = data.get('role')
    if role == 'advertiser':
        campaign = Advertiser_Wishlist.query.filter_by(advertiser_id=user_advertiser_id, campaign_id=campaign_id).first()
        if campaign:
            # remove from wishlist
            db.session.delete(campaign)
            db.session.commit()
            return jsonify({"message": "Campaign removed from the wishlist"}), 200
        new_wishlist = Advertiser_Wishlist(advertiser_id=user_advertiser_id, campaign_id=campaign_id)
        db.session.add(new_wishlist)
        db.session.commit()
        return jsonify({"message": "Campaign added to the wishlist"}), 201
    else:
        #check in the ad_impression whether the last impression took the offer or not
        campaign = User_Wishlist.query.filter_by(user_id=user_advertiser_id, campaign_id=campaign_id).first()
        if campaign:
            #remove from wishlist
            db.session.delete(campaign)
            db.session.commit()
            return jsonify({"message": "Campaign removed from wishlist successfully"}), 200
        else:
            new_wishlist = User_Wishlist(user_id=user_advertiser_id, campaign_id=campaign_id)
            db.session.add(new_wishlist)
            db.session.commit()
            return jsonify({"message": "Campaign added to wishlist successfully"}), 201


# add link pressed to the ad_clicks
@campaign_page.route('/campaign_page/link_pressed', methods=['POST'])
def link_pressed():
    data = request.json
    user_id = data.get('user_id')
    campaign_id = data.get('campaign_id')
    link = data.get('link')
    #check in the ad_impression whether the last impression took the offer or not
    new_click = Ad_Clicks(ad_campaign_id=campaign_id, user_id=user_id, click_date=datetime.now(), link_pressed=link)
    db.session.add(new_click)
    db.session.commit()
    return jsonify({"message": "Link pressed successfully"}), 200


# get the most pressed links in the campaign when the campaign is over
@campaign_page.route('/campaign_page/most_pressed_links', methods=['POST'])
def most_pressed_links():
    data = request.json
    campaign_id = data.get('campaign_id')
    #check if the campaign is over
    campaign = Campaigns.query.filter_by(id=campaign_id).first()
    if not campaign:
        return jsonify({"error": "Campaign not found"}), 400
    if campaign.end_date > datetime.now().date():
        return jsonify({"error": "Campaign is not over yet"}), 400

    #check if the campaign has a winner
    if campaign.winner:
        #get the winner
        return jsonify({"winner": campaign.winner}), 200

    # get the user that pressed the most unique links in the campaign between the start and end date when the end date is passed
    # Subquery to get total clicks per user
    subq = (
        select(Ad_Clicks.user_id, func.count(Ad_Clicks.link_pressed).label("total_clicks"))
        .where(Ad_Clicks.ad_campaign_id == campaign_id)
        .group_by(Ad_Clicks.user_id)
    )

    # Alias the subquery for clarity
    subq = alias(subq)

    # Get the maximum total clicks
    max_clicks = (
        select(func.max(subq.c.total_clicks))
        .select_from(subq)
    ).scalar_subquery()

    # Main query to get users with max clicks
    query = (
        select(Ad_Clicks.user_id, func.count(Ad_Clicks.link_pressed).label("total_clicks"))
        .where(Ad_Clicks.ad_campaign_id == 6)
        .group_by(Ad_Clicks.user_id)
        .having(func.count(Ad_Clicks.link_pressed) == max_clicks)
        .order_by(func.count(Ad_Clicks.link_pressed).desc())
    )

    results = db.session.execute(query).fetchall()
    if not results:
        return jsonify({"error": "No results found"}), 400
    results_dict = []
    for item in results:
        results_dict.append(item._asdict())

    # randomize the results and choose only one user
    import random
    random.shuffle(results_dict)
    # put it in the winner column in the campaign
    campaign.winner = results_dict[0]['user_id']
    db.session.commit()
    return jsonify({"the winner is": results_dict[0]}), 200