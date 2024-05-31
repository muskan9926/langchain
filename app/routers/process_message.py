from utils.log import default_logger
from fastapi import APIRouter, HTTPException, Depends
from helper import process_Azure_pdf_folder,parent_document_retriever
from config import Config
from langchain_community.vectorstores import Chroma
from schemas import Message
from dependencies import Authentication
from dependencies import get_embedding_function,get_chroma_client,initialize_authentication,get_chunk_store
import os
router = APIRouter()

# auth_instance = initialize_authentication()

@router.post("/process_message")
def process_message(
    message: Message,
    auth: Authentication = Depends(initialize_authentication().authenticate),
    embedding_function=Depends(get_embedding_function),
    chroma_client=Depends(get_chroma_client),
    chunk_store=Depends(get_chunk_store)
):
    try:
        default_logger.info(f"Received message: {message}")
        # pdf_name=message.document_name.rsplit('.', 1)[0]
        # pdf_name=message.document_name
        # print(pdf_name)
        pdf_name=message.document_name+ ".pdf"
        print("pdf name is :")
        print(pdf_name)
        pages = process_Azure_pdf_folder(pdf_name)
        print("got pages")
        document_collection = chroma_client.create_collection(message.document_name)
        print(document_collection)
        vectorstore = Chroma(
            client=chroma_client,
            collection_name=message.document_name,
            embedding_function=embedding_function
        )
        # vectorstore.add_documents(chunks, embedding=embedding_function)
        retriever = parent_document_retriever(vectorstore, chunk_store)
        print("got retriever now adding documents")
        retriever.add_documents(pages, ids=None)
        print("added documents")
    except Exception as e:
        default_logger.exception("Error: {}".format(str(e)))
        error_message = f"Error processing message: {e}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)
