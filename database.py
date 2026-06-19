import pyodbc
import logging
from typing import List, Tuple, Any, Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.server = 'LAPTOP-2SSGG9O3\MSSQLSERVER2025'
        self.database = 'PYTHONFINAL'
        self.driver = '{ODBC Driver 17 for SQL Server}'
        
        self.connection_string = (
            f"DRIVER={self.driver};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"Trusted_Connection=yes;"
        )
        self.connection = None
        self._initialized = True

    def connect(self) -> bool:
        try:
            if self.connection is None or self.connection.closed:
                logging.info("Đang thiết lập kết nối đến SQL Server...")
                self.connection = pyodbc.connect(self.connection_string, timeout=5)
                logging.info("KẾT NỐI CƠ SỞ DỮ LIỆU THÀNH CÔNG!")
            return True
        except pyodbc.Error as e:
            logging.error(f"LỖI KẾT NỐI DATABASE: {e}")
            return False

    def disconnect(self):
        try:
            if self.connection and not self.connection.closed:
                self.connection.close()
                logging.info("Đã ngắt kết nối Cơ sở dữ liệu.")
        except pyodbc.Error as e:
            logging.error(f"LỖI KHI NGẮT KẾT NỐI: {e}")
        finally:
            self.connection = None

    def execute_read(self, query: str, params: tuple = ()) -> Optional[List[Tuple[Any, ...]]]:
        if not self.connect():
            return None
            
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
                return results
        except pyodbc.Error as e:
            logging.error(f"LỖI TRUY VẤN ĐỌC: {e}")
            logging.debug(f"Câu lệnh gây lỗi: {query} | Tham số: {params}")
            return None

    def execute_write(self, query: str, params: tuple = ()) -> bool:
        if not self.connect():
            return False
            
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                logging.info("Thực thi thay đổi dữ liệu thành công.")
                return True
        except pyodbc.IntegrityError as e:
            logging.warning(f"LỖI RÀNG BUỘC DỮ LIỆU (Integrity Error): {e}")
            self.connection.rollback()
            return False
        except pyodbc.Error as e:
            logging.error(f"LỖI TRUY VẤN GHI: {e}")
            logging.debug(f"Câu lệnh gây lỗi: {query} | Tham số: {params}")
            self.connection.rollback()
            return False

if __name__ == "__main__":
    db1 = Database()
    db2 = Database()

    logging.info(f"Kiểm tra Singleton: db1 và db2 là một? -> {db1 is db2}")

    logging.info("--- BẮT ĐẦU TEST TRUY VẤN ---")
    data = db1.execute_read("SELECT TOP 1 * FROM Users")
    if data:
        logging.info(f"Dữ liệu mẫu: {data}")
    db1.disconnect()