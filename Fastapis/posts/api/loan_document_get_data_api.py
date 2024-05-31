from utils.log import default_logger
from posts.api.api_response import APIResponse
from posts.api.db_datahandler import RDBDataHandler
from fastapi import Request

class RequestsGetDataAPI(APIResponse):
    """
    Inherits `posts.api.api_response.APIResponse class`

    Class to process and return output for requests post API.
    """
    def __init__(self,  request: Request)-> None:
        """
        Parameters
        ----------
        request : `fastapi.Request`

        """
        super().__init__(request)
        self.query = """
                    SELECT document_name, collection_name
                    FROM loan_documents
                    WHERE document_name = %s
                """

    def process(self, **kwargs):
        """
        Process the request to fetch information related to a document from the database.

        Parameters:
        ----------
        **kwargs: dict
            Arbitrary keyword arguments. Expects 'document_name' as a key to identify the document.
    
        Returns:
        -------
        None
            This method updates the output attribute and response status code based on the result of the database query.
            If successful, it returns information related to the document in the form of JSON.
        """
        try:
            document_name = kwargs.get('document_name')
            default_logger.info("Fetching information for deal: {}".format(document_name))
            db_data_ob = RDBDataHandler()
            cursor = db_data_ob.fetch(self.query, document_name)

            document_data = cursor.fetchall()
            if len(document_data) == 0:
                default_logger.exception("Deal not found: " + document_name)
                self.output = "Deal not found"
                self.response_status_code = 404
                return

            document_info = document_data[0]
            default_logger.info("Deal info tuple: {}".format(document_info))  

            response_data = {
            "document_name": document_info[0],
            "collection_name": document_info[1],
            }


            cursor.close()
            db_data_ob.connection.close()

            self.output = response_data
            self.response_status_code = 200

            return
        except:
            default_logger.exception('Error while fetching app information from the database')
            self.output = ""
            self.response_status_code = 500
            return