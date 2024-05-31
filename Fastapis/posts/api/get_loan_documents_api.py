from utils.log import default_logger
from posts.api.api_response import APIResponse
from posts.api.db_datahandler import RDBDataHandler
from fastapi import Request

class RequestsGetAllDataAPI(APIResponse):
    """
    Inherits `posts.api.api_response.APIResponse class`

    Class to process and return output for requests post API.
    """
    def __init__(self, request: Request)-> None:
        """
        Parameters
        ----------
        request : `fastapi.Request`

        """
        super().__init__(request)
        self.query = """
                    SELECT document_name FROM loan_documents
                """

    def process(self):
        """
        Process the request to fetch all document names from the database.
  
        Returns:
        -------
        None
         This method updates the output attribute and response status code based on the result of the database query.
         If successful, it returns a list of document names.
        """
        try:
          default_logger.info("Fetching deal names")
          db_data_ob = RDBDataHandler()
          cursor = db_data_ob.fetch_all_documents(self.query)
          # document_names = [row[0] for row in cursor.fetchall()]
          document_names = [] 
          for row in cursor:
                  document_names.append(row[0]) 
          
          if not document_names:
              default_logger.exception("No Documents Found")
              self.output = []
              self.response_status_code = 404
              return
  
          self.output = document_names
          print(self.output)
          self.response_status_code = 200
   
        except:
          default_logger.exception('Error while fetching document names from the database')
          self.output = []
          self.response_status_code = 500
   