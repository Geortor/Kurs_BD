import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models import *
import json
from decimal import Decimal
import datetime
import threading
import time
import os


class BackupFrame(ttk.Frame):
    def __init__(self, parent, db, position):
        super().__init__(parent, padding=20)
        self.db = db
        self.position = position
        self.backup_folder = None
        self.interval = 3600
        self.interval_unit = "секунды"
        self.create_ui()
        self.backup_timer = None

    def create_ui(self):
        ttk.Label(self, text="Авто резервное копирование", font=("Arial", 16)).pack(pady=10)

        if self.position == "Директор":
            # Папка для резервной копии
            ttk.Button(self, text="Выбрать папку для резервных копий", command=self.choose_backup_folder).pack(pady=10)

            # Выбор периода резервного копирования
            ttk.Label(self, text="Интервал резервного копирования:").pack()

            interval_frame = ttk.Frame(self)
            interval_frame.pack()

            self.interval_entry = ttk.Entry(interval_frame, width=10)
            self.interval_entry.insert(0, 1)
            self.interval_entry.pack(side=tk.LEFT)

            units = ["секунды", "минуты", "часы", "дни"]
            self.interval_unit_var = tk.StringVar(self)
            self.interval_unit_var.set(units[2])
            unit_dropdown = ttk.Combobox(interval_frame, textvariable=self.interval_unit_var, values=units, width=10)
            unit_dropdown.pack(side=tk.LEFT)

            # Кнопки управления резервными копиями
            button_frame = ttk.Frame(self)
            button_frame.pack(pady=10)

            ttk.Button(button_frame, text="Начать резервное копирование", command=self.start_backup).pack(side=tk.LEFT,
                                                                                                          padx=5)
            ttk.Button(button_frame, text="Остановить резервное копирование", command=self.stop_backup).pack(
                side=tk.LEFT, padx=5)

    def choose_backup_folder(self):
        self.backup_folder = filedialog.askdirectory()
        if self.backup_folder:
            messagebox.showinfo("Успех", f"Папка для резервных копий выбрана: {self.backup_folder}")

    def start_backup(self):
        if not self.backup_folder:
            messagebox.showinfo("Ошибка", "Выберите папку для резервных копий")
            return
        try:
            interval_value = int(self.interval_entry.get())
            unit = self.interval_unit_var.get()

            if unit == "секунды":
                self.interval = interval_value
            elif unit == "минуты":
                self.interval = interval_value * 60
            elif unit == "часы":
                self.interval = interval_value * 60 * 60
            elif unit == "дни":
                self.interval = interval_value * 60 * 60 * 24

        except Exception:
            messagebox.showinfo("Ошибка", "Введите корректный интервал")
            return

        self.perform_backup()
        if self.backup_timer:
            self.backup_timer.cancel()
        self.backup_timer = threading.Timer(self.interval, self.start_backup)
        self.backup_timer.start()
        messagebox.showinfo("Успех", f"Резервное копирование начато с интервалом {interval_value} {unit}")

    def stop_backup(self):
        if self.backup_timer:
            self.backup_timer.cancel()
            messagebox.showinfo("Успех", "Резервное копирование остановлено")
        else:
            messagebox.showinfo("Ошибка", "Резервное копирование не запущено")

    def perform_backup(self):
        if not self.backup_folder:
            messagebox.showinfo("Ошибка", "Выберите папку для резервных копий")
            return

        try:
            all_data = self.get_all_data()
            now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = os.path.join(self.backup_folder, f"backup_{now}.json")
            with open(filename, "w", encoding="utf-8") as outfile:
                json.dump(all_data, outfile, indent=4, ensure_ascii=False)
            print(f"Резервная копия успешно создана: {filename}")
        except Exception as e:
            messagebox.showinfo("Ошибка", f"Ошибка при резервном копировании {e}")

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