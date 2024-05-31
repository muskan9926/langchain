from langchain_community.document_loaders import PyPDFLoader
import os 
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_core.runnables import (
    ConfigurableField,
    RunnableBinding,
    RunnableLambda,
    RunnablePassthrough,
)
import json
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_community.document_loaders import AzureBlobStorageFileLoader
from utils.log import default_logger
from langchain.schema import format_document
from langchain.memory import ConversationBufferMemory
from operator import itemgetter
from langchain_core.messages import  get_buffer_string
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import Config
from langchain.prompts.prompt import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import OpenAI
from langchain_community.chat_message_histories import RedisChatMessageHistory
import chromadb
from langchain_community.vectorstores import Chroma
from chromadb.config import Settings
from langchain_community.embeddings import HuggingFaceInstructEmbeddings  
from langchain.storage._lc_store import create_kv_docstore
from langchain.storage import LocalFileStore
from langchain.retrievers import ParentDocumentRetriever
import logging
import requests
from requests.exceptions import ReadTimeout


def initialize_database_and_memory(session_id):
    """
    Initializes and configures the components needed for the message history and conversation memory.

    Returns:
        tuple: A tuple containing an instance of the message history class and an instance of the conversation memory class.
    """
    try:
        # message_history = RedisChatMessageHistory(session_id="models_chroma", url=Config.REDIS_URL)
        message_history = RedisChatMessageHistory(session_id=session_id, url=Config.REDIS_URL)
        memory = ConversationBufferMemory(memory_key="message", chat_memory=message_history, return_messages=True)
        return memory
    except Exception as e:
        default_logger.exception("Error: {}".format(str(e)))
        error_message = f"Error intilializing database and memory: {e}"
        return error_message


def initialize_model():
    """
    Initializes and configures the components needed for the language model and conversation history.

    Returns:
        tuple: A tuple containing the initialized embedding function, language model (LLM),
               Chroma client, and chunk store.
    """
    try:
        print("in initialize model")
        embedding_function = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
        llm = OpenAI(model_name=Config.LANGCHAIN_MODEL_NAME, max_tokens=100)
        chroma_client = chromadb.HttpClient(settings=Settings(allow_reset=True, anonymized_telemetry=False))
        fs = LocalFileStore(Config.LOCAL_STORE)
        chunk_store = create_kv_docstore(fs)
        return embedding_function, llm, chroma_client, chunk_store
    except Exception as e:
        default_logger.exception("Error: {}".format(str(e)))
        error_message = f"Error in intializing models: {e}"
        return error_message


# During retrieval, the Parent Document Retriever first fetches the small chunks based on the query.
# It then looks up the parent IDs associated with those chunks.
# Finally, it returns the larger documents corresponding to those parent IDs.
# Here Doc Store-The storage layer for the parent documents

def parent_document_retriever(vectorstore, docstore):
    """
    Creates a Parent Document Retriever.

    Args:
        vectorstore: The vector store responsible for managing embeddings.
        docstore: The storage layer for the parent documents.

    Returns:
        ParentDocumentRetriever: An instance of the Parent Document Retriever.
    """
    try:
        print("In parent document retriever function")
        child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)
        retriever = ParentDocumentRetriever(
            vectorstore=vectorstore,
            docstore=docstore,
            child_splitter=child_splitter,
        )
        print("Parent document retriever initialization complete")
        return retriever
    except Exception as e:
        default_logger.exception("Error: {}".format(str(e)))
        error_message = f"Error in parent documnet retriever: {e}"
        return error_message


def process_Azure_pdf_folder(blob_name):
    """
    Processes a folder containing PDF documents.

    Args:
        docs_folder: Path to the folder containing PDFs.
        file_name: Name of the PDF file.

    Returns:
        loaded page.
    """
    try:
        loader = AzureBlobStorageFileLoader(conn_str="DefaultEndpointsProtocol=https;AccountName=muskanlangchain;AccountKey=0JlEoyXx1zOVrLMDeebvZaKqFucQ8A5y30x9hWM7wY/DniotAQ/Or1Yt9b4T2TxyeZJkY/unPrPQ+AStB+S9Zg==;EndpointSuffix=core.windows.net",
                                            container=Config.CONTAINER_NAME,
                                            blob_name=blob_name,
                                            )
        pages = loader.load_and_split()
        print(pages)
        # text_splitter = RecursiveCharacterTextSplitter(
        # chunk_size=2000,
        # chunk_overlap=200,
        #    )
        # chunks = text_splitter.split_documents(pages)
        return pages
    except Exception as e:
        default_logger.exception("Error: {}".format(str(e)))
        error_message = f"Error processing PDF folder: {e}"
        return error_message

# def process_pdf_folder(docs_folder, file_name):
#     """
#     Processes a folder containing PDF documents.

#     Args:
#         docs_folder: Path to the folder containing PDFs.
#         file_name: Name of the PDF file.

#     Returns:
#         loaded page.
#     """
#     try:
#         print(docs_folder)
#         print(file_name)
#         pdf_path = os.path.join(docs_folder, file_name)
#         print(pdf_path)
#         loader = PyPDFLoader(pdf_path)
#         pages = loader.load_and_split()
#         return pages
#     except Exception as e:
#         default_logger.exception("Error: {}".format(str(e)))
#         error_message = f"Error processing PDF folder: {e}"
#         return error_message

# def get_pdf_name(question: str) -> str:
#     try:
#         chat = ChatOpenAI(temperature=0, model=Config.EXTRACTION_MODEL_NAME)
#         template = (
#             "Entity Definition:\n"
#             "1. PDF: Name of the PDF file present in the text.\n"
#             "\n"
#             "Output Format:\n"
#             "{{PDF}}\n"
#             "If no entities are presented in any categories, keep it None.\n"
#             "\n"
#             "available_pdf_names = ['Financial Report 2023', 'Annual Report 2023', 'jaya 2023', 'bank.pdf','Mary_St_Fixed_Rate_Loan_Agreement']\n"
#             "\n"
#             "Use the list available_pdf_names and find the similarity between the name of the PDF present in the list and the text given. "
#             "If found similar and if there are spelling mistakes in the user's text, correct them by referring to the list of PDFs.\n"
#             "\n"
#             "Examples:\n"
#             "\n"
#             "1. Sentence: Please extract and list the values of building loan promissory notes mentioned in the note section present in PDF Financial Report 2023?\n"
#             "   Output: {{\"PDF\": \"Financial Report 2023\"}}\n"
#             "\n"
#             "2. Sentence: What are the specified Deal Rate Rounding Denominator value for 'LIBOR' PRESENT IN 'Annual Report 2023'?\n"
#             "   Output: {{\"PDF\": \"Annual Report 2023\"}}\n"
#             "\n"
#             "3. Sentence: What are the specified Deal Rate Rounding Denominator value for 'LIBOR' PRESENT IN 'cocoloco'?\n"
#             "   Output: {{\"PDF\": \"\"}}\n"
#             "\n"
#             "4. Sentence: {text}\n"
#             "   Output: "
#         )

#         system_message_prompt = SystemMessagePromptTemplate.from_template(template)
#         human_template = "{text}"
#         human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
#         chat_prompt = ChatPromptTemplate.from_messages(
#             [system_message_prompt, human_message_prompt]
#         )
#         formatted_messages = chat_prompt.format_prompt(
#             text=question
#         ).to_messages()

#         response = chat.invoke(formatted_messages)
#         response_content = response.content
#         data = json.loads(response_content)
#         pdf_name = data.get('PDF', "")

#         print("PDF name retrieved:", pdf_name)  

#         if not pdf_name:
#             raise ValueError("The specified deal does not exist.")

#         return pdf_name
    
#     except Exception as e:
#         default_logger.exception("Error: {}".format(str(e)))
#         error_message = f"Error in getting pdf name: {e}"
#         return error_message
    
def api_get_call(api_url, headers=None, timeout=120):
    try:
        logging.info("Adding request to database")
        logging.info(api_url)
        r = requests.get(api_url, headers=headers, timeout=timeout)
        print(r)
        r.raise_for_status() 
        return r.content.decode().splitlines() 
    except ReadTimeout as e:
        logging.error(f"API Timeout Error: {e}")
    except Exception as e:
        logging.exception("API Error: {}".format(e))
        raise Exception('API call Error: {}'.format(e))
   


#  get pdf name when we will send our custom list of deal names 
def get_pdf_name(question: str, deal_name_list: list) -> str:
    try:
        chat = ChatOpenAI(temperature=0, model=Config.EXTRACTION_MODEL_NAME)
        template = (
            "Entity Definition:\n"
            "1. PDF: Name of the PDF file present in the text.\n"
            "\n"
            "Output Format:\n"
            "{{PDF}}\n"
            "I am providing you a list named available_pdf_names you have to fetch the pdf name which is present on text provided"
            "If no entities are presented in any categories, keep it None.\n"
            "\n"
            "available_pdf_names= {PDF_list}\n"
            "\n"
            "Use the list available_pdf_names and find the similarity between the name of the PDF present in the list and the text given. "
            "If found similar and if there are spelling mistakes in the user's text, correct them by referring to the list of PDFs.\n"
            "\n"
            "Examples:\n"
            "\n"
            "1. Sentence: Please extract and list the values of building loan promissory notes mentioned in the note section present in PDF Financial Report 2023?\n"
            "   Output: {{\"PDF\": \"Financial Report 2023\"}}\n"
            "\n"
            "2. Sentence: What are the specified Deal Rate Rounding Denominator value for 'LIBOR' PRESENT IN 'Annual Report 2023'?\n"
            "   Output: {{\"PDF\": \"Annual Report 2023\"}}\n"
            "\n"
            "3. Sentence: What are the specified Deal Rate Rounding Denominator value for 'LIBOR' PRESENT IN 'cocoloco'?\n"
            "   Output: {{\"PDF\": \"None\"}}\n"
            "\n"
            "4. Sentence: {text}\n"
            "   Output: "
        )

        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )
        print(deal_name_list)
        formatted_messages = chat_prompt.format_prompt(
            PDF_list=(deal_name_list),
            text=question
        ).to_messages()

        response = chat.invoke(formatted_messages)
        response_content = response.content
        data = json.loads(response_content)
        pdf_name = data.get('PDF', "")

        print("PDF name retrieved:", pdf_name)  # Debug print

        if not pdf_name:
            raise ValueError("The specified deal does not exist.")

        return pdf_name
    
    except Exception as e:
        error_message = f"Error processing PDF folder: {e}"
        print(error_message)
        return error_message






def create_condense_question_chain(retriever, memory):
    try:
        print("get condense question chain")
        """
        Create a language chain to condense a conversation and generate a standalone question.

        Args:
            retriever: Retrieval component providing relevant information.
            memory: Memory object for context storage.

        Returns:
            langchain.Chain: Language chain for condensing questions.
        """
        _template = """Given the following conversation and a follow-up question, rephrase the follow-up question to be a standalone question, in its original language.

        Chat History:
        {chat_history}
        Follow Up Input: {question}
        Standalone question:"""
        
        CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)
        
        standalone_question = {
            "standalone_question": {
                "question": lambda x: x["question"],
                "chat_history": lambda x: get_buffer_string(x["chat_history"]),
            }
            | CONDENSE_QUESTION_PROMPT
            | OpenAI(temperature=0)
            | StrOutputParser(),
        }

        retrieved_documents = {
            "docs": itemgetter("standalone_question") | retriever,
            "question": lambda x: x["standalone_question"],
        }
        print("got condense chain")
        return RunnablePassthrough.assign(
            chat_history=RunnableLambda(memory.load_memory_variables) | itemgetter("message"),
        ) | standalone_question | retrieved_documents

    except Exception as e:
        default_logger.exception("Error: {}".format(str(e)))
        error_message = f"Error in creating condense question chain: {e}"
        return error_message


def create_answer_chain(llm, retriever, memory):
    try:
        print("in create answer chain")
        """
        Create a language chain for generating an answer based on a context.

        Args:
            llm: Language model for generating responses.
            retriever: Parent Document Retriever for context retrieval.
            memory: Redis Memory for efficient storage of Conversation.

        Returns:
            langchain.Chain: Language chain for generating answers.
        """
        DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")

        def _combine_documents(docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"):
            doc_strings = [format_document(doc, document_prompt) for doc in docs]
            return document_separator.join(doc_strings)

        final_inputs = {
            "context": lambda x: _combine_documents(x["docs"]),
            "question": itemgetter("question"),
        }

        template = """Answer the question based only on the following context:
        {context}

        Question: {question}
        """
        ANSWER_PROMPT = ChatPromptTemplate.from_template(template)

        answer = {
            "answer": final_inputs | ANSWER_PROMPT | llm,
            "docs": itemgetter("docs"),
        }
        print("finished creating answer chain")
        return create_condense_question_chain(retriever=retriever, memory=memory) | answer

    except Exception as e:
        default_logger.exception("Error: {}".format(str(e)))
        error_message = f"Error in create answer chain: {e}"
        return error_message


def run_and_save_to_memory(question, memory, final_chain):
    try:
        print("in run and save memory function")
        """
        Run the language chain to generate an answer, display it, and save the context to memory.

        Args:
            question (str): User's input question.
            memory: Memory object for context storage.
            final_chain: Language chain for question-answering.

        Returns:
            str: The generated answer.
        """
        result = final_chain.invoke({"question": question})
        print("got result")
        answer = result["answer"]
        memory.save_context({"question": question}, {"answer": answer})
        print("done")
        # memory.load_memory_variables({})
        return answer
    
    except Exception as e:
        default_logger.exception("Error: {}".format(str(e)))
        error_message = f"Error in run and save memory function: {e}"
        return error_message


# def get_answer(llm, memory, retriever, question):
#     bot = ConversationalRetrievalChain.from_llm(llm, retriever, memory=memory, verbose=False, chain_type="stuff")
#     result = bot({"question": question})
    # answer=result['answer']
#     return answer
