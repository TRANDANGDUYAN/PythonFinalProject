import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging
from controllers import StudentController
from utils import DataValidator, DataExporter, DataVisualizer

class StudentView:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Student Management System - Developed by Tran Dang Duy An (VKU)")
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
                if lbl == "Date of Birth:":
                    entry.insert(0, "DD-MM-YYYY")

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
        util_frame.columnconfigure((0, 1), weight=1)
        
        tk.Button(util_frame, text="Gender Statistics", bg="#107C41", fg="white", font=("Segoe UI", 10, "bold"), command=self.show_statistics, cursor="hand2").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(util_frame, text="Export to Excel", bg="#0078D4", fg="white", font=("Segoe UI", 10, "bold"), command=self.export_data, cursor="hand2").grid(row=0, column=1, padx=5, pady=5, sticky="ew")

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
        if dob and dob != "DD-MM-YYYY":
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
        
        dob_val = self.var_dob.get() if self.var_dob.get() != "DD-MM-YYYY" else ""
        
        success = self.controller.add_student(
            self.var_id.get(), self.var_name.get(), dob_val,
            self.var_gender.get(), self.var_class.get(), self.var_contact.get()
        )
        if success:
            messagebox.showinfo("Success", f"Student {self.var_name.get()} added successfully.")
            self.load_data_to_table()
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to add student. ID might already exist.")
            self.set_status("Data addition error: Constraint violation.")

    def update_student(self):
        if not self.var_id.get():
            messagebox.showwarning("Warning", "Please select a student from the list to update.")
            return
        if not self._validate_inputs(): return

        dob_val = self.var_dob.get() if self.var_dob.get() != "DD-MM-YYYY" else ""

        success = self.controller.update_student(
            self.var_id.get(), self.var_name.get(), dob_val,
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
        if not rows: return
        
        self.set_status("Generating statistical chart...")
        male, female, other = 0, 0, 0
        for row in rows:
            gender = str(row[3]).strip().title()
            if gender == "Male": male += 1
            elif gender == "Female": female += 1
            else: other += 1
            
        DataVisualizer.plot_gender_ratio(male, female, other)
        self.set_status("Statistics displayed.")