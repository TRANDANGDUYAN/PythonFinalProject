import pyodbc
import logging

# Cấu hình logging để dễ theo dõi lỗi
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(name)s | %(message)s')
logger = logging.getLogger("DatabaseManager")

class DatabaseManager:
    def __init__(self):
        # ĐỊA CHỈ SERVER: Đây là nơi bạn cần đổi nếu lỗi 08001 vẫn còn
        # Hãy thử lần lượt: '.' hoặc 'localhost' hoặc 'LAPTOP-2SSGG903' (bỏ phần \MSSQLSERVER2025)
        self.server = r'LAPTOP-2SSGG903\MSSQLSERVER2025' 
        self.database = 'PYTHON'
        self.driver = '{ODBC Driver 17 for SQL Server}'
        self.connection = None

    def connect(self):
        """Thiết lập kết nối với SQL Server"""
        try:
            conn_str = (
                f"DRIVER={self.driver};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"Trusted_Connection=yes;"
            )
            self.connection = pyodbc.connect(conn_str, timeout=5)
            logger.info("Kết nối database thành công.")
            return True
        except pyodbc.Error as e:
            logger.error(f"LỖI KẾT NỐI: {e}")
            logger.info("Gợi ý: Kiểm tra lại tên server trong file database.py hoặc trạng thái SQL Server Service.")
            self.connection = None
            return False

    def execute_query(self, query, params=()):
        """Dùng cho INSERT, UPDATE, DELETE"""
        if not self.connection:
            if not self.connect(): return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return True
        except pyodbc.Error as e:
            logger.error(f"LỖI EXECUTE: {e}")
            return False

    def fetch_query(self, query, params=()):
        """Dùng cho SELECT"""
        if not self.connection:
            if not self.connect(): return None
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except pyodbc.Error as e:
            logger.error(f"LỖI FETCH: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()