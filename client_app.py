import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Client, Base 
import sys


DB_URL = "mysql+pymysql://root:Sasha.Ryback2007@localhost:3306/trips_db"

class DatabaseManager:
    """Клас для управління підключенням до БД та сесією ORM."""
    def __init__(self, db_url):
        try:
            self.engine = create_engine(db_url)
            self.Session = sessionmaker(bind=self.engine)
            
            self.engine.connect()
        except Exception as e:
            messagebox.showerror("Помилка підключення до БД", f"Не вдалося підключитися: {e}")
            sys.exit(1)

    def get_session(self):
        return self.Session()

class ClientApp:
    """Основний клас графічного інтерфейсу Tkinter."""
    def __init__(self, root, db_manager):
        self.root = root
        self.db_manager = db_manager
        self.root.title("Клієнт для бази даних 'trips_db' (Клієнти)")
        self.root.geometry("800x600")

        self._create_widgets()
        self.load_clients() 

    def _create_widgets(self):
        """Створює всі елементи інтерфейсу: таблицю, форму та кнопки."""
        
        
        frame_table = ttk.Frame(self.root)
        frame_table.pack(pady=10, padx=10, fill="both", expand=True)

        columns = ("id", "first_name", "last_name", "email", "phone")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings")
        
        
        self.tree.heading("id", text="ID", anchor=tk.CENTER)
        self.tree.column("id", width=40, anchor=tk.CENTER)
        self.tree.heading("first_name", text="Ім'я")
        self.tree.heading("last_name", text="Прізвище")
        self.tree.heading("email", text="Email")
        self.tree.heading("phone", text="Телефон")
        self.tree.pack(fill="both", expand=True)

        
        frame_form = ttk.LabelFrame(self.root, text="Додати нового клієнта")
        frame_form.pack(pady=10, padx=10)
        
        self.entries = {}
        fields = ["Ім'я", "Прізвище", "Email", "Телефон"]
        keys = ["first_name", "last_name", "email", "phone"]
        
        for i, (label_text, key) in enumerate(zip(fields, keys)):
            tk.Label(frame_form, text=label_text).grid(row=i, column=0, padx=5, pady=2, sticky="w")
            entry = ttk.Entry(frame_form, width=30)
            entry.grid(row=i, column=1, padx=5, pady=2)
            self.entries[key] = entry
            
       
        frame_buttons = ttk.Frame(self.root)
        frame_buttons.pack(pady=10)
        
        ttk.Button(frame_buttons, text="Оновити список", command=self.load_clients).grid(row=0, column=0, padx=5)
        ttk.Button(frame_buttons, text="Додати клієнта", command=self.add_client).grid(row=0, column=1, padx=5)
        ttk.Button(frame_buttons, text="Видалити клієнта", command=self.delete_client).grid(row=0, column=2, padx=5)

    def load_clients(self):
        """Оновити список клієнтів (операція READ)"""
        session = self.db_manager.get_session()
        try:
            for row in self.tree.get_children():
                self.tree.delete(row)
            
            clients = session.query(Client).all()
            for c in clients:
                self.tree.insert("", "end", values=(c.client_id, c.first_name, c.last_name, c.email, c.phone))
        except Exception as e:
            messagebox.showerror("Помилка ORM", f"Помилка завантаження даних: {e}")
        finally:
            session.close()

    def add_client(self):
        """Додати нового клієнта (операція CREATE)"""
        f = self.entries['first_name'].get()
        l = self.entries['last_name'].get()
        e = self.entries['email'].get()
        p = self.entries['phone'].get()
        
        if not f or not l or not e:
            messagebox.showwarning("Помилка", "Поля Ім'я, Прізвище та Email обов'язкові!")
            return

        session = self.db_manager.get_session()
        new_client = Client(first_name=f, last_name=l, email=e, phone=p)
        session.add(new_client)
        
        try:
            session.commit()
            messagebox.showinfo("✅", "Клієнта додано!")
            self.load_clients()
            
            for entry in self.entries.values():
                entry.delete(0, tk.END)
        except Exception as ex:
            session.rollback()
            
            messagebox.showerror("Помилка", f"Не вдалося додати клієнта. Можливо, Email вже існує: {ex.orig}")
        finally:
            session.close()

    def delete_client(self):
        """Видалити обраного клієнта (операція DELETE)"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Увага", "Оберіть клієнта для видалення!")
            return

        client_id = self.tree.item(selected[0])["values"][0]
        session = self.db_manager.get_session()
        
        try:
            client = session.query(Client).filter_by(client_id=client_id).one_or_none()
            if client:
                session.delete(client)
                session.commit()
                self.load_clients()
                messagebox.showinfo( "Клієнта видалено!")
        except Exception as ex:
            session.rollback()
            
            messagebox.showerror("Помилка видалення", f"Не вдалося видалити: {ex.orig}. Спочатку видаліть пов'язані бронювання.")
        finally:
            session.close()


if __name__ == "__main__":
    db_manager = DatabaseManager(DB_URL)
    root = tk.Tk()
    app = ClientApp(root, db_manager)
    root.mainloop()