import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models import *

class ToursFrame(ttk.Frame):
    def __init__(self, parent, db, position):
        super().__init__(parent, padding=20)
        self.db = db
        self.position = position
        self.create_ui()

    def create_ui(self):
        ttk.Label(self, text="Управление турами", font=("Arial", 16)).pack(pady=10)

        # Treeview для отображения туров
        columns = ("id", "Направление", "Цена", "Кол-во дней")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Кнопки
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        if self.position == "Менеджер" or self.position == "Директор":
            ttk.Button(button_frame, text="Добавить", command=self.add_tour).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Удалить", command=self.delete_tour).pack(side=tk.LEFT, padx=5)

        self.update_tour_list()

    def add_tour(self):
       AddTourDialog(self)

    def delete_tour(self):
        selected_item = self.tree.selection()
        if not selected_item:
             messagebox.showinfo("Ошибка", "Выберите тур для удаления")
             return
        tour_id = self.tree.item(selected_item, "values")[0]

        try:
            tour = Наименование_тура.get(Наименование_тура.id == tour_id)
            tour.delete_instance()
            messagebox.showinfo("Успех", "Тур успешно удален")
        except Exception as e:
             messagebox.showinfo("Ошибка", f"Ошибка при удалении тура: {e}")
        self.update_tour_list()

    def update_tour_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        tours = Наименование_тура.select()
        for tour in tours:
            self.tree.insert("", tk.END, values=(tour.id, tour.направление, tour.цена, tour.кол_во_дней))

class AddTourDialog(simpledialog.Dialog):
    def __init__(self, parent, title="Добавить тур"):
        self.parent = parent
        super().__init__(parent, title=title)

    def body(self, master):
       ttk.Label(master, text="Направление:").grid(row=0, column=0, sticky=tk.W, pady=5)
       self.direction_entry = ttk.Entry(master)
       self.direction_entry.grid(row=0, column=1, sticky=tk.W, pady=5)

       ttk.Label(master, text="Цена:").grid(row=1, column=0, sticky=tk.W, pady=5)
       self.price_entry = ttk.Entry(master)
       self.price_entry.grid(row=1, column=1, sticky=tk.W, pady=5)

       ttk.Label(master, text="Количество дней:").grid(row=2, column=0, sticky=tk.W, pady=5)
       self.days_entry = ttk.Entry(master)
       self.days_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
       return master

    def apply(self):
        try:
            Наименование_тура.create(
                направление=self.direction_entry.get(),
                цена=float(self.price_entry.get()),
                кол_во_дней=int(self.days_entry.get())
            )
            messagebox.showinfo("Успех", "Тур успешно добавлен")
        except Exception as e:
            messagebox.showinfo("Ошибка", f"Ошибка при добавлении тура: {e}")
        self.parent.update_tour_list()