import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from PIL import Image, ImageTk  # Asegúrate de instalar Pillow: pip install pillow
from modules.db_connection import conectar_db

class TiendaAbarrotes:
    def __init__(self, master):
        self.master = master
        self.master.title("Tienda de Abarrotes")
        self.master.attributes('-zoomed', True)  # Pantalla completa en Linux
        self.master.configure(bg="#f0f0f0")

        # Crear un contenedor principal con diseño de cuadrícula
        self.main_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.main_frame.pack(fill="both", expand=True)

        # Crear un diseño de cuadrícula para las secciones
        self.nav_frame = tk.Frame(self.main_frame, bg="#333")
        self.nav_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.content_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.content_frame.grid(row=1, column=0, sticky="nsew")

        self.sidebar_frame = tk.Frame(self.main_frame, bg="#444")
        self.sidebar_frame.grid(row=1, column=1, sticky="nsew")

        # Configurar pesos para que las secciones se expandan
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=3)
        self.main_frame.grid_columnconfigure(1, weight=1)

        # Barra de navegación
        self.label = tk.Label(self.nav_frame, text="Tienda de Abarrotes", font=("Arial", 19), bg="#333", fg="white")
        self.label.pack(side=tk.LEFT, padx=10)

        self.boton_ver_productos = tk.Button(self.nav_frame, text="Ver Productos", command=self.mostrar_productos, bg="#444", fg="white", font=("Arial", 12))
        self.boton_ver_productos.pack(side=tk.LEFT, padx=5)

        self.boton_ver_categorias = tk.Button(self.nav_frame, text="Ver Categorías", command=self.mostrar_categorias, bg="#444", fg="white", font=("Arial", 12))
        self.boton_ver_categorias.pack(side=tk.LEFT, padx=5)

        # Sidebar con botones de acciones
        tk.Label(self.sidebar_frame, text="Acciones", font=("Arial", 14), bg="#444", fg="white").pack(pady=10)
        tk.Button(self.sidebar_frame, text="Agregar Producto", command=self.agregar_producto, bg="#4CAF50", fg="white", font=("Arial", 12), width=20).pack(pady=5)
        tk.Button(self.sidebar_frame, text="Eliminar Producto", command=self.eliminar_producto, bg="#F44336", fg="white", font=("Arial", 12), width=20).pack(pady=5)
        tk.Button(self.sidebar_frame, text="Agregar Categoría", command=self.agregar_categoria, bg="#2196F3", fg="white", font=("Arial", 12), width=20).pack(pady=5)

        # Contenido principal
        self.content_canvas = tk.Canvas(self.content_frame, bg="#f0f0f0")
        self.scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=self.content_canvas.yview)
        self.scrollable_content = tk.Frame(self.content_canvas, bg="#f0f0f0")

        self.scrollable_content.bind(
            "<Configure>",
            lambda e: self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all"))
        )

        self.content_canvas.create_window((0, 0), window=self.scrollable_content, anchor="nw")
        self.content_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.content_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def mostrar_productos(self):
        # Limpiar contenido
        for widget in self.scrollable_content.winfo_children():
            widget.destroy()

        # Conectar a la base de datos y obtener productos
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT p.id_producto, p.nombre, p.precio, p.stock, c.nombre FROM productos p JOIN categorias c ON p.id_categoria = c.id_categoria")
            productos = cursor.fetchall()

            columnas = 3  # Número de columnas para la cuadrícula
            for index, producto in enumerate(productos):
                id_producto, nombre, precio, stock, categoria = producto

                # Crear la tarjeta del producto
                card = tk.Frame(self.scrollable_content, borderwidth=1, relief="solid", padx=10, pady=10, bg="white")
                card.grid(row=index // columnas, column=index % columnas, padx=10, pady=10, sticky="nsew")

                # Información del producto
                tk.Label(card, text=f"ID: {id_producto}", font=("Arial", 10, "italic"), bg="white").pack(anchor="center", pady=2)
                tk.Label(card, text=nombre, font=("Arial", 12, "bold"), bg="white").pack(anchor="center", pady=5)
                tk.Label(card, text=f"Precio: ${precio:.2f}", font=("Arial", 10), bg="white").pack(anchor="center")
                tk.Label(card, text=f"Stock: {stock}", font=("Arial", 10), bg="white").pack(anchor="center")
                tk.Label(card, text=f"Categoría: {categoria}", font=("Arial", 10, "italic"), bg="white").pack(anchor="center")

                # Botones para editar y eliminar
                botones_frame = tk.Frame(card, bg="white")
                botones_frame.pack(anchor="center", pady=5)
                tk.Button(botones_frame, text="Editar", bg="#FFC107", fg="white", font=("Arial", 10)).pack(side="left", padx=5)
                tk.Button(botones_frame, text="Eliminar", bg="#F44336", fg="white", font=("Arial", 10)).pack(side="right", padx=5)

            cursor.close()
            conexion.close()
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")

    def mostrar_categorias(self):
        # Limpiar contenido
        for widget in self.scrollable_content.winfo_children():
            widget.destroy()

        # Conectar a la base de datos y obtener categorías
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_categoria, nombre FROM categorias")
            categorias = cursor.fetchall()

            columnas = 3  # Número de columnas para la cuadrícula
            for index, categoria in enumerate(categorias):
                id_categoria, nombre_categoria = categoria

                # Crear una tarjeta para cada categoría
                card = tk.Frame(self.scrollable_content, borderwidth=1, relief="solid", padx=10, pady=10, bg="white")
                card.grid(row=index // columnas, column=index % columnas, padx=10, pady=10, sticky="nsew")

                tk.Label(card, text=nombre_categoria, font=("Arial", 12, "bold"), bg="white").pack(anchor="center", pady=5)
                tk.Button(card, text="Ver Productos", bg="#4CAF50", fg="white", font=("Arial", 10),
                          command=lambda id_categoria=id_categoria: self.mostrar_productos_por_categoria(id_categoria)).pack(anchor="center", pady=5)

            cursor.close()
            conexion.close()
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")

    def mostrar_productos_por_categoria(self, id_categoria):
        # Limpiar contenido
        for widget in self.scrollable_content.winfo_children():
            widget.destroy()

        # Conectar a la base de datos y obtener productos de la categoría
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre, precio, stock FROM productos WHERE id_categoria = %s", (id_categoria,))
            productos = cursor.fetchall()

            columnas = 3  # Número de columnas para la cuadrícula
            for index, producto in enumerate(productos):
                nombre, precio, stock = producto

                # Crear la tarjeta del producto
                card = tk.Frame(self.scrollable_content, borderwidth=1, relief="solid", padx=10, pady=10, bg="white")
                card.grid(row=index // columnas, column=index % columnas, padx=10, pady=10, sticky="nsew")

                tk.Label(card, text=nombre, font=("Arial", 12, "bold"), bg="white").pack(anchor="center", pady=5)
                tk.Label(card, text=f"Precio: ${precio:.2f}", font=("Arial", 10), bg="white").pack(anchor="center")
                tk.Label(card, text=f"Stock: {stock}", font=("Arial", 10), bg="white").pack(anchor="center")

            cursor.close()
            conexion.close()
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")

    def agregar_producto(self):
        # Ventana para agregar producto
        ventana = tk.Toplevel(self.master)
        ventana.title("Agregar Producto")
        ventana.geometry("400x300")
        ventana.configure(bg="#f0f0f0")

        tk.Label(ventana, text="Nombre:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, pady=10, padx=10, sticky="w")
        self.entry_nombre = tk.Entry(ventana, font=("Arial", 12), width=25)
        self.entry_nombre.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(ventana, text="Precio:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, pady=10, padx=10, sticky="w")
        self.entry_precio = tk.Entry(ventana, font=("Arial", 12), width=25)
        self.entry_precio.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(ventana, text="Stock:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, pady=10, padx=10, sticky="w")
        self.entry_stock = tk.Entry(ventana, font=("Arial", 12), width=25)
        self.entry_stock.grid(row=2, column=1, pady=10, padx=10)

        tk.Label(ventana, text="Categoría:", font=("Arial", 12), bg="#f0f0f0").grid(row=3, column=0, pady=10, padx=10, sticky="w")

        # Obtener categorías de la base de datos
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_categoria, nombre FROM categorias")
            self.categorias = cursor.fetchall()
            cursor.close()
            conexion.close()

        # Crear un menú desplegable para seleccionar la categoría
        self.categoria_seleccionada = tk.StringVar(ventana)
        self.categoria_seleccionada.set(self.categorias[0][1])  # Seleccionar la primera categoría por defecto
        opciones_categorias = [categoria[1] for categoria in self.categorias]
        tk.OptionMenu(ventana, self.categoria_seleccionada, *opciones_categorias).grid(row=3, column=1, pady=10, padx=10)

        tk.Button(ventana, text="Guardar", bg="#4CAF50", fg="white", font=("Arial", 12), command=self.guardar_producto).grid(row=4, column=0, columnspan=2, pady=20)

    def agregar_categoria(self):
        # Ventana para agregar categoría
        ventana = tk.Toplevel(self.master)
        ventana.title("Agregar Categoría")
        ventana.geometry("300x200")
        ventana.configure(bg="#f0f0f0")

        tk.Label(ventana, text="Nombre de la Categoría:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, pady=10, padx=10, sticky="w")
        self.entry_nombre_categoria = tk.Entry(ventana, font=("Arial", 12), width=25)
        self.entry_nombre_categoria.grid(row=0, column=1, pady=10, padx=10)

        tk.Button(ventana, text="Guardar", bg="#4CAF50", fg="white", font=("Arial", 12), command=self.guardar_categoria).grid(row=1, column=0, columnspan=2, pady=20)

    def guardar_producto(self):
        nombre = self.entry_nombre.get()
        precio = float(self.entry_precio.get())
        stock = int(self.entry_stock.get())

        # Obtener el ID de la categoría seleccionada
        categoria_nombre = self.categoria_seleccionada.get()
        categoria_id = next(categoria[0] for categoria in self.categorias if categoria[1] == categoria_nombre)

        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO productos (nombre, precio, stock, id_categoria) VALUES (%s, %s, %s, %s)",
                           (nombre, precio, stock, categoria_id))
            conexion.commit()
            cursor.close()
            conexion.close()
            messagebox.showinfo("Éxito", "Producto agregado exitosamente.")
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")

    def guardar_categoria(self):
        nombre_categoria = self.entry_nombre_categoria.get()
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO categorias (nombre) VALUES (%s)", (nombre_categoria,))
            conexion.commit()
            cursor.close()
            conexion.close()
            messagebox.showinfo("Éxito", "Categoría agregada exitosamente.")
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")

    def eliminar_producto(self):
        # Ventana para eliminar producto
        ventana = tk.Toplevel(self.master)
        ventana.title("Eliminar Producto")
        ventana.geometry("400x200")
        ventana.configure(bg="#f0f0f0")

        tk.Label(ventana, text="Selecciona el Producto a Eliminar:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, pady=10, padx=10, sticky="w")

        # Obtener productos de la base de datos
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_producto, nombre FROM productos")
            productos = cursor.fetchall()
            cursor.close()
            conexion.close()

            # Crear un menú desplegable para seleccionar el producto
            self.producto_seleccionado = tk.StringVar(ventana)
            self.producto_seleccionado.set(productos[0][1])  # Seleccionar el primer producto por defecto
            opciones_productos = [f"{producto[1]} (ID: {producto[0]})" for producto in productos]
            tk.OptionMenu(ventana, self.producto_seleccionado, *opciones_productos).grid(row=0, column=1, pady=10, padx=10)

            tk.Button(ventana, text="Eliminar", bg="#F44336", fg="white", font=("Arial", 12),
                      command=lambda: self.confirmar_eliminar(ventana, productos)).grid(row=1, column=0, columnspan=2, pady=20)
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")

    def confirmar_eliminar(self, ventana, productos):
        # Obtener el ID del producto seleccionado
        producto_nombre = self.producto_seleccionado.get()
        try:
            producto_id = next(producto[0] for producto in productos if f"{producto[1]} (ID: {producto[0]})" == producto_nombre)
        except StopIteration:
            messagebox.showerror("Error", "No se pudo encontrar el producto seleccionado.")
            return

        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            try:
                # Eliminar registros relacionados en la tabla ventas
                cursor.execute("DELETE FROM ventas WHERE id_producto = %s", (producto_id,))
                # Eliminar el producto
                cursor.execute("DELETE FROM productos WHERE id_producto = %s", (producto_id,))
                conexion.commit()
                messagebox.showinfo("Éxito", "Producto eliminado exitosamente.")
                ventana.destroy()
                self.mostrar_productos()  # Refrescar la vista de productos
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")
            finally:
                cursor.close()
                conexion.close()
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