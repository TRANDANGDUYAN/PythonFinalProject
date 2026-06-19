import logging
from typing import List, Tuple, Optional, Any
from database import Database

class StudentController:
    def __init__(self):
        self.db = Database()
        logging.info("Khởi tạo StudentController thành công.")
    def _clean_data(self, text: Any) -> str:
        if isinstance(text, str):
            return text.strip()
        return str(text) if text is not None else ""

    def _format_name(self, name: str) -> str:
        clean_name = self._clean_data(name)
        return clean_name.title()

    def get_all_students(self) -> Optional[List[Tuple[Any, ...]]]:
        logging.info("Đang truy xuất danh sách toàn bộ sinh viên...")
        query = """
            SELECT StudentID, FullName, DateOfBirth, Gender, ClassID, Contact 
            FROM Students
            ORDER BY ClassID ASC, FullName ASC
        """
        return self.db.execute_read(query)

    def check_student_exists(self, student_id: str) -> bool:
        clean_id = self._clean_data(student_id)
        query = "SELECT 1 FROM Students WHERE StudentID = ?"
        result = self.db.execute_read(query, (clean_id,))
        return bool(result)

    def add_student(self, student_id: str, fullname: str, dob: str, gender: str, class_id: str, contact: str) -> bool:
        clean_id = self._clean_data(student_id)

        if self.check_student_exists(clean_id):
            logging.warning(f"Từ chối thêm mới: Mã sinh viên {clean_id} đã tồn tại.")
            return False

        formatted_name = self._format_name(fullname)
        clean_class = self._clean_data(class_id).upper()
        
        logging.info(f"Đang thực hiện thêm mới sinh viên: {clean_id} - {formatted_name}")
        query = """
            INSERT INTO Students (StudentID, FullName, DateOfBirth, Gender, ClassID, Contact)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (clean_id, formatted_name, self._clean_data(dob), 
                  self._clean_data(gender), clean_class, self._clean_data(contact))
        
        return self.db.execute_write(query, params)

    def update_student(self, student_id: str, fullname: str, dob: str, gender: str, class_id: str, contact: str) -> bool:
        clean_id = self._clean_data(student_id)
        formatted_name = self._format_name(fullname)
        clean_class = self._clean_data(class_id).upper()

        logging.info(f"Đang cập nhật dữ liệu cho sinh viên mã: {clean_id}")
        query = """
            UPDATE Students 
            SET FullName = ?, DateOfBirth = ?, Gender = ?, ClassID = ?, Contact = ?
            WHERE StudentID = ?
        """
        params = (formatted_name, self._clean_data(dob), self._clean_data(gender), 
                  clean_class, self._clean_data(contact), clean_id)
                  
        return self.db.execute_write(query, params)

    def delete_student(self, student_id: str) -> bool:
        clean_id = self._clean_data(student_id)
        
        if not self.check_student_exists(clean_id):
            logging.warning(f"Từ chối xóa: Không tìm thấy mã sinh viên {clean_id}.")
            return False

        logging.info(f"Đang thực hiện lệnh xóa sinh viên mã: {clean_id}")
        query = "DELETE FROM Students WHERE StudentID = ?"
        return self.db.execute_write(query, (clean_id,))

    def search_students(self, keyword: str) -> Optional[List[Tuple[Any, ...]]]:
        clean_keyword = self._clean_data(keyword)
        logging.info(f"Đang tìm kiếm dữ liệu với từ khóa: '{clean_keyword}'")
        
        query = """
            SELECT StudentID, FullName, DateOfBirth, Gender, ClassID, Contact 
            FROM Students
            WHERE StudentID LIKE ? 
               OR FullName LIKE ? 
               OR ClassID LIKE ?
               OR Contact LIKE ?
            ORDER BY ClassID ASC, FullName ASC
        """
        search_pattern = f"%{clean_keyword}%"
        params = (search_pattern, search_pattern, search_pattern, search_pattern)
        
        return self.db.execute_read(query, params)

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    controller = StudentController()
    
    print("\n--- TEST: Làm sạch và chuẩn hóa dữ liệu ---")
    test_name = "   trần   đặng  duy an   "
    print(f"Chuỗi gốc: '{test_name}'")
    print(f"Sau chuẩn hóa: '{controller._format_name(test_name)}'")
    
    print("\n--- TEST: Tìm kiếm ---")
    results = controller.search_students("AI")
    if results:
        print(f"Đã tìm thấy {len(results)} kết quả.")
    else:
        print("Không tìm thấy kết quả nào.")