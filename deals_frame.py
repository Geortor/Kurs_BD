import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models import *
import datetime


class DealsFrame(ttk.Frame):
    def __init__(self, parent, db, position):
        super().__init__(parent, padding=20)
        self.db = db
        self.position = position
        self.create_ui()

    def create_ui(self):
        ttk.Label(self, text="Управление сделками", font=("Arial", 16)).pack(pady=10)

        # Кнопки для управления сделками
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Открыть сделку", command=self.open_deal).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Закрыть сделку", command=self.close_deal).pack(side=tk.LEFT, padx=5)

        if self.position == "Агент" or self.position == "Менеджер" or self.position == "Директор":
            ttk.Button(button_frame, text="Оформить договор", command=self.create_contract).pack(side=tk.LEFT, padx=5)

        # Treeview для отображения сделок
        columns = ("id", "Клиент", "Сотрудник", "Тур", "Дата", "Статус")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.update_deals_list()

    def open_deal(self):
        OpenDealDialog(self, self.position)

    def close_deal(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Ошибка", "Выберите сделку для закрытия")
            return
        deal_id = self.tree.item(selected_item, "values")[0]

        try:
            deal = Сделка.get(Сделка.id == deal_id)
            if deal.статус == "Закрыта":
                messagebox.showinfo("Ошибка", "Сделка уже закрыта")
                return
            AddPaymentDialog(self, deal_id)
        except Exception as e:
            messagebox.showinfo("Ошибка", f"Ошибка при закрытии сделки: {e}")

    def create_contract(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Ошибка", "Выберите сделку для оформления договора")
            return
        deal_id = self.tree.item(selected_item, "values")[0]

        try:
            deal = Сделка.get(Сделка.id == deal_id)
            if deal.статус != "Закрыта":
                messagebox.showinfo("Ошибка", "Договор можно оформить только после закрытия сделки")
                return
            Договор.create(
                сделка=deal,
                персональные_данные=deal.клиент.персональные_данные,
                наименование_тура=deal.тур,
                дата_составления=datetime.date.today()
            )
            messagebox.showinfo("Успех", "Договор успешно создан")
        except Exception as e:
            messagebox.showinfo("Ошибка", f"Ошибка при создании договора: {e}")

    def update_deals_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        deals = Сделка.select()
        for deal in deals:
            client = deal.клиент.персональные_данные
            employee = deal.сотрудник.персональные_данные
            tour = deal.тур

            client_name = f"{client.фамилия} {client.имя}"
            employee_name = f"{employee.фамилия} {employee.имя}"
            tour_name = f"{tour.направление}"

            self.tree.insert("", tk.END,
                             values=(deal.id, client_name, employee_name, tour_name, deal.дата_заключения, deal.статус))


class AddPaymentDialog(simpledialog.Dialog):
    def __init__(self, parent, deal_id, title="Добавить оплату"):
        self.parent = parent
        self.deal_id = deal_id
        super().__init__(parent, title=title)

    def body(self, master):
        ttk.Label(master, text="Дата оплаты:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(master)
        self.date_entry.insert(0, datetime.date.today())
        self.date_entry.grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(master, text="Сумма оплаты:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.amount_entry = ttk.Entry(master)
        self.amount_entry.grid(row=1, column=1, sticky=tk.W, pady=5)

        ttk.Label(master, text="Способ оплаты:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.method_entry = ttk.Entry(master)
        self.method_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        return master

    def apply(self):
        try:
            date_str = self.date_entry.get()
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            amount = float(self.amount_entry.get())
            method = self.method_entry.get()

            deal = Сделка.get(Сделка.id == self.deal_id)
            Оплата.create(
                сделка=deal,
                дата_оплаты=date_obj,
                сумма_оплаты=amount,
                способ_оплаты=method
            )
            deal.статус = "Закрыта"
            deal.save()
            messagebox.showinfo("Успех", "Оплата добавлена, сделка закрыта")
        except Exception as e:
            messagebox.showinfo("Ошибка", f"Ошибка при добавлении оплаты: {e}")
        self.parent.update_deals_list()


class OpenDealDialog(simpledialog.Dialog):
    def __init__(self, parent, position, title="Открыть сделку"):
        self.parent = parent
        self.position = position
        super().__init__(parent, title=title)

    def body(self, master):
        # Клиент
        ttk.Label(master, text="Клиент:").grid(row=0, column=0, sticky=tk.W, pady=5)
        clients = Клиент.select()
        self.clients_list = []
        for client in clients:
            pers_data = client.персональные_данные
            self.clients_list.append(f"{pers_data.фамилия} {pers_data.имя} (id:{client.id})")

        self.client_var = tk.StringVar(master)
        if self.clients_list and (
                self.position == "Агент" or self.position == "Менеджер" or self.position == "Директор"):
            self.client_var.set(self.clients_list[0])
        self.client_dropdown = ttk.Combobox(master, textvariable=self.client_var, values=self.clients_list)
        self.client_dropdown.grid(row=0, column=1, sticky=tk.W, pady=5)

        # Сотрудник
        ttk.Label(master, text="Сотрудник:").grid(row=1, column=0, sticky=tk.W, pady=5)
        employees = Сотрудник.select()
        self.employees_list = []
        for employee in employees:
            pers_data = employee.персональные_данные
            self.employees_list.append(f"{pers_data.фамилия} {pers_data.имя} (id:{employee.id})")

        self.employee_var = tk.StringVar(master)
        if self.employees_list and (
                self.position == "Агент" or self.position == "Менеджер" or self.position == "Директор"):
            self.employee_var.set(self.employees_list[0])
        self.employee_dropdown = ttk.Combobox(master, textvariable=self.employee_var, values=self.employees_list)
        self.employee_dropdown.grid(row=1, column=1, sticky=tk.W, pady=5)

        # Тур
        ttk.Label(master, text="Тур:").grid(row=2, column=0, sticky=tk.W, pady=5)
        tours = Наименование_тура.select()
        self.tours_list = []
        for tour in tours:
            self.tours_list.append(f"{tour.направление} (id:{tour.id})")

        self.tour_var = tk.StringVar(master)
        if self.tours_list and (
                self.position == "Агент" or self.position == "Менеджер" or self.position == "Директор"):
            self.tour_var.set(self.tours_list[0])
        self.tour_dropdown = ttk.Combobox(master, textvariable=self.tour_var, values=self.tours_list)
        self.tour_dropdown.grid(row=2, column=1, sticky=tk.W, pady=5)
        return master

    def apply(self):
        try:
            client_id = int(self.client_var.get().split("id:")[1].replace(")", ""))
            employee_id = int(self.employee_var.get().split("id:")[1].replace(")", ""))
            tour_id = int(self.tour_var.get().split("id:")[1].replace(")", ""))

            Сделка.create(
                клиент=Клиент.get(Клиент.id == client_id),
                сотрудник=Сотрудник.get(Сотрудник.id == employee_id),
                тур=Наименование_тура.get(Наименование_тура.id == tour_id),
                дата_заключения=datetime.date.today(),
                статус="Создана"
            )
            messagebox.showinfo("Успех", "Сделка успешно создана")
        except Exception as e:
            messagebox.showinfo("Ошибка", f"Ошибка при создании сделки: {e}")
        self.parent.update_deals_list()