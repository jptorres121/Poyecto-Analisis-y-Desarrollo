import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from diffusers import StableDiffusionPipeline
import torch
import os
from data.animales import todos
from data.caracteristicas import caracteristicas
import random

class ActualizadorCaracteristicas:
    def __init__(self):
        self.label = None
        self.notebook = None
        self.tab_caracteristicas = None

    def set_label(self, label):
        self.label = label

    def set_notebook(self, notebook):
        self.notebook = notebook

    def set_tab_caracteristicas(self, tab):
        self.tab_caracteristicas = tab

    def actualizar(self, animal1, animal2):
        if not self.label: return
        texto1 = caracteristicas.get(animal1, "Sin información disponible.")
        texto2 = caracteristicas.get(animal2, "Sin información disponible.")
        mezcla = random.choice([
            "combina la fuerza y la inteligencia de ambos animales.",
            "posee habilidades únicas que lo hacen sorprendente.",
            "tiene rasgos equilibrados y adaptativos.",
            "es una mezcla perfecta de instinto y belleza."
        ])
        hibrido = f"El híbrido entre {animal1} y {animal2} {mezcla}"

        texto_final = (
            f"🐾 {animal1}: {texto1}\n\n"
            f"🐾 {animal2}: {texto2}\n\n"
            f"🌟 Híbrido: {hibrido}"
        )

        self.label.config(text=texto_final)
        self.notebook.select(self.tab_caracteristicas)

def crear_pestana_simulacion(notebook):
    tab = tk.Frame(notebook, bg="#18122B")
    actualizador = ActualizadorCaracteristicas()

    # Modelo de difusión
    print("Cargando modelo... (puede tardar unos minutos la primera vez)")
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = pipe.to(device)
    print("Modelo cargado correctamente ✅")

    def generar_imagen():
        animal1 = combo1.get()
        animal2 = combo2.get()
        if not animal1 or not animal2:
            messagebox.showwarning("Faltan datos", "Selecciona los dos animales.")
            return

        prompt = f"Un híbrido de cuerpo entero entre un {animal1} y un {animal2}, estilo digital realista y detallado."
        messagebox.showinfo("Generando", "Creando la imagen...")

        image = pipe(prompt, num_inference_steps=30).images[0]

        os.makedirs("assets", exist_ok=True)
        ruta_img = f"assets/{animal1}_{animal2}_hibrido.png"
        image.save(ruta_img)

        mostrar_imagen(ruta_img)
        actualizador.actualizar(animal1, animal2)

    def mostrar_imagen(path):
        img = Image.open(path)
        img = img.resize((400, 400))
        img_tk = ImageTk.PhotoImage(img)
        label_imagen.config(image=img_tk)
        label_imagen.image = img_tk

    tk.Label(tab, text="Selecciona los animales para el cruce 🧬",
             font=("Arial", 18), bg="#18122B", fg="white").pack(pady=20)

    frame_select = tk.Frame(tab, bg="#18122B")
    frame_select.pack(pady=10)

    combo1 = ttk.Combobox(frame_select, values=todos, width=25, font=("Arial", 12))
    combo1.grid(row=0, column=0, padx=20)
    combo2 = ttk.Combobox(frame_select, values=todos, width=25, font=("Arial", 12))
    combo2.grid(row=0, column=1, padx=20)

    btn = tk.Button(tab, text="🔬 Generar Cruce",
                    font=("Arial", 14), bg="#635985", fg="white",
                    command=generar_imagen)
    btn.pack(pady=30)

    label_imagen = tk.Label(tab, bg="#18122B")
    label_imagen.pack(pady=10)

    return tab, actualizador
