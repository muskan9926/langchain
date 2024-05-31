from fastapi.responses import JSONResponse
from fastapi import Request

class APIResponse:
    """
    Base class for processing the API request and returning response

    Attributes
    ----------
    request: `fastapi.Request`

    output: `Union[dict, str]` 
        Output to be sent as part of the response (default is None)
    
    response_status_code: `int`
        HTTP status code of the response (default is 200)
    
    additional_headers: `dict`
        Additional headers to be attached with the response (default is {})
    
    Methods
    -------
    process(**kwargs) -> `None`:
        processes the business logic for the API
    
    return_response() -> `fastapi.Response` :
        returns Response object for the API
    
    
    Example for inheritence:
    ------------------------
    class ExampleAPI(APIResponse):
       
        def __init__(self, request: Request) -> None:
            super().__init__(request)
        
        def process(self):
            self.output = "Response generated"
            self.additional_headers = {}

    """
    
    def __init__(self, request: Request) -> None:
        """
        Initializes attributes with default values.
        """
        self.request = request
        self.output = None
        self.response_status_code = 200
        self.additional_headers = {}
        
    def process(self, **kwargs):
        """
        Updates the self.output, self.response_status_code and self.additional_headers attributes

        Returns
        -------
        `None`
        """
        raise NotImplementedError

    def return_response(self, **kwargs):
        """
        Executes the process method to handle the request and generates an appropriate response.
    
        Parameters:
        ----------
        **kwargs: dict
            Arbitrary keyword arguments passed to the process method.
    
        Returns:
        -------
        JSONResponse
            A response object containing the output data, status code, and additional headers.
        """
        self.process(**kwargs)
        return JSONResponse(content=self.output, status_code=self.response_status_code, headers=self.additional_headers)
