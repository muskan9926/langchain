from tenacity import retry, stop_after_attempt, wait_exponential
from fastapi import  Request
from posts.api.api_response import APIResponse
from database import db_engine
from utils.log import default_logger

class RequestsPostAPI(APIResponse):
    """
    Inherits `posts.api.api_response.APIResponse class`

    Class to process and return output for requests post API.
    """

    def __init__(self, request: Request) -> None:
        """
        Parameters
        ----------
        request : `fastapi.Request`

        """
        super().__init__(request)

        self.__query = """
                    INSERT INTO langchaindbo.loan_documents (document_name, collection_name ) 
                    VALUES(%s,%s)
                    """
        self.__message_options = {
            0: "Request received successfully!",
            1: "Request validation error",
            2: "Incorrect request format!",
            3: "Unable to process request. Please try again later!"
        }

    def __validate_request(self) -> bool:
        """
        Validates the request.
        Sets the response_status_code and output in case of error conditions.

        Returns
        -------
        `bool`
            returns True if the request is valid.

        """
        try:
            # self.request_json = self.request.json()
            self.document_name = self.request.get("document_name")
            self.collection_name = self.request.get("collection_name")
        except Exception as e:
            default_logger.exception("Request validation error")
            self.output = ''
            self.response_status_code = 400
            return False
        
        return True

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, multiplier=1.5, max=5))
    def db_insert(self):
        try:
            conn = db_engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute(
                            self.__query, 
                            (self.document_name, self.collection_name)
                        )
            conn.commit()
            cursor.close()
            conn.close()
        except:
            default_logger.exception("Error during DB insertion: "+ self.document_name + " | " + str(self.db_insert.retry.statistics))
            raise Exception("Error during DB insertion: "+ self.collection_name + " | " + str(self.db_insert))
        

    def process(self) -> None:
        """
        Validates the request, processes it and sets self.output & self.response_status_code attributes
        
        Returns
        -------
        `None`
        """
        if self.__validate_request():
           self.output = ''
           try:
               self.db_insert()
               self.response_status_code = 202
           except: 
               default_logger.exception("Error while updating")
               self.response_status_code = 500
            
