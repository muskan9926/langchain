from fastapi import APIRouter, HTTPException, Depends
from helper import get_pdf_name, run_and_save_to_memory, create_answer_chain, initialize_database_and_memory, parent_document_retriever, api_get_call
from utils.log import default_logger
from langchain_community.vectorstores import Chroma
from schemas import QuestionInput
from typing import Any
from dependencies import Authentication
from dependencies import get_embedding_function, get_chroma_client, initialize_authentication, get_chunk_store, get_llm
from config import Config

router = APIRouter()

def sanitize_pdf_name(pdf_name):
    if pdf_name.endswith('.pdf'):
        return pdf_name[:-4]
    return pdf_name

@router.post("/process_question", response_model=Any)
def process_question(
    question_input: QuestionInput,
    auth: Authentication = Depends(initialize_authentication().authenticate),
    chunk_store=Depends(get_chunk_store),
    embedding_function=Depends(get_embedding_function),
    chroma_client=Depends(get_chroma_client),
    llm=Depends(get_llm)
):
    try:
        default_logger.info("Received the question")
        input_question = question_input.question
        documents_api_url = "http://localhost:8002/documents"
        api_key = "0171353f83a44cbea6b49745b19c69d1"
        request_headers = {'Authorization': api_key, 'Content-Type': "application/json"}
        loan_list = api_get_call(documents_api_url, request_headers)
        default_logger.info(f"Loan list retrieved: {loan_list}")

        pdf_name = get_pdf_name(question=input_question, deal_name_list=loan_list)
        sanitized_pdf_name = sanitize_pdf_name(pdf_name)
        default_logger.info(f"Sanitized PDF name is: {sanitized_pdf_name}")

        vectorstore = Chroma(
            client=chroma_client,
            collection_name=sanitized_pdf_name,
            embedding_function=embedding_function
        )

        retriever = parent_document_retriever(vectorstore, chunk_store)
        session_id = question_input.session_id
        memory = initialize_database_and_memory(session_id=session_id)
        final_chain = create_answer_chain(llm=llm, retriever=retriever, memory=memory)
        response = run_and_save_to_memory(input_question, memory, final_chain)
        return response
    except Exception as e:
        default_logger.exception(f"Error: {str(e)}")
        error_message = f"Error processing message: {e}"
        raise HTTPException(status_code=500, detail=error_message)
