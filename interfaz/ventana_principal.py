import tkinter as tk
from tkinter import ttk
from interfaz.pestana_simulacion import crear_pestana_simulacion
from interfaz.pestana_caracteristicas import crear_pestana_caracteristicas

def crear_ventana():
    root = tk.Tk()
    root.title("Simulador de Cruce Genético 🧬")
    root.geometry("950x700")
    root.config(bg="#18122B")

    style = ttk.Style()
    style.theme_use("clam")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # Crear pestañas y agregarlas al notebook
    tab_simulacion, actualizar_caracteristicas = crear_pestana_simulacion(notebook)
    tab_caracteristicas, label_info = crear_pestana_caracteristicas(notebook)

    notebook.add(tab_simulacion, text="🧬 Simulación")
    notebook.add(tab_caracteristicas, text="📖 Características")

    # Vincular funciones entre pestañas
    actualizar_caracteristicas.set_label(label_info)
    actualizar_caracteristicas.set_notebook(notebook)
    actualizar_caracteristicas.set_tab_caracteristicas(tab_caracteristicas)

    root.mainloop()
