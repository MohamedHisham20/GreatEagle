import Flask
from flask_cors import CORS
from flask_login import LoginManager

from database import db


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
    app.register_blueprint(login)
    app.register_blueprint(register)

    db.init_app(app)

    return app


app = create_app()

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app.route("/")
def welcome_page():
    return "<h1> Welcome </h1>"


if __name__ == '__main__':
    app.run(debug=True)
