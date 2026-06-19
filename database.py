import pyodbc
import logging
import sys
from typing import List, Tuple, Any, Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("DatabaseManager")

class DatabaseConnectionError(Exception):

    def __init__(self, message="Failed to connect to the SQL Server Database."):
        self.message = message
        super().__init__(self.message)

class Database:

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._is_initialized = False
        return cls._instance

    def __init__(self):

        if self._is_initialized:
            return

        self.server: str = r'LAPTOP-2SSGG903\MSSQLSERVER2025' 
        self.database: str = 'PYTHON'
        self.driver: str = '{ODBC Driver 17 for SQL Server}'

        self.connection_string: str = (
            f"DRIVER={self.driver};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"Trusted_Connection=yes;"
        )
        
        self.connection: Optional[pyodbc.Connection] = None
        self._is_initialized = True
        logger.info("Database component initialized successfully.")

    def connect(self) -> bool:
        try:
            conn_str = f"DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;"
            self.connection = pyodbc.connect(conn_str, timeout=5)
            return True
        except Exception as e:
            print(f"LỖI SQL THỰC SỰ LÀ: {e}") 
            return False

    def disconnect(self) -> None:

        try:
            if self.connection and not self.connection.closed:
                self.connection.close()
                logger.info("Database connection closed safely.")
        except pyodbc.Error as db_error:
            logger.error(f"Error while disconnecting: {db_error}")
        finally:
            self.connection = None

    def execute_read(self, query: str, params: tuple = ()) -> Optional[List[Tuple[Any, ...]]]:

        if not self.connect():
            logger.error("Read operation aborted: No active database connection.")
            return None

        try:

            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
                logger.debug(f"Read query executed successfully. Rows fetched: {len(results)}")
                return results
                
        except pyodbc.Error as query_error:
            logger.error(f"SQL Read Execution Error: {query_error}")
            logger.debug(f"Failed Query: {query} | Parameters: {params}")
            return None

    def execute_write(self, query: str, params: tuple = ()) -> bool:

        if not self.connect():
            logger.error("Write operation aborted: No active database connection.")
            return False

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                logger.info("Write query executed and committed successfully.")
                return True
                
        except pyodbc.IntegrityError as integrity_error:
            logger.warning(f"Data Integrity Violation (e.g., Duplicate Primary Key): {integrity_error}")
            self.connection.rollback()
            return False
            
        except pyodbc.Error as query_error:
            logger.error(f"SQL Write Execution Error: {query_error}")
            logger.debug(f"Failed Query: {query} | Parameters: {params}")
            self.connection.rollback()
            return False

if __name__ == "__main__":
    logger.info("--- DATABASE MODULE TEST INITIATED ---")

    db = Database()
    if db.connect():
        test_results = db.execute_read("SELECT @@VERSION AS 'SQL Server Version'")
        if test_results:
            logger.info(f"Connected to: {test_results[0][0].split('-')[0].strip()}")

        db.disconnect()
    else:
        logger.error("Module Test Failed: Could not establish a connection.")