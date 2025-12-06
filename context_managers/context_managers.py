import sqlite3
import logging
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SQLite:
    def __init__(self, file_name: str):
        self.file_name = file_name
        logger.info(f"Creating connection on {self.file_name}...")
        self.connection = sqlite3.connect(self.file_name)
    
    # __enter__ method to start scope of context_manager
    def __enter__(self):
        logger.info("Returning cursor connection...")
        return self.connection.cursor()

   # When out of context scope the __exit__ is triggered  
    def __exit__(self, exc_type, exc_value, traceback):
        logger.info("Finishing connection!")
        self.connection.commit()
        self.connection.close()
        return True # returning True on __exit__ method say to python that we don't care about the error, then supress the error.

@contextmanager
def open_db(file_name: str):
    connection = sqlite3.connect(file_name)
    try:
        cursor = connection.cursor()
        yield cursor
    except sqlite3.DatabaseError as error:
        logger.error(error)
    finally:
        connection.commit()
        logger.info("Closing connection...")
        connection.close()
    

def main():
    with open_db(file_name="/home/lukas/Documents/estudo/python_decorators/my_test_database.db") as cursor:
        cursor.execute("SELECT * FROM person;")
        logger.info(cursor.fetchall())


if __name__ == "__main__":
    main()