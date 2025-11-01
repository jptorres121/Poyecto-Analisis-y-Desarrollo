import tkinter as tk
from tkinter import ttk
from data.caracteristicas import rasgos, mutaciones

def crear_pestana_caracteristicas(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Características")

    tk.Label(frame, text="Rasgos Genéticos Disponibles", font=("Helvetica", 12, "bold")).pack(pady=10)
    for r in rasgos:
        tk.Label(frame, text=f"• {r}", font=("Helvetica", 10)).pack(anchor="w", padx=20)

    tk.Label(frame, text="\nMutaciones Posibles", font=("Helvetica", 12, "bold")).pack(pady=10)
    for m in mutaciones:
        tk.Label(frame, text=f"• {m if m else 'Sin mutación'}", font=("Helvetica", 10)).pack(anchor="w", padx=20)

    return frame
