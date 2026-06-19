import tkinter as tk
from tkinter import ttk, messagebox
import logging
from controllers import StudentController
from utils import DataValidator, DataExporter, DataVisualizer

class StudentView:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Hệ thống Quản lý Sinh viên - Phát triển bởi: Trần Đặng Duy An")
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
        self.status_var.set("Hệ thống đã sẵn sàng.")
        self._build_header()
        self._build_main_content()
        self._build_status_bar()
        self.load_data_to_table()

    def _configure_styles(self):
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')

        style.configure("Treeview", 
                        background="#ffffff",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#ffffff",
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading", 
                        font=("Segoe UI", 10, "bold"), 
                        background="#005A9E",
                        foreground="white")
        style.map('Treeview', background=[('selected', '#CCE8FF')])
        style.configure("TLabelframe", font=("Segoe UI", 12, "bold"))
        style.configure("TLabelframe.Label", font=("Segoe UI", 12, "bold"), foreground="#005A9E")

    def _build_header(self):
        header_frame = tk.Frame(self.root, bg="#005A9E", pady=15)
        header_frame.pack(side=tk.TOP, fill=tk.X)
        
        title_label = tk.Label(header_frame, text="CHƯƠNG TRÌNH QUẢN LÝ THÔNG TIN SINH VIÊN", 
                               font=("Segoe UI", 20, "bold"), bg="#005A9E", fg="white")
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
        left_frame = ttk.LabelFrame(parent, text=" 📝 Thông tin chi tiết ")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        form_frame = tk.Frame(left_frame, padx=10, pady=10)
        form_frame.pack(fill=tk.X)

        labels = ["Mã sinh viên (*):", "Họ và tên (*):", "Ngày sinh:", "Giới tính:", "Mã Lớp (*):", "Liên hệ:"]
        variables = [self.var_id, self.var_name, self.var_dob, self.var_gender, self.var_class, self.var_contact]

        for i, (lbl, var) in enumerate(zip(labels, variables)):
            tk.Label(form_frame, text=lbl, font=("Segoe UI", 11)).grid(row=i, column=0, pady=12, sticky="w")
            
            if lbl == "Giới tính:":
                combo = ttk.Combobox(form_frame, textvariable=var, font=("Segoe UI", 11), state="readonly", width=22)
                combo['values'] = ("Nam", "Nữ", "Khác")
                combo.grid(row=i, column=1, pady=12, padx=10, sticky="ew")
            else:
                entry = ttk.Entry(form_frame, textvariable=var, font=("Segoe UI", 11), width=24)
                entry.grid(row=i, column=1, pady=12, padx=10, sticky="ew")
                if lbl == "Ngày sinh:":
                    entry.insert(0, "YYYY-MM-DD")
        btn_frame = tk.Frame(left_frame, pady=10)
        btn_frame.pack(fill=tk.X)
        btn_frame.columnconfigure((0, 1, 2, 3), weight=1)

        btn_configs = [
            ("Thêm", "green", self.add_student),
            ("Sửa", "orange", self.update_student),
            ("Xóa", "red", self.delete_student),
            ("Mới", "gray", self.clear_form)
        ]

        for i, (text, color, command) in enumerate(btn_configs):
            btn = tk.Button(btn_frame, text=text, bg=color, fg="white", font=("Segoe UI", 10, "bold"), 
                            command=command, cursor="hand2")
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
        util_frame = tk.Frame(left_frame, pady=5)
        util_frame.pack(fill=tk.X)
        util_frame.columnconfigure((0, 1), weight=1)
        
        tk.Button(util_frame, text="📊 Thống kê Giới tính", bg="#107C41", fg="white", font=("Segoe UI", 10, "bold"), 
                  command=self.show_statistics, cursor="hand2").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(util_frame, text="📥 Xuất file Excel", bg="#0078D4", fg="white", font=("Segoe UI", 10, "bold"), 
                  command=self.export_data, cursor="hand2").grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    def _build_right_panel(self, parent):
        right_frame = ttk.LabelFrame(parent, text=" 📋 Danh sách Sinh viên ")
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(0, weight=1)
        search_frame = tk.Frame(right_frame, pady=10, padx=10)
        search_frame.grid(row=0, column=0, sticky="ew")
        
        tk.Label(search_frame, text="🔍 Tìm kiếm:", font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=(0, 5))
        search_entry = ttk.Entry(search_frame, textvariable=self.var_search, font=("Segoe UI", 11), width=30)
        search_entry.pack(side=tk.LEFT, padx=5) 
        search_entry.bind("<Return>", lambda event: self.search_data())
        
        tk.Button(search_frame, text="Tìm kiếm", bg="#005A9E", fg="white", font=("Segoe UI", 10, "bold"), 
                  command=self.search_data, cursor="hand2").pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Tải lại", bg="#6c757d", fg="white", font=("Segoe UI", 10, "bold"), 
                  command=self.load_data_to_table, cursor="hand2").pack(side=tk.LEFT, padx=5)

        table_container = tk.Frame(right_frame)
        table_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        table_container.rowconfigure(0, weight=1)
        table_container.columnconfigure(0, weight=1)

        scroll_y = ttk.Scrollbar(table_container, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(table_container, orient=tk.HORIZONTAL)

        self.student_table = ttk.Treeview(table_container, 
                                          columns=("ID", "Name", "DOB", "Gender", "Class", "Contact"), 
                                          yscrollcommand=scroll_y.set, 
                                          xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.student_table.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.config(command=self.student_table.xview)
        scroll_x.grid(row=1, column=0, sticky="ew")

        columns_config = {
            "ID": ("Mã SV", 90),
            "Name": ("Họ tên", 200),
            "DOB": ("Ngày sinh", 100),
            "Gender": ("Giới tính", 80),
            "Class": ("Lớp", 90),
            "Contact": ("Liên hệ", 120)
        }
        
        self.student_table['show'] = 'headings'
        for col, (text, width) in columns_config.items():
            self.student_table.heading(col, text=text, anchor=tk.W)
            self.student_table.column(col, width=width, anchor=tk.W)

        self.student_table.grid(row=0, column=0, sticky="nsew")
        self.student_table.bind("<ButtonRelease-1>", self.get_cursor_data)

    def _build_status_bar(self):
        status_bar = tk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor="w", 
                              font=("Segoe UI", 9), bg="#f1f1f1", padx=10, pady=2)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    def set_status(self, message: str):
        self.status_var.set(f"Trạng thái: {message}")
        logging.info(f"UI Status: {message}")

    def clear_form(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_dob.set("")
        self.var_gender.set("")
        self.var_class.set("")
        self.var_contact.set("")
        self.var_search.set("")
        self.set_status("Đã làm trống form nhập liệu.")

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
            self.set_status(f"Đang xem thông tin sinh viên: {row[0]}")

    def load_data_to_table(self):
        for item in self.student_table.get_children():
            self.student_table.delete(item)
            
        rows = self.controller.get_all_students()
        if rows:
            for row in rows:
                self.student_table.insert('', tk.END, values=row)
            self.set_status(f"Tải thành công {len(rows)} bản ghi dữ liệu.")
        else:
            self.set_status("Cơ sở dữ liệu đang trống hoặc mất kết nối.")

    def _validate_inputs(self) -> bool:
        if not self.var_id.get() or not self.var_name.get() or not self.var_class.get():
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ các trường bắt buộc (*).")
            return False
        dob = self.var_dob.get()
        if dob and dob != "YYYY-MM-DD" and not DataValidator.is_valid_date(dob):
            messagebox.showerror("Lỗi dữ liệu", "Ngày sinh phải đúng định dạng YYYY-MM-DD!")
            return False
            
        if self.var_contact.get() and not DataValidator.is_valid_phone(self.var_contact.get()):
            messagebox.showerror("Lỗi dữ liệu", "Số điện thoại không hợp lệ (Cần 10-11 số, bắt đầu bằng số 0).")
            return False
            
        return True

    def add_student(self):
        if not self._validate_inputs(): return
        dob_val = self.var_dob.get() if self.var_dob.get() != "YYYY-MM-DD" else ""
        
        success = self.controller.add_student(
            self.var_id.get(), self.var_name.get(), dob_val,
            self.var_gender.get(), self.var_class.get(), self.var_contact.get()
        )
        if success:
            messagebox.showinfo("Thành công", f"Đã thêm sinh viên {self.var_name.get()} vào hệ thống.")
            self.load_data_to_table()
            self.clear_form()
        else:
            messagebox.showerror("Lỗi", "Thêm thất bại. Mã sinh viên có thể đã tồn tại!")
            self.set_status("Lỗi thêm dữ liệu: Vi phạm ràng buộc khóa.")

    def update_student(self):
        if not self.var_id.get():
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một sinh viên trên bảng để cập nhật.")
            return
        if not self._validate_inputs(): return

        dob_val = self.var_dob.get() if self.var_dob.get() != "YYYY-MM-DD" else ""

        success = self.controller.update_student(
            self.var_id.get(), self.var_name.get(), dob_val,
            self.var_gender.get(), self.var_class.get(), self.var_contact.get()
        )
        if success:
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin thành công.")
            self.load_data_to_table()
            self.clear_form()
        else:
            messagebox.showerror("Lỗi", "Quá trình cập nhật thất bại.")

    def delete_student(self):
        target_id = self.var_id.get()
        if not target_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sinh viên cần xóa.")
            return
            
        confirm = messagebox.askyesno("Xác nhận nguy hiểm", f"Bạn có chắc chắn muốn xóa toàn bộ dữ liệu của sinh viên mã {target_id}?\nHành động này không thể hoàn tác!")
        if confirm:
            if self.controller.delete_student(target_id):
                messagebox.showinfo("Thành công", "Dữ liệu sinh viên đã bị xóa.")
                self.load_data_to_table()
                self.clear_form()
            else:
                messagebox.showerror("Lỗi", "Không thể xóa sinh viên này (Có thể do ràng buộc bảng Điểm).")

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
            self.set_status(f"Tìm kiếm '{keyword}': Tìm thấy {len(rows)} kết quả.")
        else:
            self.set_status(f"Tìm kiếm '{keyword}': Không có kết quả phù hợp.")
            messagebox.showinfo("Kết quả tìm kiếm", "Không tìm thấy sinh viên nào khớp với từ khóa.")

    def export_data(self):
        rows = self.controller.get_all_students()
        if DataExporter.export_to_csv(rows):
            self.set_status("Đã xuất danh sách sinh viên ra file CSV.")

    def show_statistics(self):
        rows = self.controller.get_all_students()
        if not rows: return
        
        self.set_status("Đang khởi tạo biểu đồ thống kê...")
        nam, nu, khac = 0, 0, 0
        for row in rows:
            gender = str(row[3]).strip().title()
            if gender == "Nam": nam += 1
            elif gender == "Nữ": nu += 1
            else: khac += 1
            
        DataVisualizer.plot_gender_ratio(nam, nu, khac)
        self.set_status("Hoàn tất hiển thị thống kê.")