from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from sqlalchemy.orm import Session
from database import db, Users


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
    app.config["SECRET_KEY"] = "SECRET_KEY"
    app.config['SQLALCHEMY_DATABASE_URI'] = ('postgresql://neondb_owner:nafA0yCgl2jH@ep-bitter-surf-a2u091xk.eu'
                                             '-central-1.aws'
                                             '.neon.tech/neondb?sslmode=require')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app, support_credentials=True)

    from Login import login
    from Register import register
    from advertiserProfile import advertiser
    from home import home
    from CampaignPage import campaign_page
    from searchPage import search_page
    from user import user
    app.register_blueprint(login)
    app.register_blueprint(register)
    app.register_blueprint(advertiser)
    app.register_blueprint(home)
    app.register_blueprint(campaign_page)
    app.register_blueprint(search_page)
    app.register_blueprint(user)

    db.init_app(app)

    return app


app = create_app()

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define the user loader function
@login_manager.user_loader
def load_user(user_id):
    with Session(db.engine) as session:
        return session.get(Users, int(user_id))

@app.route("/")
def welcome_page():
    return "<h1> Welcome </h1>"


if __name__ == '__main__':
    app.run(debug=True)
