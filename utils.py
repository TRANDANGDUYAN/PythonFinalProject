import re
import csv
import logging
from datetime import datetime
from pathlib import Path
from tkinter import messagebox
from typing import List, Tuple, Any
import matplotlib.pyplot as plt

logger = logging.getLogger("DataUtilities")

class DataValidator:
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        if not phone:
            return True
        clean_phone = phone.strip()
        pattern = r"^(0)[3|5|7|8|9][0-9]{8}$"
        if bool(re.match(pattern, clean_phone)):
            return True
        logger.warning(f"Validation failed for phone number: {clean_phone}")
        return False

    @staticmethod
    def is_valid_date(date_str: str) -> bool:
        if not date_str:
            return True
        try:
            parsed_date = datetime.strptime(date_str.strip(), '%d-%m-%Y')
            if parsed_date > datetime.now():
                logger.warning("Validation failed: Future date provided.")
                return False
            return True
        except ValueError:
            logger.warning(f"Validation failed for date format: {date_str}")
            return False

class DataExporter:
    @staticmethod
    def export_to_csv(data_list: List[Tuple[Any, ...]], base_filename: str = "StudentList") -> bool:
        if not data_list:
            messagebox.showwarning("Warning", "No data available to export.")
            logger.info("Export aborted: Empty dataset.")
            return False
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{base_filename}_{timestamp}.csv"
            export_path = Path.cwd() / filename
            with open(export_path, mode='w', encoding='utf-8-sig', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Student ID", "Full Name", "Date of Birth", "Gender", "Class ID", "Contact"])
                for row in data_list:
                    clean_row = [str(item).strip() if item is not None else "" for item in row]
                    writer.writerow(clean_row)
            logger.info(f"Report successfully exported to: {export_path}")
            messagebox.showinfo("Export Successful", f"Data saved securely at:\n{filename}")
            return True
        except PermissionError:
            logger.error("Export Error: Permission denied or file currently open.")
            messagebox.showerror("Access Error", "Cannot save file. Ensure it is not open in another application.")
            return False
        except Exception as e:
            logger.error(f"System error during export: {e}")
            messagebox.showerror("System Error", f"An error occurred during export:\n{e}")
            return False

class DataVisualizer:
    @staticmethod
    def plot_class_statistics(class_counts):
        if not class_counts:
            messagebox.showinfo("Information", "No student data available for statistics.")
            return
            
        import matplotlib.pyplot as plt

        labels = [f"{cls} ({count})" for cls, count in class_counts.items()]
        sizes = list(class_counts.values())
        colors = ['#2E86C1', '#E74C3C', '#F1C40F', '#107C41', '#ff9900', '#7a2485', '#00b7c3']
        explode = [0.05] * len(labels)
        
        fig, ax = plt.subplots(figsize=(7, 6), facecolor='#F8F9F9')

        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            autopct='%1.1f%%',
            startangle=140,
            colors=colors[:len(labels)],
            explode=explode,
            shadow=True,
            textprops={'fontsize': 11, 'fontweight': 'bold', 'color': '#333333'}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            
        plt.title('TỶ LỆ PHÂN BỔ SINH VIÊN THEO LỚP HỌC', fontsize=14, fontweight='bold', color='#1A5276', pad=20)
        ax.axis('equal') 
        fig.canvas.manager.set_window_title('System Statistics')
        plt.tight_layout()
        plt.show()