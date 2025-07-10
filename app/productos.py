import tkinter as tk
from tkinter import ttk, messagebox
from app.db import conectar

def ventana_productos():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Productos")
    ventana.geometry("700x500")

    # Treeview
    tree = ttk.Treeview(ventana, columns=("ID", "Nombre", "Categoría", "Precio", "Stock"), show="headings")
    for col in ("ID", "Nombre", "Categoría", "Precio", "Stock"):
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # Cargar productos
    def cargar_productos():
        for fila in tree.get_children():
            tree.delete(fila)
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM productos")
            for producto in cursor.fetchall():
                tree.insert("", "end", values=producto)
            conexion.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar productos\n{e}")

    # Agregar producto
    def agregar_producto():
        def guardar():
            nombre = entry_nombre.get()
            categoria = entry_categoria.get()
            precio = entry_precio.get()
            stock = entry_stock.get()
            if nombre and precio and stock:
                try:
                    conexion = conectar()
                    cursor = conexion.cursor()
                    cursor.execute("INSERT INTO productos (nombre, categoria, precio, stock) VALUES (%s, %s, %s, %s)",
                                   (nombre, categoria, precio, stock))
                    conexion.commit()
                    conexion.close()
                    messagebox.showinfo("Éxito", "Producto agregado correctamente")
                    ventana_agregar.destroy()
                    cargar_productos()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo agregar producto\n{e}")
            else:
                messagebox.showwarning("Advertencia", "Complete todos los campos obligatorios")

        ventana_agregar = tk.Toplevel()
        ventana_agregar.title("Agregar Producto")
        ventana_agregar.geometry("300x250")

        tk.Label(ventana_agregar, text="Nombre:").pack()
        entry_nombre = tk.Entry(ventana_agregar)
        entry_nombre.pack()

        tk.Label(ventana_agregar, text="Categoría:").pack()
        entry_categoria = tk.Entry(ventana_agregar)
        entry_categoria.pack()

        tk.Label(ventana_agregar, text="Precio:").pack()
        entry_precio = tk.Entry(ventana_agregar)
        entry_precio.pack()

        tk.Label(ventana_agregar, text="Stock:").pack()
        entry_stock = tk.Entry(ventana_agregar)
        entry_stock.pack()

        tk.Button(ventana_agregar, text="Guardar", command=guardar).pack(pady=10)

    # Editar producto
    def editar_producto():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return

        item = tree.item(selected[0])
        id_producto, nombre_actual, categoria_actual, precio_actual, stock_actual = item["values"]

        def guardar_edicion():
            nuevo_nombre = entry_nombre.get()
            nueva_categoria = entry_categoria.get()
            nuevo_precio = entry_precio.get()
            nuevo_stock = entry_stock.get()
            try:
                conexion = conectar()
                cursor = conexion.cursor()
                cursor.execute("""
                    UPDATE productos 
                    SET nombre = %s, categoria = %s, precio = %s, stock = %s 
                    WHERE id = %s
                """, (nuevo_nombre, nueva_categoria, nuevo_precio, nuevo_stock, id_producto))
                conexion.commit()
                conexion.close()
                messagebox.showinfo("Éxito", "Producto actualizado")
                ventana_editar.destroy()
                cargar_productos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar\n{e}")

        ventana_editar = tk.Toplevel()
        ventana_editar.title("Editar Producto")
        ventana_editar.geometry("300x250")

        tk.Label(ventana_editar, text="Nombre:").pack()
        entry_nombre = tk.Entry(ventana_editar)
        entry_nombre.insert(0, nombre_actual)
        entry_nombre.pack()

        tk.Label(ventana_editar, text="Categoría:").pack()
        entry_categoria = tk.Entry(ventana_editar)
        entry_categoria.insert(0, categoria_actual)
        entry_categoria.pack()

        tk.Label(ventana_editar, text="Precio:").pack()
        entry_precio = tk.Entry(ventana_editar)
        entry_precio.insert(0, precio_actual)
        entry_precio.pack()

        tk.Label(ventana_editar, text="Stock:").pack()
        entry_stock = tk.Entry(ventana_editar)
        entry_stock.insert(0, stock_actual)
        entry_stock.pack()

        tk.Button(ventana_editar, text="Guardar Cambios", command=guardar_edicion).pack(pady=10)

    # Eliminar producto
    def eliminar_producto():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return

        item = tree.item(selected[0])
        id_producto = item["values"][0]

        confirm = messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este producto?")
        if confirm:
            try:
                conexion = conectar()
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM productos WHERE id = %s", (id_producto,))
                conexion.commit()
                conexion.close()
                messagebox.showinfo("Éxito", "Producto eliminado")
                cargar_productos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar\n{e}")

    # Botones
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Cargar Productos", command=cargar_productos).grid(row=0, column=0, padx=5)
    tk.Button(frame_botones, text="Agregar", command=agregar_producto).grid(row=0, column=1, padx=5)
    tk.Button(frame_botones, text="Editar", command=editar_producto).grid(row=0, column=2, padx=5)
    tk.Button(frame_botones, text="Eliminar", command=eliminar_producto).grid(row=0, column=3, padx=5)

    cargar_productos()
