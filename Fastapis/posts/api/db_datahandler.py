from utils.log import default_logger
from abc import ABC, abstractmethod
from tenacity import retry, stop_after_attempt, wait_exponential
from database import db_engine

class DBDataHandler(ABC):
    """
    Base class (abstract) for handling data from database
    Abstract methods:
        1. fetch()
    """
    def __init__(self):
        pass
    
    @abstractmethod
    def fetch(self):
        pass


class RDBDataHandler(DBDataHandler):
    """
    Class for handling data from Relational data base

    Attributes:
    ----------
    connection : sqlalchemy.raw_connection
        sqlalchemy raw_connection object from db_engine
        
    Methods:
    -------
    fetch(parameterized_query, *args)
        fetches data from RDBMS

    fetch_all_documents(parameterized_query)
        fetches data from RDBMS

    """
    def __init__(self):
        """
        """
        pass
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, multiplier=1.5, max=5))
    def fetch(self, parameterized_query, *args):
        """
        Executes a parameterized query passed in method parameter with
        arguments passed in method arguments and returns database connection
        cursor.

        Parameters:
        ----------
        parameterized_query: str
            string query to be executed in database

        max_retry_count: int
            default value is 2

        Args
            all values for placeholders in parameterized query

        Returns:
        -------
        cursor object
        """
        try:
            self.connection = db_engine.raw_connection()
            cursor = self.connection.cursor()
            cursor.execute(parameterized_query, args)
            return cursor
        except:
            default_logger.exception("Error while fetching from database")
            raise Exception("Error occured while fetch data from database")
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, multiplier=1.5, max=5))
    def fetch_all_documents(self, parameterized_query):
        """
        Executes a parameterized query to fetch all documents from the database.

        Parameters:
        ----------
        parameterized_query: str
            string query to be executed in the database to fetch all documents.

        Returns:
        -------
        cursor object
            Cursor object containing the result set of the executed query.
        """
        try:
            self.connection = db_engine.raw_connection()
            cursor = self.connection.cursor()
            cursor.execute(parameterized_query)
            return cursor
        except:
            default_logger.exception("Error while fetching from database")
            raise Exception("Error occured while fetch data from database")


# TODO: All DB interactions to be generalized/formalized
# DBHandler