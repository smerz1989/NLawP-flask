import os

class Config(object):
    API_KEY = os.environ.get('QUANDLKEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')
