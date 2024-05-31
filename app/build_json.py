import os
from datetime import datetime
import uuid
import requests

docs_folder = "/Users/muskanchoudhary/Desktop/work/final_langchain_project_chroma_memory /Data"



def process_folder(docs_folder):
    pdf_files = [f for f in os.listdir(docs_folder) if f.endswith(".pdf")]
    messages = []

    for pdf_file in pdf_files:
        file_name = os.path.basename(pdf_file)
        message_json = create_message_json(file_name)
        messages.append(message_json)

    return messages

def create_message_json(file_name):
    message_id = str(uuid.uuid4())  
    common_message_json = {
        "file_name": file_name,
        "time": str(datetime.now()),  
        "id": message_id
    }
    return common_message_json

def send_messages(messages):
    for message in messages:
        print("Sending message:", message)
        try:
            headers = {
                "Authorization":  "0171353f83a44cbea6b49745b19c69d1",
                "Content-Type": "application/json"
            }
            response = requests.post("http://127.0.0.1:8001/process_message", json=message, headers=headers)
            response.raise_for_status()  
            print("Response:", response.text)
        except Exception as e:
            print("Error:", e)

result_messages = process_folder(docs_folder)
send_messages(result_messages)
