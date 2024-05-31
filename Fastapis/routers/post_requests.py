from posts.api.loan_document_post_api import RequestsPostAPI
from posts.api.user_post_api import UserRequestsPostAPI
from fastapi import APIRouter, Request,Depends
from utils.log import default_logger
from dependencies import Authentication,initialize_authentication
router = APIRouter()

@router.post("/requests/documents")
async def post_loan_documents(request: Request, auth: Authentication = Depends(initialize_authentication().authenticate)):
    """
    Endpoint to handle POST requests for loan documnets using RequestsPostAPI.
    """
    try:
        request_body = await request.json()  
        response = RequestsPostAPI(request_body).return_response()  
        return response
    except:
        default_logger.exception("An error occurred while inserting deal document data")
        return {"error": "Internal Server Error"}, 500
    

@router.post("/requests/user")
async def post_user_data(request: Request, auth: Authentication = Depends(initialize_authentication().authenticate)):
    """
    Endpoint to handle POST requests for user data using UserRequestsPostAPI.
    """
    try:
        request_body = await request.json()  
        response = UserRequestsPostAPI(request_body).return_response()  
        return response
    except:
        default_logger.exception("An error occurred while inserting user data")
        return {"error": "Internal Server Error"}, 500

