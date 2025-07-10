from tkinter import simpledialog
import tkinter as tk
from tkinter import ttk, messagebox
from app.db import conectar
from datetime import datetime

def ventana_ventas():
    ventana = tk.Toplevel()
    ventana.title("Registrar Venta")
    ventana.geometry("800x600")

    carrito = []
    total_venta = tk.DoubleVar(value=0.00)

    # Treeview Productos
    tree_productos = ttk.Treeview(ventana, columns=("ID", "Nombre", "Precio", "Stock"), show="headings")
    for col in ("ID", "Nombre", "Precio", "Stock"):
        tree_productos.heading(col, text=col)
        tree_productos.column(col, width=150)
    tree_productos.pack(pady=10, fill="x")

    # Cargar productos
    def cargar_productos():
        for fila in tree_productos.get_children():
            tree_productos.delete(fila)
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, precio, stock FROM productos WHERE stock > 0")
            for producto in cursor.fetchall():
                tree_productos.insert("", "end", values=producto)
            conexion.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar productos\n{e}")

    cargar_productos()

    # Carrito
    tree_carrito = ttk.Treeview(ventana, columns=("ID", "Nombre", "Cantidad", "Subtotal"), show="headings")
    for col in ("ID", "Nombre", "Cantidad", "Subtotal"):
        tree_carrito.heading(col, text=col)
        tree_carrito.column(col, width=150)
    tree_carrito.pack(pady=10, fill="x")

    # Agregar al carrito
    # Agregar al carrito
    def agregar_al_carrito():
        selected = tree_productos.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return

        item = tree_productos.item(selected[0])
        id_producto, nombre, precio, stock = item["values"]

        try:
            precio = float(precio)  # Asegurarse que es número
            stock = int(stock)      # Por si acaso también
        except ValueError:
            messagebox.showerror("Error", "Datos inválidos del producto.")
            return

        cantidad = simpledialog.askinteger("Cantidad", f"Ingrese cantidad para '{nombre}' (Disponible: {stock}):", minvalue=1, maxvalue=stock)
        if cantidad is None:
            return

        subtotal = round(precio * cantidad, 2)
        carrito.append({"id": id_producto, "nombre": nombre, "cantidad": cantidad, "subtotal": subtotal})
        tree_carrito.insert("", "end", values=(id_producto, nombre, cantidad, subtotal))

        total_actual = total_venta.get() + subtotal
        total_venta.set(round(total_actual, 2))
        lbl_total.config(text=f"Total: S/. {total_venta.get():.2f}")

    # Registrar Venta
    def registrar_venta():
        if not carrito:
            messagebox.showwarning("Advertencia", "El carrito está vacío")
            return
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            # Insertar Venta
            cursor.execute("INSERT INTO ventas (fecha, total) VALUES (%s, %s)", (datetime.now(), total_venta.get()))
            id_venta = cursor.lastrowid

            # Insertar Detalles + Actualizar stock
            for item in carrito:
                cursor.execute("""
                    INSERT INTO detalle_venta (id_venta, id_producto, cantidad, subtotal) 
                    VALUES (%s, %s, %s, %s)
                """, (id_venta, item["id"], item["cantidad"], item["subtotal"]))

                cursor.execute("""
                    UPDATE productos SET stock = stock - %s WHERE id = %s
                """, (item["cantidad"], item["id"]))

            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", f"Venta registrada correctamente\nTotal: S/. {total_venta.get():.2f}")
            carrito.clear()
            tree_carrito.delete(*tree_carrito.get_children())
            total_venta.set(0.00)
            lbl_total.config(text=f"Total: S/. 0.00")
            cargar_productos()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar venta\n{e}")

    # Botones
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Agregar al Carrito", command=agregar_al_carrito).grid(row=0, column=0, padx=5)
    tk.Button(frame_botones, text="Registrar Venta", command=registrar_venta).grid(row=0, column=1, padx=5)

    lbl_total = tk.Label(ventana, text="Total: S/. 0.00", font=("Arial", 16, "bold"))
    lbl_total.pack(pady=10)

