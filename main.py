##########################################################
# PYTHON INTERMEDIO - TRABAJO INTEGRADOR FINAL - TECNO3F #
##########################################################

import tkinter as tk # Se importa el módulo 'tkinter' para crear la interfaz gráfica, usando 'tk' como alias
from tkinter import ttk, messagebox # Se importa 'ttk' ('themed tk') para widgets más modernos y 'messagebox' para ventanas de diálogo
import sqlite3 # Se importa 'sqlite3' para manejar la base de datos SQLite
import re # Se importa el módulo 're' para usar expresiones regulares (útil para validar el email)

# Se define la clase principal 'CRUDUsuario' que contendrá toda la funcionalidad de la aplicación
class CRUDUsuario:
    def __init__(self, master):
        self.master = master
        self.master.title("CRUD de Usuario")
        self.master.configure(bg='white')  # Configura el fondo de la ventana en blanco

        # Conecta a la base de datos SQLite
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

        # Crea las tablas necesarias en la base de datos
        self.create_tables()
        # Crea los widgets de la interfaz de usuario
        self.create_widgets()

    def create_tables(self):
        # Crea la tabla1 para almacenar 'nombre y apellido'
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tabla1 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                apellido TEXT
            )
        ''')
        # Crea la tabla2 para almacenar 'edad' y relacionarla con la tabla1
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tabla2 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                edad INTEGER,
                tabla1_id INTEGER,
                FOREIGN KEY (tabla1_id) REFERENCES tabla1 (id)
            )
        ''')
        # Crea la tabla3 para almacenar 'email' y relacionarla con tabla2
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tabla3 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                tabla2_id INTEGER,
                FOREIGN KEY (tabla2_id) REFERENCES tabla2 (id)
            )
        ''')
        # Guarda los cambios en la base de datos
        self.conn.commit()

    def create_widgets(self):
        # Configuración de los colores para los botones
        colors = {
            'azul': '#CCEBFF',
            'naranja': '#F2BE8B',
            'verde': '#DDFFDD',
            'amarillo': '#FFFFCC',
            'rojo': '#F28B8B'
        }

        # Crea y posiciona los botones a la izquierda
        ttk.Button(self.master, text="Cargar Usuario por ID", command=self.load_user, 
                   style='Azul.TButton').grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        ttk.Button(self.master, text="Mostrar Usuarios", command=self.read_records, 
                   style='Naranja.TButton').grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        ttk.Button(self.master, text="Crear Nuevo Usuario", command=self.create_record, 
                   style='Verde.TButton').grid(row=2, column=0, padx=5, pady=5, sticky='ew')
        ttk.Button(self.master, text="Actualizar Usuario", command=self.update_record, 
                   style='Amarillo.TButton').grid(row=3, column=0, padx=5, pady=5, sticky='ew')
        ttk.Button(self.master, text="Eliminar Usuario", command=self.delete_record, 
                   style='Rojo.TButton').grid(row=4, column=0, padx=5, pady=5, sticky='ew')

        # Configura los estilos para los botones
        style = ttk.Style()
        style.configure('Azul.TButton', background=colors['azul'])
        style.configure('Naranja.TButton', background=colors['naranja'])
        style.configure('Verde.TButton', background=colors['verde'])
        style.configure('Amarillo.TButton', background=colors['amarillo'])
        style.configure('Rojo.TButton', background=colors['rojo'])

        # Crea y posiciona las etiquetas y campos de entrada a la derecha
        # Configura las etiquetas con fondo blanco para que parezcan transparentes
        tk.Label(self.master, text="ID:", bg='white').grid(row=0, column=1, padx=5, pady=5, sticky='e')
        self.id_entry = ttk.Entry(self.master)
        self.id_entry.grid(row=0, column=2, padx=5, pady=5)
        # Agrega el texto de ayuda en el campo ID
        self.id_entry.insert(0, "Ingresar el ID del usuario")
        self.id_entry.config(foreground='grey')
        self.id_entry.bind('<FocusIn>', self.on_entry_click)
        self.id_entry.bind('<FocusOut>', self.on_focusout)

        tk.Label(self.master, text="Nombre:", bg='white').grid(row=1, column=1, padx=5, pady=5, sticky='e')
        self.nombre_entry = ttk.Entry(self.master)
        self.nombre_entry.grid(row=1, column=2, padx=5, pady=5)

        tk.Label(self.master, text="Apellido:", bg='white').grid(row=2, column=1, padx=5, pady=5, sticky='e')
        self.apellido_entry = ttk.Entry(self.master)
        self.apellido_entry.grid(row=2, column=2, padx=5, pady=5)

        tk.Label(self.master, text="Edad:", bg='white').grid(row=3, column=1, padx=5, pady=5, sticky='e')
        self.edad_entry = ttk.Entry(self.master)
        self.edad_entry.grid(row=3, column=2, padx=5, pady=5)

        tk.Label(self.master, text="E-mail:", bg='white').grid(row=4, column=1, padx=5, pady=5, sticky='e')
        self.email_entry = ttk.Entry(self.master)
        self.email_entry.grid(row=4, column=2, padx=5, pady=5)

    def on_entry_click(self, event):
        """Función para manejar el clic en el campo ID"""
        if self.id_entry.get() == "Ingresar el ID del usuario":
            self.id_entry.delete(0, tk.END)
            self.id_entry.config(foreground='black')

    def on_focusout(self, event):
        """Función para manejar la pérdida de foco en el campo ID"""
        if self.id_entry.get() == "":
            self.id_entry.insert(0, "Ingresar el ID del usuario")
            self.id_entry.config(foreground='grey')

    def load_user(self):
        """Carga los datos de un usuario basado en el ID proporcionado"""
        id_to_load = self.id_entry.get()
        if id_to_load == "Ingresar el ID del usuario" or not id_to_load:
            messagebox.showerror("Error", "Por favor, ingrese un ID válido para cargar")
            return

        # Busca el usuario en la base de datos
        self.cursor.execute('''
            SELECT t1.id, t1.nombre, t1.apellido, t2.edad, t3.email
            FROM tabla1 t1
            JOIN tabla2 t2 ON t1.id = t2.tabla1_id
            JOIN tabla3 t3 ON t2.id = t3.tabla2_id
            WHERE t1.id = ?
        ''', (id_to_load,))

        user = self.cursor.fetchone()
        if user:
            # Si se encuentra el usuario, llena los campos con sus datos
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, user[0])
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, user[1])
            self.apellido_entry.delete(0, tk.END)
            self.apellido_entry.insert(0, user[2])
            self.edad_entry.delete(0, tk.END)
            self.edad_entry.insert(0, user[3])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, user[4])
            messagebox.showinfo("Éxito", "Usuario cargado")
        else:
            messagebox.showerror("Error", "No se encontró un usuario con ese ID")

    def validate_inputs(self):
        """Valida los datos ingresados por el usuario"""
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        edad = self.edad_entry.get()
        email = self.email_entry.get()

        if not nombre.isalpha() or not apellido.isalpha():
            messagebox.showerror("Error", "El nombre y apellido deben contener solo letras.")
            return False

        if not edad.isdigit() or int(edad) <= 0:
            messagebox.showerror("Error", "La edad debe ser un número entero positivo.")
            return False

        if not re.match(r"[^@]+@[^@]+\.com$", email):
            messagebox.showerror("Error", "El e-mail debe contener '@' y terminar en '.com'")
            return False

        return True

    def create_record(self):
        """Crea un nuevo registro de usuario en la base de datos"""
        if not self.validate_inputs():
            return

        # Inserta los datos en la tabla1
        self.cursor.execute("INSERT INTO tabla1 (nombre, apellido) VALUES (?, ?)",
                            (self.nombre_entry.get(), self.apellido_entry.get()))
        tabla1_id = self.cursor.lastrowid

        # Inserta los datos en la tabla2
        self.cursor.execute("INSERT INTO tabla2 (edad, tabla1_id) VALUES (?, ?)",
                            (int(self.edad_entry.get()), tabla1_id))
        tabla2_id = self.cursor.lastrowid

        # Inserta los datos en la tabla3
        self.cursor.execute("INSERT INTO tabla3 (email, tabla2_id) VALUES (?, ?)",
                            (self.email_entry.get(), tabla2_id))

        # Guarda los cambios en la base de datos
        self.conn.commit()
        messagebox.showinfo("Éxito", "Usuario creado")
        self.clear_entries()

    def read_records(self):
        """Lee y muestra todos los registros de usuarios"""
        # Obtiene todos los registros de la base de datos
        self.cursor.execute('''
            SELECT t1.id, t1.nombre, t1.apellido, t2.edad, t3.email
            FROM tabla1 t1
            JOIN tabla2 t2 ON t1.id = t2.tabla1_id
            JOIN tabla3 t3 ON t2.id = t3.tabla2_id
        ''')
        records = self.cursor.fetchall()
        if records:
            # Si hay registros, los muestra en un mensaje
            message = "\n".join([f"ID: {r[0]}, Nombre: {r[1]}, Apellido: {r[2]}, Edad: {r[3]}, Email: {r[4]}" for r in records])
            messagebox.showinfo("Usuarios", message)
        else:
            messagebox.showinfo("Usuarios", "No hay usuarios para mostrar")

    def update_record(self):
        """Actualiza un registro de usuario existente"""
        if not self.validate_inputs():
            return

        id_to_update = self.id_entry.get()
        if id_to_update == "Ingresar el ID del usuario" or not id_to_update:
            messagebox.showerror("Error", "Por favor, primero cargue un usuario para actualizar")
            return

        # Actualiza los datos en la tabla1
        self.cursor.execute("UPDATE tabla1 SET nombre = ?, apellido = ? WHERE id = ?",
                            (self.nombre_entry.get(), self.apellido_entry.get(), id_to_update))

        # Actualiza los datos en la tabla2
        self.cursor.execute('''
            UPDATE tabla2 SET edad = ?
            WHERE tabla1_id = ?
        ''', (int(self.edad_entry.get()), id_to_update))

        # Actualiza los datos en la tabla3
        self.cursor.execute('''
            UPDATE tabla3 SET email = ?
            WHERE tabla2_id = (SELECT id FROM tabla2 WHERE tabla1_id = ?)
        ''', (self.email_entry.get(), id_to_update))

        # Guarda los cambios en la base de datos
        self.conn.commit()
        messagebox.showinfo("Éxito", "Usuario actualizado")
        self.clear_entries()

    def delete_record(self):
        """Elimina un registro de usuario de la base de datos"""
        id_to_delete = self.id_entry.get()
        if id_to_delete == "Ingresar el ID del usuario" or not id_to_delete:
            messagebox.showerror("Error", "Por favor, primero cargue un usuario para eliminar")
            return

        # Se pide 'confirmación' antes de eliminar al usuario
        confirm = messagebox.askyesno("Confirmar eliminación", 
                                      "¿Está seguro de que desea eliminar este usuario? Esta acción no se puede deshacer.")
        if not confirm:
            return

        # Elimina los datos de la tabla3
        self.cursor.execute('''
            DELETE FROM tabla3 WHERE tabla2_id IN (
                SELECT id FROM tabla2 WHERE tabla1_id = ?
            )
        ''', (id_to_delete,))

        # Elimina los datos de la tabla2
        self.cursor.execute("DELETE FROM tabla2 WHERE tabla1_id = ?", (id_to_delete,))
        # Elimina los datos de la tabla1
        self.cursor.execute("DELETE FROM tabla1 WHERE id = ?", (id_to_delete,))

        # Guarda los cambios en la base de datos
        self.conn.commit()
        messagebox.showinfo("Éxito", "Usuario eliminado")
        self.clear_entries()

    def clear_entries(self):
        """Limpia todos los campos de entrada"""
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, "Ingresar el ID del usuario")
        self.id_entry.config(foreground='grey')
        self.nombre_entry.delete(0, tk.END)
        self.apellido_entry.delete(0, tk.END)
        self.edad_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CRUDUsuario(root)
    root.mainloop()