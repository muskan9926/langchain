from fastapi import FastAPI , Depends
from fastapi.middleware.cors import CORSMiddleware 
from config import Config
from dependencies import initialize_authentication
from database import db_engine
from routers import post_requests, get_requests


def create_app():
    app = FastAPI()
    db = db_engine

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers and assign tags
    app.include_router(post_requests.router, tags=["post_loan_documents", "post_user_data"],dependencies=[
        Depends(initialize_authentication().authenticate)
        ])
    app.include_router(get_requests.router, tags=["fetch_all_documents", "fetch_document_by_name"],dependencies=[
        Depends(initialize_authentication().authenticate)
        ])

    return app,db

