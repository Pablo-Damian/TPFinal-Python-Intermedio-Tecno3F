import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class CRUDApp:
    def __init__(self, master):
        self.master = master
        self.master.title("CRUD App")

        # Conectar a la base de datos (la crea si no existe)
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

        # Crear tablas
        self.create_tables()

        # Crear widgets
        self.create_widgets()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tabla1 (
                id INTEGER PRIMARY KEY,
                campo1 TEXT,
                campo2 TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tabla2 (
                id INTEGER PRIMARY KEY,
                campo3 TEXT,
                tabla1_id INTEGER,
                FOREIGN KEY (tabla1_id) REFERENCES tabla1 (id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tabla3 (
                id INTEGER PRIMARY KEY,
                campo4 TEXT,
                campo5 TEXT,
                tabla2_id INTEGER,
                FOREIGN KEY (tabla2_id) REFERENCES tabla2 (id)
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        # Campos de entrada
        ttk.Label(self.master, text="Campo 1:").grid(row=0, column=0, padx=5, pady=5)
        self.campo1 = ttk.Entry(self.master)
        self.campo1.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.master, text="Campo 2:").grid(row=1, column=0, padx=5, pady=5)
        self.campo2 = ttk.Entry(self.master)
        self.campo2.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.master, text="Campo 3:").grid(row=2, column=0, padx=5, pady=5)
        self.campo3 = ttk.Entry(self.master)
        self.campo3.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.master, text="Campo 4:").grid(row=3, column=0, padx=5, pady=5)
        self.campo4 = ttk.Entry(self.master)
        self.campo4.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.master, text="Campo 5:").grid(row=4, column=0, padx=5, pady=5)
        self.campo5 = ttk.Entry(self.master)
        self.campo5.grid(row=4, column=1, padx=5, pady=5)

        # Botones
        ttk.Button(self.master, text="Crear", command=self.create_record).grid(row=5, column=0, padx=5, pady=5)
        ttk.Button(self.master, text="Leer", command=self.read_records).grid(row=5, column=1, padx=5, pady=5)
        ttk.Button(self.master, text="Actualizar", command=self.update_record).grid(row=6, column=0, padx=5, pady=5)
        ttk.Button(self.master, text="Eliminar", command=self.delete_record).grid(row=6, column=1, padx=5, pady=5)

    def create_record(self):
        # Insertar en tabla1
        self.cursor.execute("INSERT INTO tabla1 (campo1, campo2) VALUES (?, ?)",
                            (self.campo1.get(), self.campo2.get()))
        tabla1_id = self.cursor.lastrowid

        # Insertar en tabla2
        self.cursor.execute("INSERT INTO tabla2 (campo3, tabla1_id) VALUES (?, ?)",
                            (self.campo3.get(), tabla1_id))
        tabla2_id = self.cursor.lastrowid

        # Insertar en tabla3
        self.cursor.execute("INSERT INTO tabla3 (campo4, campo5, tabla2_id) VALUES (?, ?, ?)",
                            (self.campo4.get(), self.campo5.get(), tabla2_id))

        self.conn.commit()
        messagebox.showinfo("Éxito", "Registro creado")

    def read_records(self):
        self.cursor.execute('''
            SELECT t1.campo1, t1.campo2, t2.campo3, t3.campo4, t3.campo5
            FROM tabla1 t1
            JOIN tabla2 t2 ON t1.id = t2.tabla1_id
            JOIN tabla3 t3 ON t2.id = t3.tabla2_id
        ''')
        records = self.cursor.fetchall()
        for record in records:
            print(record)
        messagebox.showinfo("Registros", "\n".join(map(str, records)))

    def update_record(self):
        # Actualizar tabla1
        self.cursor.execute("UPDATE tabla1 SET campo1 = ?, campo2 = ? WHERE campo1 = ?",
                            (self.campo1.get(), self.campo2.get(), self.campo1.get()))

        # Actualizar tabla2
        self.cursor.execute('''
            UPDATE tabla2 SET campo3 = ?
            WHERE tabla1_id = (SELECT id FROM tabla1 WHERE campo1 = ?)
        ''', (self.campo3.get(), self.campo1.get()))

        # Actualizar tabla3
        self.cursor.execute('''
            UPDATE tabla3 SET campo4 = ?, campo5 = ?
            WHERE tabla2_id = (
                SELECT t2.id FROM tabla2 t2
                JOIN tabla1 t1 ON t1.id = t2.tabla1_id
                WHERE t1.campo1 = ?
            )
        ''', (self.campo4.get(), self.campo5.get(), self.campo1.get()))

        self.conn.commit()
        messagebox.showinfo("Éxito", "Registro actualizado")

    def delete_record(self):
        # Eliminar de tabla3
        self.cursor.execute('''
            DELETE FROM tabla3 WHERE tabla2_id IN (
                SELECT t2.id FROM tabla2 t2
                JOIN tabla1 t1 ON t1.id = t2.tabla1_id
                WHERE t1.campo1 = ?
            )
        ''', (self.campo1.get(),))

        # Eliminar de tabla2
        self.cursor.execute('''
            DELETE FROM tabla2 WHERE tabla1_id = (
                SELECT id FROM tabla1 WHERE campo1 = ?
            )
        ''', (self.campo1.get(),))

        # Eliminar de tabla1
        self.cursor.execute("DELETE FROM tabla1 WHERE campo1 = ?", (self.campo1.get(),))

        self.conn.commit()
        messagebox.showinfo("Éxito", "Registro eliminado")

if __name__ == "__main__":
    root = tk.Tk()
    app = CRUDApp(root)
    root.mainloop()