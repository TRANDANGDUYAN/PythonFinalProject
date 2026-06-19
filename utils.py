import re
import csv
import logging
from datetime import datetime
from pathlib import Path
from tkinter import messagebox
from typing import List, Tuple, Any
import matplotlib.pyplot as plt

class DataValidator:

    @staticmethod
    def is_valid_phone(phone: str) -> bool:

        if not phone: 
            return True
            
        clean_phone = phone.strip()
        pattern = r"^(0)[3|5|7|8|9][0-9]{8}$"
        
        if bool(re.match(pattern, clean_phone)):
            return True
        else:
            logging.warning(f"Lỗi xác thực: Số điện thoại '{clean_phone}' không hợp lệ.")
            return False

    @staticmethod
    def is_valid_date(date_str: str) -> bool:

        if not date_str: 
            return True
            
        try:
            parsed_date = datetime.strptime(date_str.strip(), '%Y-%m-%d')
            if parsed_date > datetime.now():
                logging.warning("Lỗi xác thực: Ngày sinh lớn hơn ngày hiện tại.")
                return False
                
            return True
        except ValueError:
            logging.warning(f"Lỗi xác thực: Ngày sinh '{date_str}' sai định dạng.")
            return False


class DataExporter:

    @staticmethod
    def export_to_csv(data_list: List[Tuple[Any, ...]], base_filename: str = "DanhSachSinhVien") -> bool:

        if not data_list:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu trong hệ thống để xuất báo cáo!")
            logging.info("Hủy xuất file: Dữ liệu trống.")
            return False
            
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{base_filename}_{timestamp}.csv"

            export_path = Path.cwd() / filename
            
            with open(export_path, mode='w', encoding='utf-8-sig', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Mã Sinh Viên", "Họ và Tên", "Ngày Sinh", "Giới Tính", "Mã Lớp", "Liên Hệ"])
                for row in data_list:
                    clean_row = [str(item).strip() if item is not None else "" for item in row]
                    writer.writerow(clean_row)
                    
            logging.info(f"Đã xuất báo cáo thành công tại: {export_path}")
            messagebox.showinfo("Xuất file thành công", f"Dữ liệu đã được lưu an toàn tại:\n{filename}")
            return True
            
        except PermissionError:
            logging.error("Lỗi xuất file: Không có quyền ghi hoặc file đang bị mở bởi phần mềm khác.")
            messagebox.showerror("Lỗi Truy cập", "Không thể lưu file! Hãy chắc chắn rằng bạn không đang mở file trùng tên trong Excel.")
            return False
        except Exception as e:
            logging.error(f"Lỗi hệ thống khi xuất file: {e}")
            messagebox.showerror("Lỗi Hệ thống", f"Đã xảy ra lỗi khi xuất dữ liệu:\n{e}")
            return False


class DataVisualizer:

    @staticmethod
    def plot_gender_ratio(male_count: int, female_count: int, other_count: int = 0):

        total = male_count + female_count + other_count
        if total == 0:
            logging.warning("Từ chối vẽ biểu đồ: Tổng số sinh viên bằng 0.")
            messagebox.showinfo("Thông báo", "Chưa có dữ liệu sinh viên để tạo thống kê!")
            return

        logging.info(f"Đang tạo biểu đồ thống kê cho {total} sinh viên...")

        labels = []
        sizes = []
        colors = []
        explode = []
        
        if male_count > 0:
            labels.append(f'Nam ({male_count})')
            sizes.append(male_count)
            colors.append('#2E86C1')
            explode.append(0.05)
            
        if female_count > 0:
            labels.append(f'Nữ ({female_count})')
            sizes.append(female_count)
            colors.append('#E74C3C')
            explode.append(0.05)
            
        if other_count > 0:
            labels.append(f'Khác ({other_count})')
            sizes.append(other_count)
            colors.append('#F1C40F')
            explode.append(0.05)

        fig, ax = plt.subplots(figsize=(7, 6), facecolor='#F8F9F9')

        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            colors=colors, 
            autopct='%1.1f%%', 
            startangle=140,
            explode=explode,
            shadow=True, # Đổ bóng cho đẹp
            textprops={'fontsize': 11, 'fontweight': 'bold', 'color': '#333333'}
        )

        for autotext in autotexts:
            autotext.set_color('white')

        plt.title('PHÂN TÍCH TỶ LỆ GIỚI TÍNH SINH VIÊN', fontsize=14, fontweight='bold', color='#1A5276', pad=20)

        ax.axis('equal')  
        fig.canvas.manager.set_window_title('Thống kê Hệ thống')
        plt.tight_layout()
        plt.show()
        logging.info("Đã đóng cửa sổ thống kê.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    print("--- KIỂM TRA VALIDATION ĐỊNH DẠNG ---")
    print(f"Số ĐT '0901234567' -> Hợp lệ: {DataValidator.is_valid_phone('0901234567')}")
    print(f"Số ĐT '0123456789' (Đầu 01 cũ) -> Hợp lệ: {DataValidator.is_valid_phone('0123456789')}")
    print(f"Ngày sinh '2050-01-01' (Tương lai) -> Hợp lệ: {DataValidator.is_valid_date('2050-01-01')}")