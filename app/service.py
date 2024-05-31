from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
from helper import process_pdf_folder,initialize_model,get_pdf_name,initialize_database_and_memory,create_answer_chain, run_and_save_to_memory,parent_document_retriever
from utils.log import default_logger
from config import Config
from langchain_community.vectorstores import Chroma

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

class Message(BaseModel):
    file_name: str
    time: str
    id: str

class QuestionInput(BaseModel):
    question: str

embedding_function,llm,chroma_client = initialize_model()
message_history, memory, chunk_store= initialize_database_and_memory()


@app.post("/process_message")
def process_message(message: Message):
    try:
        default_logger.info(f"Received message: {message}")
        pages = process_pdf_folder(Config.DATA_FOLDER, message.file_name)
        print(message.file_name)
        document_collection =chroma_client.create_collection(message.file_name)
        print(document_collection)
        vectorstore= Chroma(
        client=chroma_client,
        collection_name=message.file_name,
        embedding_function=embedding_function)
        print("got vector store")
        retreiver=parent_document_retriever(vectorstore,chunk_store)
        retreiver.add_documents(pages, ids=None)        
        print(message.file_name)
    except Exception as e:
        error_message = f"Error processing message: {e}"
        raise HTTPException(status_code=500, detail=error_message)


    
@app.post("/process_question", response_model=Any)
def process_question(question_input: QuestionInput):
    try:
        default_logger.info("Recieved the question")
        input_question = question_input.question
        pdf_name= get_pdf_name(question=input_question)
        print(pdf_name)
        vectorstore= Chroma(
        client=chroma_client,
        collection_name=pdf_name,
        embedding_function=embedding_function)
        retreiver=parent_document_retriever(vectorstore,chunk_store)
        final_chain=create_answer_chain(llm=llm,retriever=retreiver,memory=memory)
        response=run_and_save_to_memory(input_question, memory, final_chain)
        print(response)
        return response
    except Exception as e:
        error_message = f"Error processing message: {e}"
        raise HTTPException(status_code=500, detail=error_message)



