import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models import *


class ClientsFrame(ttk.Frame):
    def __init__(self, parent, db, position):
        super().__init__(parent, padding=20)
        self.db = db
        self.position = position
        self.create_ui()

    def create_ui(self):
        ttk.Label(self, text="Управление клиентами", font=("Arial", 16)).pack(pady=10)

        # Treeview для отображения клиентов
        columns = ("id", "ФИО", "Паспорт", "Адрес")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Кнопки
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Добавить", command=self.add_client).pack(side=tk.LEFT, padx=5)

        if self.position == "Директор" or self.position == "Менеджер" or self.position == "Агент":
            ttk.Button(button_frame, text="Обновить", command=self.update_client).pack(side=tk.LEFT, padx=5)

        if self.position == "Директор" or self.position == "Менеджер":
            ttk.Button(button_frame, text="Удалить", command=self.delete_client).pack(side=tk.LEFT, padx=5)

        self.update_client_list()

    def add_client(self):
        AddClientDialog(self)

    def delete_client(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Ошибка", "Выберите клиента для удаления")
            return

        client_id = self.tree.item(selected_item, "values")[0]
        try:
            client = Клиент.get(Клиент.id == client_id)
            client.персональные_данные.delete_instance(recursive=True)
            messagebox.showinfo("Успех", "Клиент успешно удален")
        except Exception as e:
            messagebox.showinfo("Ошибка", f"Ошибка при удалении клиента: {e}")

        self.update_client_list()

    def update_client(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Ошибка", "Выберите клиента для редактирования")
            return
        client_id = self.tree.item(selected_item, "values")[0]
        UpdateClientDialog(self, client_id)

    def update_client_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        clients = Клиент.select()
        for client in clients:
            pers_data = client.персональные_данные
            fio = f"{pers_data.фамилия} {pers_data.имя} {pers_data.отчество or ''}"
            passport = f"{pers_data.серия_паспорта} {pers_data.номер_паспорта}"
            address = f"{pers_data.нас_пункт} {pers_data.улица} {pers_data.дом} {pers_data.квартира or ''}"
            self.tree.insert("", tk.END, values=(client.id, fio, passport, address))


class AddClientDialog(simpledialog.Dialog):
    def __init__(self, parent, title="Добавить клиента"):
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
            Клиент.create(персональные_данные=pers_data)
            messagebox.showinfo("Успех", "Клиент успешно добавлен")
        except Exception as e:
            messagebox.showinfo("Ошибка", f"Ошибка при добавлении клиента: {e}")
        self.parent.update_client_list()


class UpdateClientDialog(simpledialog.Dialog):
    def __init__(self, parent, client_id, title="Обновить клиента"):
        self.parent = parent
        self.client_id = client_id
        super().__init__(parent, title=title)

    def body(self, master):
        try:
            client = Клиент.get(Клиент.id == self.client_id)
            pers_data = client.персональные_данные

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
        except Exception as e:
            messagebox.showinfo("Ошибка", f"Ошибка при получении клиента: {e}")
            self.destroy()
        return master

    def apply(self):
        try:
            client = Клиент.get(Клиент.id == self.client_id)
            pers_data = client.персональные_данные
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
            messagebox.showinfo("Успех", "Клиент успешно обновлен")
        except Exception as e:
            messagebox.showinfo("Ошибка", f"Ошибка при обновлении клиента: {e}")
        self.parent.update_client_list()