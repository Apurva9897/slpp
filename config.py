import os

class Config:
    SECRET_KEY = 'MY_SECRET_KEY' 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///slpp.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
