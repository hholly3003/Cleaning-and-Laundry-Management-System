from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
#Load environment variable
from dotenv import load_dotenv
load_dotenv()


db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    #Flask app creation
    app = Flask(__name__)
    #Load configuration from settings.py
    app.config.from_object("settings.app_config")

    #Register flask extensions to the flask application
    db.init_app(app)
    ma.init_app(app)

    #Register the commands blueprint into flask app
    from commands import db_commands
    app.register_blueprint(db_commands)

    return app