import sys
import logging
import traceback
import tkinter as tk
from tkinter import messagebox
from views import StudentView
from database import Database

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("app_system.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def global_exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.critical("CRITICAL ERROR: Phần mềm gặp sự cố nghiêm trọng!", exc_info=(exc_type, exc_value, exc_traceback))

    error_msg = "".join(traceback.format_exception_only(exc_type, exc_value)).strip()
    messagebox.showerror("Sự cố Hệ thống", 
                         f"Phần mềm vừa gặp một lỗi bất ngờ và đã được ghi lại vào file app_system.log.\n\nChi tiết lỗi:\n{error_msg}")
sys.excepthook = global_exception_handler

def center_window(window: tk.Tk, width: int, height: int):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def main():
    logging.info("="*50)
    logging.info("KHỞI ĐỘNG HỆ THỐNG QUẢN LÝ SINH VIÊN")
    logging.info("="*50)

    db = Database()
    if not db.connect():
        logging.warning("Phần mềm khởi chạy trong trạng thái mất kết nối với SQL Server.")

    root = tk.Tk()

    APP_WIDTH = 1250
    APP_HEIGHT = 700

    app = StudentView(root)

    center_window(root, APP_WIDTH, APP_HEIGHT)

    def on_closing():
        logging.info("Người dùng đang đóng phần mềm...")
        db.disconnect()
        root.destroy()
        logging.info("HỆ THỐNG ĐÃ TẮT AN TOÀN.")
        logging.info("="*50)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

if __name__ == "__main__":
    main()