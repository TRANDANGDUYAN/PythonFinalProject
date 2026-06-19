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

        result = self.db.fetch_query(query, (clean_id,))
        return bool(result)

    def get_all_students(self) -> Optional[List[Tuple[Any, ...]]]:
        query = """
            SELECT StudentID, FullName, DateOfBirth, Gender, ClassID, Contact 
            FROM Students
            ORDER BY ClassID ASC, FullName ASC
        """

        raw_rows = self.db.fetch_query(query)
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

        return self.db.execute_query(query, params)

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
        return self.db.execute_query(query, params)

    def delete_student(self, student_id: str) -> bool:
        clean_id = self._clean_text(student_id)
        
        if not self.check_student_exists(clean_id):
            logger.warning(f"Deletion rejected. Student ID {clean_id} not found.")
            return False

        query = "DELETE FROM Students WHERE StudentID = ?"
        return self.db.execute_query(query, (clean_id,))

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
        raw_rows = self.db.fetch_query(query, params)
        return self._process_fetched_rows(raw_rows)

    def get_all_subjects(self) -> Optional[List[Tuple[Any, ...]]]:
        query = "SELECT SubjectID, SubjectName FROM Subjects"
        return self.db.fetch_query(query)

    def get_student_grades(self, student_id: str) -> Optional[List[Tuple[Any, ...]]]:
        clean_id = self._clean_text(student_id)
        query = """
            SELECT s.SubjectID, s.SubjectName, 
                   g.AttendanceScore, g.AssignmentScore, g.MidtermScore, g.FinalScore
            FROM Subjects s
            LEFT JOIN Grades g ON s.SubjectID = g.SubjectID AND g.StudentID = ?
        """
        raw_grades = self.db.fetch_query(query, (clean_id,))
        
        if not raw_grades:
            return []

        processed = []
        for row in raw_grades:
            subj_id, subj_name, cc, bt, gk, ck = row
            total = None
            
            if cc is not None and gk is not None and ck is not None:
                if bt is not None: 
                    total = round(cc * 0.1 + bt * 0.2 + gk * 0.2 + ck * 0.5, 2)
                else: 
                    total = round(cc * 0.2 + gk * 0.2 + ck * 0.6, 2)
                    
            processed.append((subj_id, subj_name, cc, bt, gk, ck, total))
            
        return processed

    def save_grade(self, student_id: str, subject_id: str, cc: float, bt: Optional[float], gk: float, ck: float) -> bool:
        clean_student = self._clean_text(student_id)
        clean_subject = self._clean_text(subject_id)
        
        check_query = "SELECT 1 FROM Grades WHERE StudentID = ? AND SubjectID = ?"
        exists = self.db.fetch_query(check_query, (clean_student, clean_subject))
        
        if exists:
            update_query = """
                UPDATE Grades 
                SET AttendanceScore = ?, AssignmentScore = ?, MidtermScore = ?, FinalScore = ? 
                WHERE StudentID = ? AND SubjectID = ?
            """
            return self.db.execute_query(update_query, (cc, bt, gk, ck, clean_student, clean_subject))
        else:
            insert_query = """
                INSERT INTO Grades (StudentID, SubjectID, AttendanceScore, AssignmentScore, MidtermScore, FinalScore) 
                VALUES (?, ?, ?, ?, ?, ?)
            """
            return self.db.execute_query(insert_query, (clean_student, clean_subject, cc, bt, gk, ck))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    controller = StudentController()
    test_data = controller.get_all_students()
    if test_data:
        for item in test_data:
            print(item)