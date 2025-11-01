import tkinter as tk
from tkinter import ttk
from interfaz.pestana_simulacion import crear_pestana_simulacion
from interfaz.pestana_caracteristicas import crear_pestana_caracteristicas

def crear_ventana():
    ventana = tk.Tk()
    ventana.title("Simulador Genético de Animales 🧬")
    ventana.geometry("850x600")
    ventana.configure(bg="#DDE6ED")

    titulo = tk.Label(
        ventana,
        text="Simulador de Cruces Genéticos",
        font=("Helvetica", 20, "bold"),
        bg="#DDE6ED",
        fg="#27374D"
    )
    titulo.pack(pady=15)

    frame = tk.Frame(ventana, bg="#DDE6ED")
    frame.pack(pady=10)

    notebook = ttk.Notebook(frame)
    notebook.pack()

    crear_pestana_simulacion(notebook)
    crear_pestana_caracteristicas(notebook)

    ventana.mainloop()
