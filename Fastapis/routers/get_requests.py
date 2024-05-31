from fastapi import APIRouter, Request
from utils.log import default_logger
from fastapi import Depends
from posts.api.loan_document_get_data_api import RequestsGetDataAPI
from posts.api.get_loan_documents_api import RequestsGetAllDataAPI
from dependencies import initialize_authentication, Authentication

router = APIRouter()


@router.get("/documents")
async def fetch_all_documents(request: Request,auth: Authentication = Depends(initialize_authentication().authenticate)):
    """
    Endpoint to fetch document data by document name using the RequestsGetAllDataAPI.
    """
    try:
        return RequestsGetAllDataAPI(request).return_response()
    except:
        default_logger.exception("An error occurred while fetching document data")
        return {"error": "Internal Server Error"}, 500
    

@router.get("/documents/")
    # "/get_document_data/<string:documentname>"

async def fetch_document_by_name(document_name: str, request: Request,auth: Authentication = Depends(initialize_authentication().authenticate)):
    """
    Endpoint to fetch document data by document name using the RequestsGetDataAPI.
    """
    try:
        return RequestsGetDataAPI(request).return_response(document_name=document_name)
    except:
        default_logger.exception("An error occurred while fetching document data")
        return {"error": "Internal Server Error"}, 500
