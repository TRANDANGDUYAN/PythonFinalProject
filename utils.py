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
    def plot_gender_ratio(male_count: int, female_count: int, other_count: int = 0):
        total = male_count + female_count + other_count
        if total == 0:
            logger.warning("Visualization aborted: Zero students found.")
            messagebox.showinfo("Information", "No student data available for statistics.")
            return
        logger.info(f"Generating statistical chart for {total} students.")
        labels = []
        sizes = []
        colors = []
        explode = []
        
        if male_count > 0:
            labels.append(f'Male ({male_count})')
            sizes.append(male_count)
            colors.append('#2E86C1')
            explode.append(0.05)
        if female_count > 0:
            labels.append(f'Female ({female_count})')
            sizes.append(female_count)
            colors.append('#E74C3C')
            explode.append(0.05)
        if other_count > 0:
            labels.append(f'Other ({other_count})')
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
            shadow=True,
            textprops={'fontsize': 11, 'fontweight': 'bold', 'color': '#333333'}
        )
        for autotext in autotexts:
            autotext.set_color('white')
            
        plt.title('STUDENT GENDER RATIO ANALYSIS', fontsize=14, fontweight='bold', color='#1A5276', pad=20)
        ax.axis('equal')
        fig.canvas.manager.set_window_title('System Statistics')
        plt.tight_layout()
        plt.show()
        logger.info("Statistical window closed.")