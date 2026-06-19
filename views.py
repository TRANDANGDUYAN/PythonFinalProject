import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging
from controllers import StudentController
from utils import DataValidator, DataExporter, DataVisualizer

class StudentView:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1250x700")
        self.root.minsize(1000, 600)
        
        self._configure_styles()
        self.controller = StudentController()

        self.var_id = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_dob = tk.StringVar()
        self.var_gender = tk.StringVar()
        self.var_class = tk.StringVar()
        self.var_contact = tk.StringVar()
        self.var_search = tk.StringVar()
        self.status_var = tk.StringVar()
        self.status_var.set("System is ready.")

        self._build_header()
        self._build_main_content()
        self._build_status_bar()
        self.load_data_to_table()

    def _configure_styles(self):
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
            
        style.configure("Treeview", background="#ffffff", foreground="black", rowheight=25, fieldbackground="#ffffff", font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#005A9E", foreground="white")
        style.map('Treeview', background=[('selected', '#CCE8FF')])
        style.configure("TLabelframe", font=("Segoe UI", 12, "bold"))
        style.configure("TLabelframe.Label", font=("Segoe UI", 12, "bold"), foreground="#005A9E")

    def _build_header(self):
        header_frame = tk.Frame(self.root, bg="#005A9E", pady=15)
        header_frame.pack(side=tk.TOP, fill=tk.X)
        title_label = tk.Label(header_frame, text="STUDENT INFORMATION MANAGEMENT SYSTEM", font=("Segoe UI", 20, "bold"), bg="#005A9E", fg="white")
        title_label.pack()

    def _build_main_content(self):
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=0, minsize=420)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        self._build_left_panel(main_frame)
        self._build_right_panel(main_frame)

    def _build_left_panel(self, parent):
        left_frame = ttk.LabelFrame(parent, text=" Student Details ")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        form_frame = tk.Frame(left_frame, padx=10, pady=10)
        form_frame.pack(fill=tk.X)

        labels = ["Student ID (*):", "Full Name (*):", "Date of Birth:", "Gender:", "Class ID (*):", "Contact:"]
        variables = [self.var_id, self.var_name, self.var_dob, self.var_gender, self.var_class, self.var_contact]

        for i, (lbl, var) in enumerate(zip(labels, variables)):
            tk.Label(form_frame, text=lbl, font=("Segoe UI", 11)).grid(row=i, column=0, pady=12, sticky="w")
            if lbl == "Gender:":
                combo = ttk.Combobox(form_frame, textvariable=var, font=("Segoe UI", 11), state="readonly", width=22)
                combo['values'] = ("Male", "Female", "Other")
                combo.grid(row=i, column=1, pady=12, padx=10, sticky="ew")
            else:
                entry = ttk.Entry(form_frame, textvariable=var, font=("Segoe UI", 11), width=24)
                entry.grid(row=i, column=1, pady=12, padx=10, sticky="ew")

        btn_frame = tk.Frame(left_frame, pady=10)
        btn_frame.pack(fill=tk.X)
        btn_frame.columnconfigure((0, 1, 2, 3), weight=1)

        btn_configs = [
            ("Add", "green", self.add_student),
            ("Update", "orange", self.update_student),
            ("Delete", "red", self.delete_student),
            ("Clear", "gray", self.clear_form)
        ]

        for i, (text, color, command) in enumerate(btn_configs):
            btn = tk.Button(btn_frame, text=text, bg=color, fg="white", font=("Segoe UI", 10, "bold"), command=command, cursor="hand2")
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")

        util_frame = tk.Frame(left_frame, pady=5)
        util_frame.pack(fill=tk.X)
        util_frame.columnconfigure((0, 1, 2), weight=1)
        
        tk.Button(util_frame, text="Class Statistics", bg="#107C41", fg="white", font=("Segoe UI", 10, "bold"), command=self.show_statistics, cursor="hand2").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(util_frame, text="Export to Excel", bg="#0078D4", fg="white", font=("Segoe UI", 10, "bold"), command=self.export_data, cursor="hand2").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        tk.Button(util_frame, text="Manage Grades", bg="#ff9900", fg="black", font=("Segoe UI", 10, "bold"), command=self.open_grading_window, cursor="hand2").grid(row=0, column=2, padx=5, pady=5, sticky="ew")

    def _build_right_panel(self, parent):
        right_frame = ttk.LabelFrame(parent, text=" Student List ")
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(0, weight=1)

        search_frame = tk.Frame(right_frame, pady=10, padx=10)
        search_frame.grid(row=0, column=0, sticky="ew")
        
        tk.Label(search_frame, text="Search:", font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=(0, 5))
        search_entry = ttk.Entry(search_frame, textvariable=self.var_search, font=("Segoe UI", 11), width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind("<Return>", lambda event: self.search_data())
        
        tk.Button(search_frame, text="Search", bg="#005A9E", fg="white", font=("Segoe UI", 10, "bold"), command=self.search_data, cursor="hand2").pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Refresh", bg="#6c757d", fg="white", font=("Segoe UI", 10, "bold"), command=self.load_data_to_table, cursor="hand2").pack(side=tk.LEFT, padx=5)

        table_container = tk.Frame(right_frame)
        table_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        table_container.rowconfigure(0, weight=1)
        table_container.columnconfigure(0, weight=1)

        scroll_y = ttk.Scrollbar(table_container, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(table_container, orient=tk.HORIZONTAL)

        self.student_table = ttk.Treeview(table_container, columns=("ID", "Name", "DOB", "Gender", "Class", "Contact"), yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.student_table.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.config(command=self.student_table.xview)
        scroll_x.grid(row=1, column=0, sticky="ew")

        columns_config = {
            "ID": ("Student ID", 90),
            "Name": ("Full Name", 200),
            "DOB": ("Date of Birth", 100),
            "Gender": ("Gender", 80),
            "Class": ("Class", 90),
            "Contact": ("Contact", 120)
        }
        
        self.student_table['show'] = 'headings'
        for col, (text, width) in columns_config.items():
            self.student_table.heading(col, text=text, anchor=tk.W)
            self.student_table.column(col, width=width, anchor=tk.W)

        self.student_table.grid(row=0, column=0, sticky="nsew")
        self.student_table.bind("<ButtonRelease-1>", self.get_cursor_data)

    def _build_status_bar(self):
        status_bar = tk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor="w", font=("Segoe UI", 9), bg="#f1f1f1", padx=10, pady=2)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def set_status(self, message: str):
        self.status_var.set(f"Status: {message}")
        logging.info(f"UI Status: {message}")

    def clear_form(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_dob.set("")
        self.var_gender.set("")
        self.var_class.set("")
        self.var_contact.set("")
        self.var_search.set("")
        self.set_status("Form cleared.")

    def get_cursor_data(self, event):
        cursor_row = self.student_table.focus()
        contents = self.student_table.item(cursor_row)
        row = contents.get('values')
        
        if row:
            self.var_id.set(row[0])
            self.var_name.set(row[1])
            self.var_dob.set(row[2])
            self.var_gender.set(row[3])
            self.var_class.set(row[4])
            self.var_contact.set(f"0{row[5]}" if str(row[5]).isdigit() and not str(row[5]).startswith('0') else str(row[5]))
            self.set_status(f"Viewing student: {row[0]}")

    def load_data_to_table(self):
        for item in self.student_table.get_children():
            self.student_table.delete(item)
            
        rows = self.controller.get_all_students()
        if rows:
            for row in rows:
                self.student_table.insert('', tk.END, values=row)
            self.set_status(f"Loaded {len(rows)} records successfully.")
        else:
            self.set_status("Database is empty or connection failed.")

    def _validate_inputs(self) -> bool:
        if not self.var_id.get() or not self.var_name.get() or not self.var_class.get():
            messagebox.showwarning("Warning", "Please fill in all mandatory fields (*).")
            return False
            
        dob = self.var_dob.get()
        if dob: 
            try:
                datetime.strptime(dob, "%d-%m-%Y")
            except ValueError:
                messagebox.showerror("Data Error", "Date of birth must be in DD-MM-YYYY format!")
                return False
                
        if self.var_contact.get() and not DataValidator.is_valid_phone(self.var_contact.get()):
            messagebox.showerror("Data Error", "Invalid phone number format.")
            return False
            
        return True

    def add_student(self):
        if not self._validate_inputs(): return
        if self.controller.check_student_exists(self.var_id.get()):
            messagebox.showerror("Lỗi ID", "Mã sinh viên này ĐÃ TỒN TẠI trong database!")
            return
        dob = self.var_dob.get()
        if dob:
            try:
                datetime.strptime(dob, "%d-%m-%Y")
            except ValueError:
                messagebox.showerror("Lỗi Ngày tháng", "Ngày tháng nhập sai định dạng DD-MM-YYYY!")
                return

        success = self.controller.add_student(
            self.var_id.get(), self.var_name.get(), dob,
            self.var_gender.get(), self.var_class.get(), self.var_contact.get()
        )
        
        if success:
            messagebox.showinfo("Success", "Thêm thành công!")
            self.load_data_to_table()
            self.clear_form()
        else:
            messagebox.showerror("Lỗi Database", "Lỗi không xác định. Kiểm tra lại kết nối SQL!")

    def update_student(self):
        if not self.var_id.get():
            messagebox.showwarning("Warning", "Please select a student from the list to update.")
            return
        if not self._validate_inputs(): return

        success = self.controller.update_student(
            self.var_id.get(), self.var_name.get(), self.var_dob.get(),
            self.var_gender.get(), self.var_class.get(), self.var_contact.get()
        )
        if success:
            messagebox.showinfo("Success", "Information updated successfully.")
            self.load_data_to_table()
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to update information.")

    def delete_student(self):
        target_id = self.var_id.get()
        if not target_id:
            messagebox.showwarning("Warning", "Please select a student to delete.")
            return
            
        confirm = messagebox.askyesno("Critical Action", f"Are you sure you want to delete student {target_id}?\nThis action cannot be undone!")
        if confirm:
            if self.controller.delete_student(target_id):
                messagebox.showinfo("Success", "Student deleted successfully.")
                self.load_data_to_table()
                self.clear_form()
            else:
                messagebox.showerror("Error", "Failed to delete student (Possible foreign key constraint).")

    def search_data(self):
        keyword = self.var_search.get().strip()
        if not keyword:
            self.load_data_to_table()
            return
            
        for item in self.student_table.get_children():
            self.student_table.delete(item)
            
        rows = self.controller.search_students(keyword)
        if rows:
            for row in rows:
                self.student_table.insert('', tk.END, values=row)
            self.set_status(f"Search '{keyword}': Found {len(rows)} results.")
        else:
            self.set_status(f"Search '{keyword}': No results found.")
            messagebox.showinfo("Search Results", "No students matched your search keyword.")

    def export_data(self):
        rows = self.controller.get_all_students()
        if DataExporter.export_to_csv(rows):
            self.set_status("Student list exported to CSV successfully.")

    def show_statistics(self):
        rows = self.controller.get_all_students()
        if not rows: 
            messagebox.showwarning("Thông báo", "Không có dữ liệu sinh viên để thống kê!")
            return
        
        self.set_status("Generating statistical chart...")

        class_counts = {}
        for row in rows:
            class_id = str(row[4]).strip().upper()
            if class_id:
                class_counts[class_id] = class_counts.get(class_id, 0) + 1

        DataVisualizer.plot_class_statistics(class_counts)
        self.set_status("Statistics displayed.")

    def open_grading_window(self):
        selected_row = self.student_table.focus() 
        if not selected_row:
            messagebox.showwarning("Warning", "Please select a student from the list to manage grades!")
            return

        row_data = self.student_table.item(selected_row)['values']
        student_id = row_data[0]
        student_name = row_data[1]

        grade_window = tk.Toplevel(self.root)
        grade_window.title(f"Quản lý Điểm số - {student_name} ({student_id})")
        grade_window.geometry("850x550") 
        grade_window.grab_set() 

        frame_top = tk.Frame(grade_window, padx=15, pady=15)
        frame_top.pack(fill=tk.X)

        tk.Label(frame_top, text="Môn học:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, pady=5, sticky=tk.W)
        cbo_subjects = ttk.Combobox(frame_top, width=35, state="readonly", font=("Segoe UI", 10))
        cbo_subjects.grid(row=0, column=1, columnspan=3, padx=10, pady=5, sticky=tk.W)
        
        subjects_data = self.controller.get_all_subjects()
        subject_dict = {}
        if subjects_data:
            subject_dict = {f"{row[0]} - {row[1]}": row[0] for row in subjects_data}
            cbo_subjects['values'] = list(subject_dict.keys())

        tk.Label(frame_top, text="Chuyên cần (CC):", font=("Segoe UI", 10)).grid(row=1, column=0, pady=5, sticky=tk.W)
        txt_cc = ttk.Entry(frame_top, width=10, font=("Segoe UI", 10))
        txt_cc.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        tk.Label(frame_top, text="Bài tập (Trống = Bỏ qua):", font=("Segoe UI", 10)).grid(row=1, column=2, pady=5, sticky=tk.W)
        txt_bt = ttk.Entry(frame_top, width=10, font=("Segoe UI", 10))
        txt_bt.grid(row=1, column=3, padx=10, pady=5, sticky=tk.W)

        tk.Label(frame_top, text="Giữa kỳ (GK):", font=("Segoe UI", 10)).grid(row=2, column=0, pady=5, sticky=tk.W)
        txt_gk = ttk.Entry(frame_top, width=10, font=("Segoe UI", 10))
        txt_gk.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        tk.Label(frame_top, text="Cuối kỳ (CK):", font=("Segoe UI", 10)).grid(row=2, column=2, pady=5, sticky=tk.W)
        txt_ck = ttk.Entry(frame_top, width=10, font=("Segoe UI", 10))
        txt_ck.grid(row=2, column=3, padx=10, pady=5, sticky=tk.W)

        frame_mid = tk.Frame(grade_window, padx=15, pady=5)
        frame_mid.pack(fill=tk.BOTH, expand=True)
        
        columns = ("SubjectID", "SubjectName", "CC", "BT", "GK", "CK", "Total", "Letter")
        tree_grades = ttk.Treeview(frame_mid, columns=columns, show="headings", height=8)
        
        headings = ["Mã Môn", "Tên Môn Học", "CC", "BT", "GK", "CK", "Tổng Điểm", "Điểm Chữ"]
        widths = [70, 220, 50, 50, 50, 50, 80, 80]
        
        for col, head, wid in zip(columns, headings, widths):
            tree_grades.heading(col, text=head)
            anchor = tk.W if col == "SubjectName" else tk.CENTER
            tree_grades.column(col, width=wid, anchor=anchor)
        
        tree_grades.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scroll_grades = ttk.Scrollbar(frame_mid, orient=tk.VERTICAL, command=tree_grades.yview)
        tree_grades.configure(yscrollcommand=scroll_grades.set)
        scroll_grades.pack(side=tk.RIGHT, fill=tk.Y)

        frame_bottom = tk.Frame(grade_window, padx=15, pady=10)
        frame_bottom.pack(fill=tk.X)
        lbl_gpa = tk.Label(frame_bottom, text="GPA Tích lũy: N/A", font=("Segoe UI", 12, "bold"), fg="#D83B01")
        lbl_gpa.pack(side=tk.LEFT)

        def load_grades():
            for item in tree_grades.get_children():
                tree_grades.delete(item)
            grades_data = self.controller.get_student_grades(student_id)
            
            total_gpa_points = 0.0
            count = 0

            if grades_data:
                for row in grades_data:
                    subj_id, subj_name, cc, bt, gk, ck, total = row
                    
                    cc_val = cc if cc is not None else "-"
                    bt_val = bt if bt is not None else "-"
                    gk_val = gk if gk is not None else "-"
                    ck_val = ck if ck is not None else "-"
                    total_val = total if total is not None else "-"
                    letter_val = "-"
                    
                    if total is not None:
                        if total >= 8.5:
                            letter_val = "A"
                            score_4 = 4.0
                        elif total >= 7.0:
                            letter_val = "B"
                            score_4 = 3.0
                        elif total >= 5.0:
                            letter_val = "C"
                            score_4 = 2.0
                        elif total >= 4.0:
                            letter_val = "D"
                            score_4 = 1.0
                        else:
                            letter_val = "F"
                            score_4 = 0.0
                        
                        total_gpa_points += score_4
                        count += 1

                    tree_grades.insert("", tk.END, values=(subj_id, subj_name, cc_val, bt_val, gk_val, ck_val, total_val, letter_val))

            if count > 0:
                gpa = round(total_gpa_points / count, 2)
                lbl_gpa.config(text=f"GPA Tích lũy: {gpa} / 4.0")
            else:
                lbl_gpa.config(text="GPA Tích lũy: N/A")

        def save_action():
            selected_subject = cbo_subjects.get()
            cc_str = txt_cc.get().strip()
            bt_str = txt_bt.get().strip()
            gk_str = txt_gk.get().strip()
            ck_str = txt_ck.get().strip()
            
            if not selected_subject or not cc_str or not gk_str or not ck_str:
                messagebox.showerror("Error", "Vui lòng chọn môn và nhập đủ điểm CC, GK, CK!")
                return
                
            try:
                cc = float(cc_str)
                gk = float(gk_str)
                ck = float(ck_str)
                bt = float(bt_str) if bt_str else None 
                
                for score in [s for s in (cc, bt, gk, ck) if s is not None]:
                    if score < 0 or score > 10:
                        messagebox.showerror("Error", "Điểm số phải từ 0 đến 10!")
                        return
            except ValueError:
                messagebox.showerror("Error", "Điểm số phải là số hợp lệ!")
                return
                
            subject_id = subject_dict[selected_subject]
            if self.controller.save_grade(student_id, subject_id, cc, bt, gk, ck):
                messagebox.showinfo("Success", "Lưu điểm thành công!")
                load_grades() 
                txt_cc.delete(0, tk.END)
                txt_bt.delete(0, tk.END)
                txt_gk.delete(0, tk.END)
                txt_ck.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Không thể lưu điểm.")

        btn_save = tk.Button(frame_top, text="Lưu Cập Nhật Điểm", bg="#005A9E", fg="white", font=("Segoe UI", 10, "bold"), command=save_action, cursor="hand2")
        btn_save.grid(row=2, column=4, padx=10, sticky=tk.S)

        load_grades()