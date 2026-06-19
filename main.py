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
    datefmt='%d-%m-%Y %H:%M:%S',
    handlers=[
        logging.FileHandler("app_system.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def global_exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.critical("CRITICAL ERROR: Application encountered a crash!", exc_info=(exc_type, exc_value, exc_traceback))
    error_msg = "".join(traceback.format_exception_only(exc_type, exc_value)).strip()
    messagebox.showerror("System Crash", f"An unexpected error occurred. Please check app_system.log.\n\nError details:\n{error_msg}")

sys.excepthook = global_exception_handler

def center_window(window: tk.Tk, width: int, height: int):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def main():
    logging.info("INITIALIZING STUDENT MANAGEMENT SYSTEM")
    
    db = Database()
    if not db.connect():
        logging.warning("System started in offline mode (Database connection failed).")
    
    root = tk.Tk()
    APP_WIDTH = 1250
    APP_HEIGHT = 700
    
    app = StudentView(root)
    center_window(root, APP_WIDTH, APP_HEIGHT)
    
    def on_closing():
        logging.info("Shutting down system...")
        db.disconnect()
        root.destroy()
        logging.info("SYSTEM TERMINATED SAFELY.")
        sys.exit(0)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()