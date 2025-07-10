import tkinter as tk
from tkinter import messagebox
from app import productos, ventas, reportes

def mostrar_menu():
    root = tk.Tk()
    root.title("MiniMarket Pro - Menú Principal")
    root.geometry("400x300")

    tk.Label(root, text="MiniMarket Pro", font=("Arial", 18, "bold")).pack(pady=20)
    tk.Button(root, text="Gestión de Productos", width=25, command=productos.ventana_productos).pack(pady=10)
    tk.Button(root, text="Registrar Venta", width=25, command=ventas.ventana_ventas).pack(pady=10)
    tk.Button(root, text="Ver Reportes", width=25, command=reportes.ventana_reportes).pack(pady=10)
    tk.Button(root, text="Salir", width=25, command=root.destroy).pack(pady=10)

    root.mainloop()
