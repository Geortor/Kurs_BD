import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from models import *
import pandas as pd
import json
from decimal import Decimal
import datetime


class ExportFrame(ttk.Frame):
    def __init__(self, parent, db, position):
        super().__init__(parent, padding=20)
        self.db = db
        self.position = position
        self.create_ui()

    def create_ui(self):
        ttk.Label(self, text="Экспорт ВСЕХ данных БД", font=("Arial", 16)).pack(pady=10)

        if self.position == "Директор":
            # Кнопки
            button_frame = ttk.Frame(self)
            button_frame.pack(pady=10)

            ttk.Button(button_frame, text="Экспорт в XLSX", command=self.export_all_to_xlsx).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Экспорт в JSON", command=self.export_all_to_json).pack(side=tk.LEFT, padx=5)

    def export_all_to_xlsx(self):
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not filename:
            return

        try:
            all_data = self.get_all_data()
            with pd.ExcelWriter(filename, engine="openpyxl") as writer:
                for table_name, data in all_data.items():
                    df = pd.DataFrame(data)
                    df.to_excel(writer, sheet_name=table_name, index=False)
            messagebox.showinfo("Успех", "Данные из всех таблиц успешно экспортированы в XLSX")
        except Exception as e:
            messagebox.showinfo("Ошибка", f"Ошибка при экспорте: {e}")

    def export_all_to_json(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not filename:
            return
        try:
            all_data = self.get_all_data()
            with open(filename, "w", encoding="utf-8") as outfile:
                json.dump(all_data, outfile, indent=4, ensure_ascii=False)
            messagebox.showinfo("Успех", "Данные из всех таблиц успешно экспортированы в JSON")

        except Exception as e:
            messagebox.showinfo("Ошибка", f"Ошибка при экспорте: {e}")

    def get_all_data(self):
        tables = ['Персональные_данные', 'Сотрудник', 'Клиент', 'Наименование_тура', 'Сделка', 'Договор', 'Оплата']
        all_data = {}
        for table_name in tables:
            try:
                model = globals()[table_name]
                query = model.select()
                data = list(query.dicts())

                # Преобразуем все Decimal в float и date в строки
                for row in data:
                    for key, value in row.items():
                        if isinstance(value, Decimal):
                            row[key] = float(value)
                        if isinstance(value, datetime.date):
                            row[key] = value.strftime('%Y-%m-%d')

                all_data[table_name] = data
            except Exception as e:
                messagebox.showinfo("Ошибка", f"Ошибка при получении данных из {table_name} таблицы {e}")
                return {}
        return all_data