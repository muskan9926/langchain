# main.py
from fastapi import FastAPI , Depends
from fastapi.middleware.cors import CORSMiddleware 
from routers import process_message, process_question
from config import Config
from dependencies import get_chroma_client,get_embedding_function,get_llm,initialize_authentication,get_chunk_store
from fastapi import Depends


def create_app():
    app = FastAPI()
    print("intilizing authentication")
    # auth_instance = initialize_authentication()

    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["POST"],
        allow_headers=["*"],
    )


    print("included router ")
    # By Dependecy example get_embedding_function every time an api hits it will ask get_embedding_function to get embedding_function
    app.include_router(process_message.router, tags=["process_message"], dependencies=[
    Depends(get_embedding_function),
    Depends(get_chroma_client),
    Depends(initialize_authentication().authenticate),
    Depends(get_chunk_store)

])

    app.include_router(process_question.router, tags=["process_question"], dependencies=[
    Depends(get_llm),
    Depends(get_chroma_client),
    Depends(initialize_authentication().authenticate),
    Depends(get_embedding_function),
    Depends(get_chunk_store)

])
   
    return app

