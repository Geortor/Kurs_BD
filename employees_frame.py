import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models import *


class EmployeesFrame(ttk.Frame):
    def __init__(self, parent, db, position):
        super().__init__(parent, padding=20)
        self.db = db
        self.position = position
        self.create_ui()

    def create_ui(self):
        ttk.Label(self, text="Управление сотрудниками", font=("Arial", 16)).pack(pady=10)

        # Treeview для отображения сотрудников
        columns = ("id", "ФИО", "Должность")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Кнопки
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        if self.position == "Директор":
            ttk.Button(button_frame, text="Добавить", command=self.add_employee).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Удалить", command=self.delete_employee).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Обновить", command=self.update_employee).pack(side=tk.LEFT, padx=5)

        self.update_employees_list()

    def add_employee(self):
        AddEmployeeDialog(self)

    def delete_employee(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Ошибка", "Выберите сотрудника для удаления")
            return

        employee_id = self.tree.item(selected_item, "values")[0]
        try:
            employee = Сотрудник.get(Сотрудник.id == employee_id)
            employee.персональные_данные.delete_instance(recursive=True)
            messagebox.showinfo("Успех", "Сотрудник успешно удален")
        except Exception as e:
            messagebox.showinfo("Ошибка", f"Ошибка при удалении сотрудника: {e}")

        self.update_employees_list()

    def update_employee(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Ошибка", "Выберите сотрудника для редактирования")
            return
        employee_id = self.tree.item(selected_item, "values")[0]
        UpdateEmployeeDialog(self, employee_id)

    def update_employees_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        employees = Сотрудник.select()
        for employee in employees:
            pers_data = employee.персональные_данные
            fio = f"{pers_data.фамилия} {pers_data.имя} {pers_data.отчество or ''}"
            self.tree.insert("", tk.END, values=(employee.id, fio, employee.должность))


class AddEmployeeDialog(simpledialog.Dialog):
    def __init__(self, parent, title="Добавить сотрудника"):
        self.parent = parent
        super().__init__(parent, title=title)

    def body(self, master):
        ttk.Label(master, text="Фамилия:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.fam_entry = ttk.Entry(master)
        self.fam_entry.grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(master, text="Имя:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(master)
        self.name_entry.grid(row=1, column=1, sticky=tk.W, pady=5)

        ttk.Label(master, text="Отчество:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.otch_entry = ttk.Entry(master)
        self.otch_entry.grid(row=2, column=1, sticky=tk.W, pady=5)

        ttk.Label(master, text="Серия паспорта:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.ser_entry = ttk.Entry(master)
        self.ser_entry.grid(row=3, column=1, sticky=tk.W, pady=5)

        ttk.Label(master, text="Номер паспорта:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.num_entry = ttk.Entry(master)
        self.num_entry.grid(row=4, column=1, sticky=tk.W, pady=5)

        ttk.Label(master, text="Населенный пункт:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.city_entry = ttk.Entry(master)
        self.city_entry.grid(row=5, column=1, sticky=tk.W, pady=5)

        ttk.Label(master, text="Улица:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.street_entry = ttk.Entry(master)
        self.street_entry.grid(row=6, column=1, sticky=tk.W, pady=5)

        ttk.Label(master, text="Дом:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.home_entry = ttk.Entry(master)
        self.home_entry.grid(row=7, column=1, sticky=tk.W, pady=5)

        ttk.Label(master, text="Квартира:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.flat_entry = ttk.Entry(master)
        self.flat_entry.grid(row=8, column=1, sticky=tk.W, pady=5)

        ttk.Label(master, text="Должность:").grid(row=9, column=0, sticky=tk.W, pady=5)
        self.position_entry = ttk.Entry(master)
        self.position_entry.grid(row=9, column=1, sticky=tk.W, pady=5)
        return master

    def apply(self):
        try:
            pers_data = Персональные_данные.create(
                фамилия=self.fam_entry.get(),
                имя=self.name_entry.get(),
                отчество=self.otch_entry.get(),
                серия_паспорта=int(self.ser_entry.get()),
                номер_паспорта=int(self.num_entry.get()),
                нас_пункт=self.city_entry.get(),
                улица=self.street_entry.get(),
                дом=self.home_entry.get(),
                квартира=self.flat_entry.get()
            )
            Сотрудник.create(персональные_данные=pers_data, должность=self.position_entry.get())
            messagebox.showinfo("Успех", "Сотрудник успешно добавлен")
        except Exception as e:
            messagebox.showinfo("Ошибка", f"Ошибка при добавлении сотрудника: {e}")
        self.parent.update_employees_list()


class UpdateEmployeeDialog(simpledialog.Dialog):
    def __init__(self, parent, employee_id, title="Обновить сотрудника"):
        self.parent = parent
        self.employee_id = employee_id
        super().__init__(parent, title=title)

    def body(self, master):
        try:
            employee = Сотрудник.get(Сотрудник.id == self.employee_id)
            pers_data = employee.персональные_данные

            ttk.Label(master, text="Фамилия:").grid(row=0, column=0, sticky=tk.W, pady=5)
            self.fam_entry = ttk.Entry(master)
            self.fam_entry.insert(0, pers_data.фамилия)
            self.fam_entry.grid(row=0, column=1, sticky=tk.W, pady=5)

            ttk.Label(master, text="Имя:").grid(row=1, column=0, sticky=tk.W, pady=5)
            self.name_entry = ttk.Entry(master)
            self.name_entry.insert(0, pers_data.имя)
            self.name_entry.grid(row=1, column=1, sticky=tk.W, pady=5)

            ttk.Label(master, text="Отчество:").grid(row=2, column=0, sticky=tk.W, pady=5)
            self.otch_entry = ttk.Entry(master)
            self.otch_entry.insert(0, pers_data.отчество)
            self.otch_entry.grid(row=2, column=1, sticky=tk.W, pady=5)

            ttk.Label(master, text="Серия паспорта:").grid(row=3, column=0, sticky=tk.W, pady=5)
            self.ser_entry = ttk.Entry(master)
            self.ser_entry.insert(0, pers_data.серия_паспорта)
            self.ser_entry.grid(row=3, column=1, sticky=tk.W, pady=5)

            ttk.Label(master, text="Номер паспорта:").grid(row=4, column=0, sticky=tk.W, pady=5)
            self.num_entry = ttk.Entry(master)
            self.num_entry.insert(0, pers_data.номер_паспорта)
            self.num_entry.grid(row=4, column=1, sticky=tk.W, pady=5)

            ttk.Label(master, text="Населенный пункт:").grid(row=5, column=0, sticky=tk.W, pady=5)
            self.city_entry = ttk.Entry(master)
            self.city_entry.insert(0, pers_data.нас_пункт)
            self.city_entry.grid(row=5, column=1, sticky=tk.W, pady=5)

            ttk.Label(master, text="Улица:").grid(row=6, column=0, sticky=tk.W, pady=5)
            self.street_entry = ttk.Entry(master)
            self.street_entry.insert(0, pers_data.улица)
            self.street_entry.grid(row=6, column=1, sticky=tk.W, pady=5)

            ttk.Label(master, text="Дом:").grid(row=7, column=0, sticky=tk.W, pady=5)
            self.home_entry = ttk.Entry(master)
            self.home_entry.insert(0, pers_data.дом)
            self.home_entry.grid(row=7, column=1, sticky=tk.W, pady=5)

            ttk.Label(master, text="Квартира:").grid(row=8, column=0, sticky=tk.W, pady=5)
            self.flat_entry = ttk.Entry(master)
            self.flat_entry.insert(0, pers_data.квартира)
            self.flat_entry.grid(row=8, column=1, sticky=tk.W, pady=5)

            ttk.Label(master, text="Должность:").grid(row=9, column=0, sticky=tk.W, pady=5)
            self.position_entry = ttk.Entry(master)
            self.position_entry.insert(0, employee.должность)
            self.position_entry.grid(row=9, column=1, sticky=tk.W, pady=5)
            return master
        except Exception as e:
            messagebox.showinfo("Ошибка", f"Ошибка при получении сотрудника: {e}")
            self.destroy()

    def apply(self):
        try:
            employee = Сотрудник.get(Сотрудник.id == self.employee_id)
            pers_data = employee.персональные_данные
            pers_data.фамилия = self.fam_entry.get()
            pers_data.имя = self.name_entry.get()
            pers_data.отчество = self.otch_entry.get()
            pers_data.серия_паспорта = int(self.ser_entry.get())
            pers_data.номер_паспорта = int(self.num_entry.get())
            pers_data.нас_пункт = self.city_entry.get()
            pers_data.улица = self.street_entry.get()
            pers_data.дом = self.home_entry.get()
            pers_data.квартира = self.flat_entry.get()
            pers_data.save()
            employee.должность = self.position_entry.get()
            employee.save()
            messagebox.showinfo("Успех", "Сотрудник успешно обновлен")
        except Exception as e:
            messagebox.showinfo("Ошибка", f"Ошибка при обновлении сотрудника: {e}")
        self.parent.update_employees_list()