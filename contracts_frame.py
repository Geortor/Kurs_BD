import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch


class ContractsFrame(ttk.Frame):
    def __init__(self, parent, db, position):
        super().__init__(parent, padding=20)
        self.db = db
        self.position = position
        self.create_ui()

    def create_ui(self):
        ttk.Label(self, text="Управление договорами", font=("Arial", 16)).pack(pady=10)

        # Treeview для отображения договоров
        columns = ("id", "Клиент", "Тур", "Дата составления", "Сумма")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Кнопка для скачивания PDF
        if self.position == "Директор" or self.position == "Менеджер":
            ttk.Button(self, text="Скачать PDF", command=self.generate_pdf).pack(pady=10)

        self.update_contracts_list()

    def update_contracts_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        contracts = Договор.select()
        for contract in contracts:
            client = contract.персональные_данные
            tour = contract.наименование_тура
            client_name = f"{client.фамилия} {client.имя}"
            tour_name = f"{tour.направление}"

            deal = contract.сделка
            total_amount = 0
            if deal:
                payments = deal.оплаты
                for payment in payments:
                    total_amount += payment.сумма_оплаты

            self.tree.insert("", tk.END, values=(
            contract.id, client_name, tour_name, contract.дата_составления, f"{total_amount:.2f}"))

    def generate_pdf(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Ошибка", "Выберите договор для скачивания PDF")
            return
        contract_id = self.tree.item(selected_item, "values")[0]

        try:
            contract = Договор.get(Договор.id == contract_id)
            self.create_contract_pdf(contract)
        except Exception as e:
            messagebox.showinfo("Ошибка", f"Ошибка при генерации PDF: {e}")

    def create_contract_pdf(self, contract):

        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not filename:
            return

        c = canvas.Canvas(filename, pagesize=letter)

        # Заголовок
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(4.135 * inch, 10 * inch, "CONTRACT")
        c.line(0.5 * inch, 9.8 * inch, 7.7 * inch, 9.8 * inch)

        # Данные о договоре
        c.setFont("Helvetica", 12)
        c.drawString(0.75 * inch, 9.3 * inch, f"Number contract: {contract.id}")
        c.drawString(0.75 * inch, 9 * inch, f"Date: {contract.дата_составления}")

        c.drawString(0.75 * inch, 8.5 * inch, "Information about client:")
        client = contract.персональные_данные
        c.drawString(0.75 * inch, 8.2 * inch, f"FIO: {client.фамилия} {client.имя} {client.отчество or ''}")
        c.drawString(0.75 * inch, 7.9 * inch, f"Pasport: {client.серия_паспорта} {client.номер_паспорта}")
        c.drawString(0.75 * inch, 7.6 * inch,
                     f"Адрес: {client.нас_пункт}, {client.улица}, {client.дом} {client.квартира or ''}")

        c.drawString(0.75 * inch, 7.1 * inch, "Information about toure:")
        tour = contract.наименование_тура
        c.drawString(0.75 * inch, 6.8 * inch, f"Where: {tour.направление}")
        c.drawString(0.75 * inch, 6.5 * inch, f"Price: {tour.цена}")
        c.drawString(0.75 * inch, 6.2 * inch, f"Days: {tour.кол_во_дней}")

        deal = contract.сделка
        total_amount = 0
        if deal:
            payments = deal.оплаты
            for payment in payments:
                total_amount += payment.сумма_оплаты
        c.drawString(0.75 * inch, 5.9 * inch, f"Total sum: {total_amount:.2f}")

        c.save()
        messagebox.showinfo("Успех", "PDF успешно сгенерирован!")