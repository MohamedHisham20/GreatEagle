# blueprints/models.py
import enum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, ForeignKey, Enum
from flask_login import UserMixin
from sqlalchemy.orm import Mapped

db = SQLAlchemy()


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


class CriteriaEnum(db.Enum):
    Kids = 'Kids'
    BiggerKids = 'BiggerKids'
    Teenagers = 'Teenagers'
    Adults = 'Adults'
    Elders = 'Elders'


class AdvertiserTypeEnum(db.Enum):
    Factory = "Factory"
    Shop = "Shop"


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    age = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    profilepic = db.Column(db.String(200))

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'age': self.age,
            'name': self.name,
            'profilepic': self.profilepic
        }


class Advertisers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)
    advertiser_name = db.Column(db.String(255), nullable=False)
    contact_email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    advertiser_logo = db.Column(db.String(255))
    advertiser_type = db.Column(AdvertiserTypeEnum,
                                nullable=False)  # another method enum : Mapped[AdvertiserTypeEnum]
    about = db.Column(db.String(500))
    visa_number = db.Column(db.Integer)

    #transform to dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'advertiser_name': self.advertiser_name,
            'contact_email': self.contact_email,
            'password': self.password,
            'advertiser_logo': self.advertiser_logo,
            'advertiser_type': self.advertiser_type.value,  # get the value of the enum
            'about': self.about,
            'visa_number': self.visa_number
        }


class AdCampaigns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    advertiser_id = db.Column(db.Integer, ForeignKey('advertisers.id'))
    campaign_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500))
    target_audience = db.Column(CriteriaEnum, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    price = db.Column(db.Integer)
    offer = db.Column(db.Integer)
    __table_args__ = (CheckConstraint('end_date >= start_date OR end_date IS NULL', name='check_end_date'),)


class AdClicks(db.Model):
    ad_campaign_id = db.Column(db.Integer, ForeignKey('ad_campaigns.id'), primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), primary_key=True)
    click_date = db.Column(db.DateTime)
    link_pressed = db.Column(db.String(255))


class AdImpressions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, ForeignKey('ad_campaigns.id'))
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    impression_date = db.Column(db.DateTime)
    took_offer = db.Column(db.Boolean)


class AdvertiserLocations(db.Model):
    location = db.Column(db.String(255), primary_key=True)
    a_id = db.Column(db.Integer, ForeignKey('advertisers.id'), primary_key=True)


class CampaignLocations(db.Model):
    location = db.Column(db.String(255), primary_key=True)
    campaign_id = db.Column(db.Integer, ForeignKey('ad_campaigns.id'), primary_key=True)


class Videos(db.Model):
    link = db.Column(db.String(255), primary_key=True)
    campaign_id = db.Column(db.Integer, ForeignKey('ad_campaigns.id'), primary_key=True)


class Images(db.Model):
    image = db.Column(db.String(255), primary_key=True)
    campaign_id = db.Column(db.Integer, ForeignKey('ad_campaigns.id'), primary_key=True)


class Wishlist(db.Model):
    campaign_id = db.Column(db.Integer, ForeignKey('ad_campaigns.id'), primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), primary_key=True)


class Phones(db.Model):
    phone = db.Column(db.Integer, primary_key=True)
    a_id = db.Column(db.Integer, ForeignKey('advertisers.id'), primary_key=True)

    def __repr__(self):
        return '<User %r>' % self.username

# Now you can use the session to execute queries
# with app.app_context():
#     userss = Users.query.all()
#     for user in userss:
#         print(user.__dict__)
