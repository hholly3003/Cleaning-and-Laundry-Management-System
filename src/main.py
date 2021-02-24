#Load environment variable
from dotenv import load_dotenv
load_dotenv()

#Flask app creation
from flask import Flask
app = Flask(__name__)

#Load configuration from settings.py
app.config.from_object("settings.app_config")

#Database connection