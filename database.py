# blueprints/models.py
import enum

from flask import send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, ForeignKey, Enum
from flask_login import UserMixin
from sqlalchemy.orm import Mapped

db = SQLAlchemy()


# create a function to get the image of the advertiser
def get_advertiser_image(advertiser_id):
    advertiser = Advertisers.query.filter_by(id=advertiser_id).first()
    #convert the image from binary to image
    with open('image.jpg', 'wb') as file:
        file.write(advertiser.advertiser_pic)
    #return the image to display in the frontend
    return send_file('image.jpg', mimetype='image/jpg')


# create a function to get the image of the user
def get_user_image(user_id):
    user = Users.query.filter_by(id=user_id).first()
    #convert the image from binary to image
    with open('image.jpg', 'wb') as file:
        file.write(user.profile_pic)
    #return the image to display in the frontend
    return send_file('image.jpg', mimetype='image/jpg')


def dict_factory2(obj):
    if isinstance(obj, list):
        for user in obj:
            if isinstance(user, Users):
                print(user.__dict__)
    elif isinstance(obj, Users):
        print(obj.__dict__)
    else:
        return None


def dict_factory(obj):
    if isinstance(obj, list):
        return [item.to_dict() for item in obj if isinstance(item, db.Model)]
    elif isinstance(obj, db.Model):
        return obj.to_dict()
    # else:
    #     return None


class CriteriaEnum(enum.Enum):
    Babies = 'Babies'
    Kids = 'Kids'
    Teenagers = 'Teenagers'
    Adults = 'Adults'
    Elders = 'Elders'


class AdvertiserTypeEnum(enum.Enum):
    Factory = "Factory"
    Shop = "Shop"


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    age = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    profile_pic = db.Column(db.String(200))

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'age': self.age,
            'name': self.name,
            'profile_pic': self.profile_pic
        }


class Advertisers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)
    advertiser_name = db.Column(db.String(255), nullable=False)
    contact_email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    advertiser_pic = db.Column(db.String(200))
    referral_code = db.Column(db.Integer)
    advertiser_type = db.Column(Enum(AdvertiserTypeEnum),
                                nullable=False)  # another method enum : Mapped[AdvertiserTypeEnum]
    about = db.Column(db.String(500))
    visa_number = db.Column(db.String(50))

    #transform to dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'advertiser_name': self.advertiser_name,
            'contact_email': self.contact_email,
            'password': self.password,
            'advertiser_type': self.advertiser_type.value,  # get the value of the enum
            'about': self.about,
            'visa_number': self.visa_number,
            'referral_code': self.referral_code,
            'advertiser_pic': self.advertiser_pic
        }


class Campaigns(db.Model):
    __tablename__ = 'ad_campaigns'  # Ensure this matches the table name
    id = db.Column(db.Integer, primary_key=True)
    advertiser_id = db.Column(db.Integer, ForeignKey('advertisers.id'))
    campaign_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500))
    target_audience = db.Column(Enum(CriteriaEnum), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    price = db.Column(db.Integer)
    offer = db.Column(db.Integer)
    __table_args__ = (CheckConstraint('end_date >= start_date OR end_date IS NULL', name='check_end_date'),)

    def to_dict(self):
        return {
            'id': self.id,
            'advertiser_id': self.advertiser_id,
            'campaign_name': self.campaign_name,
            'description': self.description,
            'target_audience': self.target_audience.value,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'price': self.price,
            'offer': self.offer
        }


class Ad_Clicks(db.Model):
    ad_campaign_id = db.Column(db.Integer, ForeignKey('ad_campaigns.id'), primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), primary_key=True)
    click_date = db.Column(db.DateTime)
    link_pressed = db.Column(db.String(255))


class Ad_Impressions(db.Model):
    __tablename__ = 'ad_impressions'  # Ensure this matches the table name
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, ForeignKey('ad_campaigns.id'))
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    impression_date = db.Column(db.DateTime)
    took_offer = db.Column(db.Boolean)


class Advertiser_Locations(db.Model):
    __tablename__ = 'advertiser_locations'  # Ensure this matches the table name
    location = db.Column(db.String(255), primary_key=True)
    advertiser_id = db.Column(db.Integer, ForeignKey('advertisers.id'), primary_key=True)

    #create a to_dict function to transform the object to dictionary
    @staticmethod
    def get_locations(advertiser_id):
        # loop on the objects and return one dictionary for all the phones of the same advertiser
        locations = []
        # get the phones of the advertiser
        for location in Advertiser_Locations.query.filter_by(advertiser_id=advertiser_id).all():
            locations.append(location.location)
        return locations


class Campaign_Locations(db.Model):
    __tablename__ = 'campaign_locations'  # Ensure this matches the table name
    location = db.Column(db.String(255), primary_key=True)
    campaign_id = db.Column(db.Integer, ForeignKey('ad_campaigns.id'), primary_key=True)

    @staticmethod
    def get_locations(campaign_id):
        # loop on the objects and return one dictionary for all the phones of the same advertiser
        locations = []
        # get the phones of the advertiser
        for location in Campaign_Locations.query.filter_by(campaign_id=campaign_id).all():
            locations.append(location.location)
        return locations

class Campaign_Videos(db.Model):
    __tablename__ = 'campaign_videos'  # Ensure this matches the table name
    link = db.Column(db.String(255), primary_key=True)
    campaign_id = db.Column(db.Integer, ForeignKey('ad_campaigns.id'), primary_key=True)


class Campaign_Images(db.Model):
    __tablename__ = 'campaign_images'  # Ensure this matches the table name
    image = db.Column(db.String(255), primary_key=True)
    campaign_id = db.Column(db.Integer, ForeignKey('ad_campaigns.id'), primary_key=True)

    @staticmethod
    def get_images(campaign_id):
        # loop on the objects and return one dictionary for all the phones of the same advertiser
        images = []
        # get the phones of the advertiser
        for image in Campaign_Images.query.filter_by(campaign_id=campaign_id).all():
            images.append(image.image)
        return images


class Wishlist(db.Model):
    campaign_id = db.Column(db.Integer, ForeignKey('ad_campaigns.id'), primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), primary_key=True)


class Advertiser_Images(db.Model):
    image = db.Column(db.String(255), primary_key=True)
    advertiser_id = db.Column(db.Integer, ForeignKey('advertisers.id'), primary_key=True)


class Advertiser_Phones(db.Model):
    __tablename__ = 'advertiser_phones'  # Ensure this matches the table name
    phone = db.Column(db.String(20), primary_key=True)
    advertiser_id = db.Column(db.Integer, ForeignKey('advertisers.id'), primary_key=True)

    #create a to_dict function to transform the object to dictionary
    @staticmethod
    def get_phones(advertiser_id):
        #loop on the objects and return one dictionary for all the phones of the same advertiser
        phones = []
        #get the phones of the advertiser
        for phone in Advertiser_Phones.query.filter_by(advertiser_id=advertiser_id).all():
            phones.append(phone.phone)
        return phones
        # return {
        # 'phones': phones
        # 'advertiser_id': self.advertiser_id
        # }

        # return {
        #     'phone': self.phone
        #     # 'advertiser_id': self.advertiser_id
        # }

    def __repr__(self):
        return '<User %r>' % self.username

# Now you can use the session to execute queries
# with app.app_context():
#     userss = Users.query.all()
#     for user in userss:
#         print(user.__dict__)
