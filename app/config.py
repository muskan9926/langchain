import os
import json
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
    DATA_FOLDER=os.environ["DATA_FOLDER"]
    LANGCHAIN_MODEL_NAME=os.environ["LANGCHAIN_MODEL_NAME"]
    EMBEDDING_MODEL_NAME=os.environ["EMBEDDING_MODEL_NAME"]
    EXTRACTION_MODEL_NAME=os.environ["EXTRACTION_MODEL_NAME"]
    REDIS_URL=os.environ["REDIS_URL"]
    LOCAL_STORE=os.environ["LOCAL_STORE"]
    API_AUTH_KEY = os.environ['API_AUTH_KEY']
    CONTAINER_NAME=os.environ['CONTAINER_NAME']
    



