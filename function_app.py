import azure.functions as func
import logging
import azure.functions as func
import logging
import requests
from urllib.parse import urlparse, unquote
from requests.exceptions import ReadTimeout


app = func.FunctionApp()

def parse_blob_url(blob_url):
    parsed_url = urlparse(blob_url)
    encoded_blob_name = parsed_url.path.split('/')[-1]
    blob_name = unquote(encoded_blob_name)
    return blob_name

def api_call(api_url, data, headers, timeout=3700):
    try:
        logging.info("Adding request to database")
        logging.info(api_url)
        r = requests.post(api_url, json=data, headers=headers, timeout=timeout)
        r.raise_for_status()  
    except ReadTimeout as e:
        logging.error(f"API Timeout Error: {e}")
    except Exception as e:
        logging.exception("API Error: {}".format(e))
        raise Exception('API call Error: {}'.format(e))
   
def create_common_message_json(blob_url):
    if not blob_url:
        logging.warning("Blob URL not found in the event data.")
        return None
    blob_name = parse_blob_url(blob_url)
    blob_name=blob_name.rsplit('.', 1)[0]
    common_message_json = {
        "document_name": blob_name,
        "collection_name": blob_name,
    }
    print(common_message_json)
    return common_message_json

@app.blob_trigger(arg_name="myblob", path="langchainfiles",
                               connection="muskanlangchain_STORAGE") 
def blob_trigger(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")
    print("printing blob uri :")
    print(myblob.uri)
    blob_url = myblob.uri
    print("blob url is :")
    print(blob_url)
    message_json = create_common_message_json(blob_url)
    print("message_json is:")
    print(message_json)
    api_url = "http://localhost:8002/requests/documents"
    print("called api")
    api_key =  "0171353f83a44cbea6b49745b19c69d1"
    request_headers = {'Authorization': api_key, 'Content-Type': "application/json"}
    api_call(api_url,message_json,request_headers)
    print("calling process api")
    process_api_url= "http://localhost:8001/process_message"
    api_call(process_api_url,message_json,request_headers)
    print("completed")
    

