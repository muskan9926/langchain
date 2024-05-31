import os
import json
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    API_AUTH_KEY = os.environ['API_AUTH_KEY']
    
    SQLCONNSTR_DBSTRING = os.environ['SQLCONNSTR_DBSTRING']
