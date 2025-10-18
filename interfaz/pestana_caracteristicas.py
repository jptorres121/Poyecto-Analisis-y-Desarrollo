import tkinter as tk

def crear_pestana_caracteristicas(notebook):
    tab = tk.Frame(notebook, bg="#18122B")

    tk.Label(tab, text="Características del cruce generado",
             font=("Arial", 18), bg="#18122B", fg="#FFFFFF").pack(pady=20)

    label_info = tk.Label(tab,
                          text="Aquí aparecerán las descripciones del híbrido una vez generado.",
                          font=("Arial", 13), bg="#18122B", fg="white",
                          justify="left", wraplength=800)
    label_info.pack(pady=40)

    return tab, label_info
