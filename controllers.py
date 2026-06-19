import logging
from datetime import datetime
from typing import List, Tuple, Optional, Any
from database import Database

logger = logging.getLogger("StudentController")

class StudentController:
    def __init__(self):
        self.db = Database()
        self.db_date_format = "%Y-%m-%d"
        self.view_date_format = "%d-%m-%Y"

    def _clean_text(self, text: Any) -> str:
        if isinstance(text, str):
            return text.strip()
        return str(text) if text is not None else ""

    def _format_name(self, name: str) -> str:
        return self._clean_text(name).title()

    def _convert_date_to_db_format(self, date_str: str) -> str:
        clean_date = self._clean_text(date_str)
        if not clean_date:
            return ""
        try:
            parsed_date = datetime.strptime(clean_date, self.view_date_format)
            return parsed_date.strftime(self.db_date_format)
        except ValueError:
            logger.error(f"Date conversion error. Expected {self.view_date_format}, got {clean_date}")
            return ""

    def _convert_date_to_view_format(self, date_obj: Any) -> str:
        if not date_obj:
            return ""
        if isinstance(date_obj, str):
            try:
                parsed_date = datetime.strptime(date_obj, self.db_date_format)
                return parsed_date.strftime(self.view_date_format)
            except ValueError:
                return date_obj
        if isinstance(date_obj, datetime) or hasattr(date_obj, 'strftime'):
            return date_obj.strftime(self.view_date_format)
        return str(date_obj)

    def _process_fetched_rows(self, rows: Optional[List[Tuple[Any, ...]]]) -> Optional[List[Tuple[Any, ...]]]:
        if not rows:
            return rows
        processed_rows = []
        for row in rows:
            row_list = list(row)
            if len(row_list) > 2 and row_list[2]:
                row_list[2] = self._convert_date_to_view_format(row_list[2])
            processed_rows.append(tuple(row_list))
        return processed_rows

    def check_student_exists(self, student_id: str) -> bool:
        clean_id = self._clean_text(student_id)
        query = "SELECT 1 FROM Students WHERE StudentID = ?"
        result = self.db.execute_read(query, (clean_id,))
        return bool(result)

    def get_all_students(self) -> Optional[List[Tuple[Any, ...]]]:
        query = """
            SELECT StudentID, FullName, DateOfBirth, Gender, ClassID, Contact 
            FROM Students
            ORDER BY ClassID ASC, FullName ASC
        """
        raw_rows = self.db.execute_read(query)
        return self._process_fetched_rows(raw_rows)

    def add_student(self, student_id: str, fullname: str, dob: str, gender: str, class_id: str, contact: str) -> bool:
        clean_id = self._clean_text(student_id)
        
        if self.check_student_exists(clean_id):
            logger.warning(f"Addition rejected. Student ID {clean_id} already exists.")
            return False

        formatted_name = self._format_name(fullname)
        clean_class = self._clean_text(class_id).upper()
        db_ready_dob = self._convert_date_to_db_format(dob)
        
        query = """
            INSERT INTO Students (StudentID, FullName, DateOfBirth, Gender, ClassID, Contact)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (clean_id, formatted_name, db_ready_dob, 
                  self._clean_text(gender), clean_class, self._clean_text(contact))
        
        return self.db.execute_write(query, params)

    def update_student(self, student_id: str, fullname: str, dob: str, gender: str, class_id: str, contact: str) -> bool:
        clean_id = self._clean_text(student_id)
        formatted_name = self._format_name(fullname)
        clean_class = self._clean_text(class_id).upper()
        db_ready_dob = self._convert_date_to_db_format(dob)

        query = """
            UPDATE Students 
            SET FullName = ?, DateOfBirth = ?, Gender = ?, ClassID = ?, Contact = ?
            WHERE StudentID = ?
        """
        params = (formatted_name, db_ready_dob, self._clean_text(gender), 
                  clean_class, self._clean_text(contact), clean_id)
                  
        return self.db.execute_write(query, params)

    def delete_student(self, student_id: str) -> bool:
        clean_id = self._clean_text(student_id)
        
        if not self.check_student_exists(clean_id):
            logger.warning(f"Deletion rejected. Student ID {clean_id} not found.")
            return False

        query = "DELETE FROM Students WHERE StudentID = ?"
        return self.db.execute_write(query, (clean_id,))

    def search_students(self, keyword: str) -> Optional[List[Tuple[Any, ...]]]:
        clean_keyword = self._clean_text(keyword)
        
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
        
        raw_rows = self.db.execute_read(query, params)
        return self._process_fetched_rows(raw_rows)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    controller = StudentController()
    test_data = controller.get_all_students()
    if test_data:
        for item in test_data:
            print(item)