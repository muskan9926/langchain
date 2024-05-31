from fastapi import Header, HTTPException
from utils.log import default_logger
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
        

authentication_instance = Authentication(api_auth_key=Config.API_AUTH_KEY)

def initialize_authentication():
    return authentication_instance
        
        