from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from marshmallow.exceptions import ValidationError
#Load environment variable
from dotenv import load_dotenv
load_dotenv()


db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    #Flask app creation
    app = Flask(__name__)
    #Load configuration from settings.py
    app.config.from_object("settings.app_config")

    #Register flask extensions to the flask application
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app,db)

    #Register the commands blueprint into flask app
    from commands import db_commands
    app.register_blueprint(db_commands)

    #Register the controllers into flask app
    from controllers import registerable_controllers
    for controller in registerable_controllers:
        app.register_blueprint(controller)
    
    @app.errorhandler(ValidationError)
    def handle_bad_request(error):
        return (jsonify(error.messages), 400)

    return app