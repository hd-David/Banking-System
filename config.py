import os

class Config:
    SECRET_KEY = os.urandom(64)
    SQLALCHEMY_DATABASE_URI = 'your-database-uri'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
