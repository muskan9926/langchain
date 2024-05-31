from fastapi import Header, HTTPException
from utils.log import default_logger
from helper import initialize_model
from config import Config

class Authentication:
    def __init__(self, api_auth_key):
        self.api_auth_key = api_auth_key

    def authenticate(self, authorization: str = Header(...)):
        if authorization == self.api_auth_key:
            return
        else:
            default_logger.exception("Authentication failed: " + str(authorization))
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        

class Initialization:
    def __init__(self):
        print("Initializing Initialization instance...")
        self._initialize_app()
        print("Initialization complete.")

    def _initialize_app(self):
        print("Initializing app attributes...")
        self.embedding_function, self.llm, self.chroma_client, self.chunk_store = initialize_model()
        print("Attributes initialized successfully.")



initialization_instance = Initialization()
authentication_instance = Authentication(api_auth_key=Config.API_AUTH_KEY)

def get_embedding_function():
    return initialization_instance.embedding_function

def get_llm():
    return initialization_instance.llm

def get_chroma_client():
    return initialization_instance.chroma_client

def get_chunk_store():
    return initialization_instance.chunk_store

def initialize_authentication():
    return authentication_instance



