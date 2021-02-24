import os

# Getting the environment variables
def get_env(var):
    value = os.environ.get(var)

    if not value:
        raise ValueError(f"{var} is not set!")
    return value

#Defining configuration for different environments
class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return get_env("DB_URI")

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True

environment = os.environ.get("FLASK_ENV")

if environment == "development":
    app_config = DevelopmentConfig()
elif environment == "testing":
    app_config = TestingConfig()
else:
    app_config = ProductionConfig()