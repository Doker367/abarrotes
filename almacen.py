import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from PIL import Image, ImageTk  # Asegúrate de instalar Pillow: pip install pillow

def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',  # Cambia esto
            password='Doker367.',  # Cambia esto
            database='tienda'  # Cambia esto
        )
        if conexion.is_connected():
            return conexion
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

class TiendaAbarrotes:
    def __init__(self, master):
        self.master = master
        self.master.title("Tienda de Abarrotes")
        self.master.geometry("800x600")  # Ajustar el tamaño de la ventana
        self.master.configure(bg="#f0f0f0")
        self.navigation_stack = []  # Pila de navegación para registrar vistas anteriores

        # Barra de navegación
        self.nav_frame = tk.Frame(master, bg="#333")
        self.nav_frame.pack(fill='x')
        self.label = tk.Label(self.nav_frame, text="Tienda de Abarrotes", font=("Arial", 19), bg="#333", fg="white")
        self.label.pack(side=tk.LEFT, padx=10)
        self.boton_ver_productos = tk.Button(self.nav_frame, text="Ver Productos", command=self.mostrar_productos, bg="#444", fg="white")
        self.boton_ver_productos.pack(side=tk.LEFT, padx=5)
        self.boton_ver_categorias = tk.Button(self.nav_frame, text="Ver Categorías", command=self.mostrar_categorias, bg="#444", fg="white")
        self.boton_ver_categorias.pack(side=tk.LEFT, padx=5)
        self.boton_regresar = tk.Button(self.nav_frame, text="Regresar", command=self.regresar, bg="#444", fg="white", state="disabled")
        self.boton_regresar.pack(side=tk.LEFT, padx=5)

        # Frame para mostrar los productos
        self.frame_productos = tk.Frame(master, bg="#f0f0f0")
        self.frame_productos.pack(pady=10, fill='both', expand=True)

    def mostrar_productos(self):
        # Registrar la vista actual en la pila de navegación
        self.navigation_stack.append(self.mostrar_productos)
        self.actualizar_boton_regresar()

        # Limpiar el frame de productos
        for widget in self.frame_productos.winfo_children():
            widget.destroy()

        # Crear un canvas con scrollbar para permitir el scroll
        canvas = tk.Canvas(self.frame_productos, bg="#f0f0f0")
        scrollbar = tk.Scrollbar(self.frame_productos, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Conectar a la base de datos
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            # Obtener las categorías
            cursor.execute("SELECT * FROM categorias")
            categorias = cursor.fetchall()

            for categoria in categorias:
                id_categoria, nombre_categoria = categoria
                # Mostrar el nombre de la categoría
                tk.Label(scrollable_frame, text=nombre_categoria, font=("Arial", 14, "bold"), bg="#f0f0f0").pack(anchor="w", pady=10)

                # Obtener los productos de la categoría
                cursor.execute("SELECT id_producto, nombre, precio, stock FROM productos WHERE id_categoria = %s", (id_categoria,))
                productos = cursor.fetchall()

                for producto in productos:
                    id_producto, nombre, precio, stock = producto
                    # Crear la tarjeta del producto
                    card = tk.Frame(scrollable_frame, borderwidth=1, relief="solid", padx=10, pady=10, bg="white")
                    card.pack(pady=5, fill='x')

                    # Información del producto
                    tk.Label(card, text=f"Nombre: {nombre}", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, sticky="w")
                    tk.Label(card, text=f"Precio: ${precio:.2f}", font=("Arial", 12)).grid(row=1, column=0, columnspan=3, sticky="w")
                    tk.Label(card, text=f"Stock: {stock}", font=("Arial", 12)).grid(row=2, column=0, columnspan=3, sticky="w")

                    # Caja de entrada para cantidad
                    tk.Label(card, text="Cantidad:", font=("Arial", 10)).grid(row=3, column=0, sticky="e")
                    cantidad_entry = tk.Entry(card, width=5)
                    cantidad_entry.insert(0, 0)  # Inicializar en 0
                    cantidad_entry.grid(row=3, column=1, sticky="w")

                    # Botones para agregar y eliminar
                    tk.Button(card, text="▲", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white",
                              command=lambda id_producto=id_producto, cantidad_entry=cantidad_entry: self.agregar_stock(id_producto, cantidad_entry)).grid(row=3, column=2, padx=5)
                    tk.Button(card, text="▼", font=("Arial", 10, "bold"), bg="#F44336", fg="white",
                              command=lambda id_producto=id_producto, cantidad_entry=cantidad_entry: self.eliminar_stock(id_producto, cantidad_entry)).grid(row=3, column=3, padx=5)

            cursor.close()
            conexion.close()
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")

    def mostrar_categorias(self):
        # Registrar la vista actual en la pila de navegación
        self.navigation_stack.append(self.mostrar_categorias)
        self.actualizar_boton_regresar()

        # Limpiar el frame de productos
        for widget in self.frame_productos.winfo_children():
            widget.destroy()

        # Conectar a la base de datos
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_categoria, nombre FROM categorias")  # Seleccionamos ID y nombre
            categorias = cursor.fetchall()

            for categoria in categorias:
                id_categoria, nombre_categoria = categoria

                # Crear un frame para la categoría
                card = tk.Frame(self.frame_productos, borderwidth=1, relief="solid", padx=10, pady=10, bg="white")
                card.pack(pady=5, fill='x')

                # Botón con el nombre de la categoría
                btn_categoria = tk.Button(card, text=nombre_categoria, font=("Arial", 12),
                                           bg="white", relief="flat",
                                           command=lambda id_categoria=id_categoria: self.mostrar_productos_por_categoria(id_categoria))
                btn_categoria.pack(side="left", padx=10)

            cursor.close()
            conexion.close()
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")

    def mostrar_productos_por_categoria(self, id_categoria):
        # Registrar la vista actual en la pila de navegación
        self.navigation_stack.append(lambda: self.mostrar_productos_por_categoria(id_categoria))
        self.actualizar_boton_regresar()

        # Limpiar el frame de productos
        for widget in self.frame_productos.winfo_children():
            widget.destroy()

        # Conectar a la base de datos
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre, precio, stock FROM productos WHERE id_categoria = %s", (id_categoria,))
            productos = cursor.fetchall()

            for producto in productos:
                nombre, precio, stock = producto
                # Crear la tarjeta del producto
                card = tk.Frame(self.frame_productos, borderwidth=1, relief="solid", padx=10, pady=10, bg="white")
                card.pack(pady=5, fill='x')

                # Información del producto
                tk.Label(card, text=f"Nombre: {nombre}", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, sticky="w")
                tk.Label(card, text=f"Precio: ${precio:.2f}", font=("Arial", 12)).grid(row=1, column=0, columnspan=3, sticky="w")
                tk.Label(card, text=f"Stock: {stock}", font=("Arial", 12)).grid(row=2, column=0, columnspan=3, sticky="w")

            cursor.close()
            conexion.close()
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")

    def regresar(self):
        if len(self.navigation_stack) > 1:
            # Eliminar la vista actual de la pila
            self.navigation_stack.pop()
            # Obtener la vista anterior
            vista_anterior = self.navigation_stack[-1]
            # Mostrar la vista anterior
            vista_anterior()
        self.actualizar_boton_regresar()

    def actualizar_boton_regresar(self):
        # Habilitar o deshabilitar el botón de regresar según la pila de navegación
        if len(self.navigation_stack) > 1:
            self.boton_regresar.config(state="normal")
        else:
            self.boton_regresar.config(state="disabled")

    def agregar_producto(self):
        # Ventana para agregar producto
        self.ventana_agregar = tk.Toplevel(self.master)
        self.ventana_agregar.title("Agregar Producto")
        tk.Label(self.ventana_agregar, text="Nombre:").grid(row=0, column=0)
        self.entry_nombre = tk.Entry(self.ventana_agregar)
        self.entry_nombre.grid(row=0, column=1)
        tk.Label(self.ventana_agregar, text="Precio:").grid(row=1, column=0)
        self.entry_precio = tk.Entry(self.ventana_agregar)
        self.entry_precio.grid(row=1, column=1)
        tk.Label(self.ventana_agregar, text="Stock:").grid(row=2, column=0)
        self.entry_stock = tk.Entry(self.ventana_agregar)
        self.entry_stock.grid(row=2, column=1)
        tk.Label(self.ventana_agregar, text="Categoría ID:").grid(row=3, column=0)
        self.entry_categoria_id = tk.Entry(self.ventana_agregar)
        self.entry_categoria_id.grid(row=3, column=1)
        tk.Button(self.ventana_agregar, text="Agregar", command=self.guardar_producto).grid(row=4, columnspan=2)

    def guardar_producto(self):
        nombre = self.entry_nombre.get()
        precio = float(self.entry_precio.get())
        stock = int(self.entry_stock.get())
        categoria_id = int(self.entry_categoria_id.get())
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO productos (nombre, precio, stock, id_categoria) VALUES (%s, %s, %s, %s)",
                           (nombre, precio, stock, categoria_id))
            conexion.commit()
            cursor.close()
            conexion.close()
            messagebox.showinfo("Éxito", "Producto agregado exitosamente.")
            self.ventana_agregar.destroy()
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")

    def eliminar_producto(self):
        # Ventana para eliminar producto
        self.ventana_eliminar = tk.Toplevel(self.master)
        self.ventana_eliminar.title("Eliminar Producto")
        tk.Label(self.ventana_eliminar, text="ID del Producto a Eliminar:").grid(row=0, column=0)
        self.entry_id_producto = tk.Entry(self.ventana_eliminar)
        self.entry_id_producto.grid(row=0, column=1)
        tk.Button(self.ventana_eliminar, text="Eliminar", command=self.confirmar_eliminar).grid(row=1, columnspan=2)

    def confirmar_eliminar(self):
        id_producto = int(self.entry_id_producto.get())
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
            conexion.commit()
            cursor.close()
            conexion.close()
            messagebox.showinfo("Éxito", "Producto eliminado exitosamente.")
            self.ventana_eliminar.destroy()
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")

    def agregar_stock(self, id_producto, cantidad_entry):
        try:
            cantidad = int(cantidad_entry.get())
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0.")
            conexion = conectar_db()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("UPDATE productos SET stock = stock + %s WHERE id_producto = %s", (cantidad, id_producto))
                conexion.commit()
                cursor.close()
                conexion.close()
                messagebox.showinfo("Éxito", "Stock actualizado exitosamente.")
                self.mostrar_productos()  # Refrescar la vista
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        except ValueError as e:
            messagebox.showerror("Error", f"Cantidad inválida: {e}")

    def eliminar_stock(self, id_producto, cantidad_entry):
        try:
            cantidad = int(cantidad_entry.get())
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0.")
            conexion = conectar_db()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("SELECT stock FROM productos WHERE id_producto = %s", (id_producto,))
                stock_actual = cursor.fetchone()[0]
                if stock_actual < cantidad:
                    messagebox.showerror("Error", "No hay suficiente stock para eliminar.")
                    return
                cursor.execute("UPDATE productos SET stock = stock - %s WHERE id_producto = %s", (cantidad, id_producto))
                conexion.commit()
                cursor.close()
                conexion.close()
                messagebox.showinfo("Éxito", "Stock actualizado exitosamente.")
                self.mostrar_productos()  # Refrescar la vista
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        except ValueError as e:
            messagebox.showerror("Error", f"Cantidad inválida: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TiendaAbarrotes(root)
    root.mainloop()