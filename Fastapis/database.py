from utils.log import default_logger
import sqlalchemy
from tenacity import retry, stop_after_attempt, wait_exponential
from config import Config
from utils.log import default_logger

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, multiplier=1.5, max=5))
def create_db_engine():
    try:
        print("creating database engine")
        db_engine = sqlalchemy.create_engine(Config.SQLCONNSTR_DBSTRING)
        return db_engine
    except Exception as e:
        default_logger.exception("Error while creating the database engine")
        raise e

db_engine = create_db_engine()