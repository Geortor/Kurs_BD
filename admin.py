import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from clients_frame import ClientsFrame
from employees_frame import EmployeesFrame
from tours_frame import ToursFrame
from deals_frame import DealsFrame
from contracts_frame import ContractsFrame
from export_frame import ExportFrame
from backup_frame import BackupFrame
from models import *
import threading
import datetime
import os

# Роли
AGENT = "Агент"
MANAGER = "Менеджер"
DIRECTOR = "Директор"


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Вход в админ-панель")
        self.root.geometry("300x200")

        # Подключение к БД
        db.connect()
        self.db = db

        self.create_login_form()

    def create_login_form(self):
        ttk.Label(self.root, text="ID сотрудника:").pack(pady=5)
        self.id_entry = ttk.Entry(self.root)
        self.id_entry.pack(pady=5)

        ttk.Label(self.root, text="Должность:").pack(pady=5)
        self.position_entry = ttk.Entry(self.root)
        self.position_entry.pack(pady=5)

        ttk.Button(self.root, text="Войти", command=self.login).pack(pady=10)

    def login(self):
        try:
            employee_id = int(self.id_entry.get())
            position = self.position_entry.get()
            employee = Сотрудник.get((Сотрудник.id == employee_id) & (Сотрудник.должность == position))

            self.root.destroy()
            root = tk.Tk()
            app = AdminApp(root, self.db, position)
            root.mainloop()

        except Exception as e:
            messagebox.showinfo("Ошибка", "Неверные учетные данные")


class AdminApp:
    def __init__(self, root, db, position):
        self.root = root
        self.root.title("Админ-панель туристического агентства")
        self.root.geometry("1200x900")

        self.style = ttk.Style(root)
        self.configure_styles()

        self.db = db
        self.position = position
        self.create_menu()
        self.create_welcome_frame()

    def configure_styles(self):
        # Стиль для меню
        self.style.configure("TMenu", foreground="white", background="#333333", font=("Arial", 10))
        self.style.configure("TMenu.TLabel", foreground="white", background="#333333", font=("Arial", 10))

        # Стиль для кнопок
        self.style.configure("TButton", font=("Arial", 10), padding=5)

        # Стиль для вкладок (если используются)
        self.style.configure("TNotebook.Tab", font=("Arial", 10), padding=[8, 4])

    def create_menu(self):
        menu_bar = tk.Menu(self.root, tearoff=0)
        self.root.config(menu=menu_bar)

        # Главное меню
        main_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Главное", menu=main_menu)
        main_menu.add_command(label="Главная", command=self.show_welcome_frame)
        main_menu.add_separator()
        main_menu.add_command(label="Выйти", command=self.logout)
        main_menu.add_command(label="Выход", command=self.root.destroy)

        # Меню управления
        manage_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Управление", menu=manage_menu)
        manage_menu.add_command(label="Клиенты", command=self.show_clients_frame)
        manage_menu.add_command(label="Сотрудники", command=self.show_employees_frame)

        if self.position == MANAGER or self.position == DIRECTOR:
            manage_menu.add_command(label="Туры", command=self.show_tours_frame)

        manage_menu.add_command(label="Сделки", command=self.show_deals_frame)

        if self.position == DIRECTOR or self.position == MANAGER:
            manage_menu.add_command(label="Договоры", command=self.show_contracts_frame)

        if self.position == DIRECTOR:
            manage_menu.add_command(label="Экспорт", command=self.show_export_frame)
            manage_menu.add_command(label="Резервное копирование", command=self.show_backup_frame)

        # Помощь
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Помощь", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)

    def create_welcome_frame(self):
        self.welcome_frame = ttk.Frame(self.root, padding=20)
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)

        welcome_label = ttk.Label(self.welcome_frame, text="Добро пожаловать в админ-панель!", font=("Arial", 20))
        welcome_label.pack(pady=50)

    def show_welcome_frame(self):
        self.clear_frame()
        self.create_welcome_frame()

    def show_clients_frame(self):
        self.clear_frame()
        self.clients_frame = ClientsFrame(self.root, self.db, self.position)
        self.clients_frame.pack(fill=tk.BOTH, expand=True)

    def show_employees_frame(self):
        self.clear_frame()
        self.employees_frame = EmployeesFrame(self.root, self.db, self.position)
        self.employees_frame.pack(fill=tk.BOTH, expand=True)

    def show_tours_frame(self):
        self.clear_frame()
        self.tours_frame = ToursFrame(self.root, self.db, self.position)
        self.tours_frame.pack(fill=tk.BOTH, expand=True)

    def show_deals_frame(self):
        self.clear_frame()
        self.deals_frame = DealsFrame(self.root, self.db, self.position)
        self.deals_frame.pack(fill=tk.BOTH, expand=True)

    def show_contracts_frame(self):
        self.clear_frame()
        self.contracts_frame = ContractsFrame(self.root, self.db, self.position)
        self.contracts_frame.pack(fill=tk.BOTH, expand=True)

    def show_export_frame(self):
        self.clear_frame()
        self.export_frame = ExportFrame(self.root, self.db, self.position)
        self.export_frame.pack(fill=tk.BOTH, expand=True)

    def show_backup_frame(self):
        self.clear_frame()
        self.backup_frame = BackupFrame(self.root, self.db, self.position)
        self.backup_frame.pack(fill=tk.BOTH, expand=True)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, (ttk.Frame, tk.Frame)):
                widget.destroy()

    def show_about(self):
        messagebox.showinfo("О программе", "Это админ-панель для туристического агентства.")

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        login_app = LoginApp(root)
        root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginApp(root)
    root.mainloop()