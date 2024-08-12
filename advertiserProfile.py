import vercel_blob

from database import db, Advertisers, Advertiser_Phones, Advertiser_Locations, Campaigns, dict_factory, \
    Campaign_Locations, Campaign_Images, Campaign_Videos, check_data
from extensions import bcrypt
from flask import request, jsonify, Blueprint, json
from flask_cors import CORS

advertiser = Blueprint("advertiserProfile", __name__, static_folder="static")
CORS(advertiser)


# CORS(register, resources={
#     r"/*": {"origins": "http://localhost:3000"}})  # Allow CORS for the login blueprint (Cross-Origin Resource Sharing


@advertiser.route('/advertiser/getInfo', methods=['POST'])
def get_info():  # get advertiser info (remaining the campaign info)
    data = request.json
    advertiser_id = data.get('advertiser_id')
    advertiser = Advertisers.query.filter_by(id=advertiser_id).first()

    if not advertiser:
        return jsonify({"error": "Advertiser does not exist"}), 400
    # get advertiser phones
    advertiser_phones = Advertiser_Phones.get_phones(advertiser_id)
    advertiser_locations = Advertiser_Locations.get_locations(advertiser_id)
    advertiser = advertiser.to_dict()
    advertiser['phones'] = advertiser_phones
    advertiser['locations'] = advertiser_locations
    return jsonify({"advertiser": advertiser}), 200


@advertiser.route('/advertiser/addCampaign', methods=['POST'])
def add_campaign():
    data = json.loads(request.form['data'])
    advertiser_id = data.get('advertiser_id')
    campaign_name = data.get('campaign_name')
    campaign_description = data.get('campaign_description')
    campaign_start_date = data.get('campaign_start_date')
    campaign_end_date = data.get('campaign_end_date')
    campaign_target_audience = data.get('campaign_target_audience')
    campaign_price = data.get('campaign_price')
    campaign_offer = data.get('campaign_offer')
    campaign_location = data.get('campaign_location')
    campaign_videos = data.get('campaign_videos')
    campaign_images = request.files.getlist("image")

    campaign = Campaigns.query.filter_by(campaign_name=campaign_name).first()
    if campaign:
        return jsonify({"error": "Campaign already exists"}), 400

    new_campaign = Campaigns(advertiser_id=advertiser_id, campaign_name=campaign_name,
                             description=campaign_description, start_date=campaign_start_date,
                             end_date=campaign_end_date, target_audience=campaign_target_audience,
                             price=campaign_price, offer=campaign_offer)
    db.session.add(new_campaign)
    db.session.commit()
    # get the campaign id
    campaign_id = new_campaign.id
    print(campaign_id)
    # add the campaign location to the database
    for location in campaign_location:
        new_location = Campaign_Locations(campaign_id=campaign_id, location=location)
        db.session.add(new_location)

    # add the campaign video URLs to the database
    for video in campaign_videos:
        new_video = Campaign_Videos(campaign_id=campaign_id, link=video)
        db.session.add(new_video)

    # add the campaign images to the database
    for c_image in campaign_images:
        # upload the image to the cloudinary
        resp = vercel_blob.put(c_image.filename, c_image.read())
        # get the image url
        image = resp.get('url')
        new_image = Campaign_Images(campaign_id=campaign_id, image=image)
        db.session.add(new_image)

    db.session.commit()
    return jsonify({"message": "Campaign created successfully"}), 201


@advertiser.route('/advertiser/editCampaign', methods=['POST'])
def edit_campaign():
    data = json.loads(request.form['data'])
    campaign_name = data.get('campaign_name')
    campaign_description = data.get('campaign_description')
    campaign_start_date = data.get('campaign_start_date')
    campaign_end_date = data.get('campaign_end_date')
    campaign_target_audience = data.get('campaign_target_audience')
    campaign_price = data.get('campaign_price')
    campaign_offer = data.get('campaign_offer')
    campaign_location = data.get('campaign_location')
    campaign_videos = data.get('campaign_videos')
    campaign_images = request.files.getlist("image")
    campaign_id = data.get('campaign_id')
    campaign = Campaigns.query.filter_by(id=campaign_id).first()

    if not campaign:
        return jsonify({"error": "Campaign does not exist"}), 400

    # update the campaign if the data is provided
    campaign.campaign_name = check_data(campaign.campaign_name, campaign_name)
    campaign.description = check_data(campaign.description, campaign_description)
    campaign.start_date = check_data(campaign.start_date, campaign_start_date)
    campaign.end_date = check_data(campaign.end_date, campaign_end_date)
    campaign.target_audience = check_data(campaign.target_audience, campaign_target_audience)
    campaign.price = check_data(campaign.price, campaign_price)
    campaign.offer = check_data(campaign.offer, campaign_offer)

    # add the campaign location to the database
    locations = Campaign_Locations.get_locations(campaign_id)
    for location in campaign_location:
        # update the location if it exists
        if location in locations:
            continue
        else:
            new_location = Campaign_Locations(campaign_id=campaign_id, location=location)
            db.session.add(new_location)
    # delete the old locations that are not in the new list
    for location in locations:
        if location not in campaign_location:
            deleted_location = Campaign_Locations.query.filter_by(campaign_id=campaign_id, location=location
                                                                  ).first()
            db.session.delete(deleted_location)

    # add the campaign video URLs to the database
    videos = Campaign_Videos.get_videos(campaign_id)
    for video in campaign_videos:
        # update the video if it exists
        if video in videos:
            continue
        else:
            new_video = Campaign_Videos(campaign_id=campaign_id, link=video)
            db.session.add(new_video)
    # delete the old videos that are not in the new list
    for video in videos:
        if video not in campaign_videos:
            deleted_video = Campaign_Videos.query.filter_by(campaign_id=campaign_id, link=video).first()
            db.session.delete(deleted_video)

    #delete the old images
    images = Campaign_Images.get_images(campaign_id)
    for image in images:
        deleted_image = Campaign_Images.query.filter_by(campaign_id=campaign_id, image=image).first()
        vercel_blob.delete(deleted_image.image)
        db.session.delete(deleted_image)

    # add the campaign images to the database
    for c_image in campaign_images:
        # upload the image to the cloudinary
        resp = vercel_blob.put(c_image.filename, c_image.read())
        # get the image url
        image = resp.get('url')
        new_image = Campaign_Images(campaign_id=campaign_id, image=image)
        db.session.add(new_image)
    db.session.commit()

    return jsonify({"message": "Campaign updated successfully"}), 200


@advertiser.route('/advertiser/deleteCampaign', methods=['POST'])
def delete_campaign():
    data = request.json
    campaign_id = data.get('campaign_id')
    campaign = Campaigns.query.filter_by(campaign_id=campaign_id).first()

    if not campaign:
        return jsonify({"error": "Campaign does not exist"}), 400

    #delete the campaign images
    images = Campaign_Images.get_images(campaign_id)
    for image in images:
        vercel_blob.delete(image)
        db.session.delete(image)

    #delete the campaign videos
    videos = Campaign_Videos.get_videos(campaign_id)
    for video in videos:
        db.session.delete(video)

    #delete the campaign locations
    locations = Campaign_Locations.get_locations(campaign_id)
    for location in locations:
        db.session.delete(location)

    db.session.delete(campaign)
    db.session.commit()

    return jsonify({"message": "Campaign deleted successfully"}), 200


@advertiser.route('/advertiser/getCampaigns', methods=['POST'])
def get_campaigns():
    #get all campaigns for a specific advertiser
    data = request.json
    advertiser_id = data.get('advertiser_id')
    campaigns = Campaigns.query.filter_by(advertiser_id=advertiser_id).all()
    # get the campaigns' images
    campaigns_dict = []
    for campaign in campaigns:
        campaign_images = Campaign_Images.get_images(campaign.id)
        campaign = dict_factory(campaign)
        campaign['images'] = campaign_images
        campaigns_dict.append(campaign)
    return jsonify({"campaigns": campaigns_dict}), 200


@advertiser.route('/advertiser/editAdvertiser', methods=['POST'])
def edit_advertiser():
    data = json.loads(request.form['data'])
    advertiser_id = data.get('advertiser_id')

    # get the advertiser from the database
    advertiser = Advertisers.query.filter_by(id=advertiser_id).first()

    if not advertiser:
        return jsonify({"error": "Advertiser does not exist"}), 400

    company_name = data.get('company_name')
    advertiser_name = data.get('advertiser_name')
    contact_email = data.get('contact_email')
    advertiser_type = data.get('advertiser_type')
    about = data.get('about')
    visa_number = data.get('visa')
    advertiser_phones = data.get('advertiser_phones')
    advertiser_locations = data.get('advertiser_locations')
    advertiser_image = request.files.get('image')

    advertiser_password = data.get('password')
    hashed_password = bcrypt.generate_password_hash(advertiser_password).decode('utf-8')
    # check if the image is provided
    if advertiser_image:
        # check if the image is an image
        if advertiser_image.mimetype not in ['image/jpeg', 'image/png', 'image/jpg']:
            return jsonify({"error": "Please provide an image"}), 400
        # check if the image is less than 10MB
        if advertiser_image.content_length > 10 * 1024 * 1024:
            return jsonify({"error": "Image size should be less than 10MB"}), 400
        # upload the image to the cloudinary
        resp = vercel_blob.put(advertiser_image.filename, advertiser_image.read())
        # get the image url
        image = resp.get('url')
        # remove previous image from the cloudinary
        if advertiser.advertiser_pic:
            vercel_blob.delete(advertiser.advertiser_pic)
        advertiser.advertiser_pic = image

    #update if the data is provided
    advertiser.company_name = check_data(advertiser.company_name, company_name)
    advertiser.advertiser_name = check_data(advertiser.advertiser_name, advertiser_name)
    advertiser.contact_email = check_data(advertiser.contact_email, contact_email)
    advertiser.advertiser_type = check_data(advertiser.advertiser_type, advertiser_type)
    advertiser.about = check_data(advertiser.about, about)
    advertiser.visa_number = check_data(advertiser.visa_number, visa_number)
    advertiser.password = check_data(advertiser.password, hashed_password)

    # add the advertiser phones to the database
    if advertiser_phones:
        phones = Advertiser_Phones.get_phones(advertiser_id)
        for phone in advertiser_phones:
            #update the phone .. if it exists in the database continue to the next phone
            #but if it does not exist add it to the database
            if phone in phones:
                continue
            else:
                new_phone = Advertiser_Phones(advertiser_id=advertiser_id, phone=phone)
                db.session.add(new_phone)
        #delete the old phones that are not in the new list
        for phone in phones:
            if phone not in advertiser_phones:
                deleted_phone = Advertiser_Phones.query.filter_by(advertiser_id=advertiser_id, phone=phone).first()
                db.session.delete(deleted_phone)

    # add the advertiser location to the database
    if advertiser_locations:
        locations = Advertiser_Locations.get_locations(advertiser_id)
        for location in advertiser_locations:
            #update the location if it exists
            if location in locations:
                continue
            else:
                new_location = Advertiser_Locations(advertiser_id=advertiser_id, location=location)
                db.session.add(new_location)
        #delete the old locations that are not in the new list
        for location in locations:
            if location not in advertiser_locations:
                deleted_location = Advertiser_Locations.query.filter_by(advertiser_id=advertiser_id,
                                                                        location=location).first()
                db.session.delete(deleted_location)
    db.session.commit()

    return jsonify({"message": "Advertiser updated successfully"}), 200
