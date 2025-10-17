import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from diffusers import StableDiffusionPipeline
import torch
import os
import random

# ===============================
# CONFIGURACIÓN DEL MODELO
# ===============================
print("Cargando modelo... (puede tardar unos minutos la primera vez)")
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = pipe.to(device)
print("Modelo cargado correctamente ✅")

# ===============================
# BASE DE DATOS SIMPLE DE ANIMALES
# ===============================
caracteristicas = {
    "León": "Fuerte, valiente y con una melena imponente.",
    "Tigre": "Ágil, sigiloso y con rayas distintivas.",
    "Elefante": "Grande, inteligente y con trompa poderosa.",
    "Lobo": "Rápido, cazador y leal a su manada.",
    "Caballo": "Elegante, veloz y resistente.",
    "Gato": "Astuto, independiente y curioso.",
    "Perro": "Fiel, protector y amistoso.",
    "Jirafa": "Alta, tranquila y con un largo cuello.",
    "Cebra": "Ágil, veloz y con rayas únicas.",
    "Oso": "Fuerte, robusto y gran nadador.",
    "Tiburón": "Depredador del mar, rápido y feroz.",
    "Delfín": "Inteligente, amistoso y juguetón.",
    "Pulpo": "Flexible, misterioso y con ocho brazos.",
    "Calamar": "Rápido, escurridizo y nocturno.",
    "Ballena": "Gigante del mar, pacífica y poderosa.",
    "Medusa": "Transparente, silenciosa y venenosa.",
    "Caballito de mar": "Pequeño, elegante y protector.",
    "Foca": "Ágil en el agua, divertida y sociable.",
    "Manta raya": "Grácil, grande y pacífica.",
    "Pez payaso": "Colorido, protector y valiente.",
    "Águila": "Majestuosa, con vista aguda y poderosa.",
    "Halcon": "Rápido, cazador y preciso.",
    "Murciélago": "Nocturno, ágil y con ecolocalización.",
    "Búho": "Sabio, silencioso y cazador nocturno.",
    "Loro": "Colorido, hablador y social.",
    "Paloma": "Pacífica, elegante y viajera.",
    "Gaviota": "Costera, libre y ruidosa.",
    "Flamenco": "Elegante, rosado y de largas patas.",
    "Cuervo": "Inteligente, misterioso y astuto.",
    "Pato": "Sociable, acuático y adaptable."
}

# ===============================
# LISTAS DE ANIMALES
# ===============================
terrestres = ["León", "Tigre", "Elefante", "Lobo", "Caballo", "Gato", "Perro", "Jirafa", "Cebra", "Oso"]
acuaticos = ["Tiburón", "Delfín", "Pulpo", "Calamar", "Ballena", "Medusa", "Caballito de mar", "Foca", "Manta raya", "Pez payaso"]
aereos = ["Águila", "Halcon", "Murciélago", "Búho", "Loro", "Paloma", "Gaviota", "Flamenco", "Cuervo", "Pato"]
todos = terrestres + acuaticos + aereos

# ===============================
# FUNCIONES
# ===============================
def generar_imagen():
    animal1 = combo1.get()
    animal2 = combo2.get()
    if not animal1 or not animal2:
        messagebox.showwarning("Faltan datos", "Por favor selecciona los dos animales.")
        return

    prompt = (
        f"Un híbrido completo entre un {animal1} y un {animal2}, "
        f"de cuerpo entero, estilo digital realista, colorido, detallado, fondo natural."
    )
    messagebox.showinfo("Generando", "Creando la imagen, por favor espera unos segundos...")

    image = pipe(prompt, num_inference_steps=30).images[0]

    os.makedirs("assets", exist_ok=True)
    ruta_img = f"assets/{animal1}_{animal2}_hibrido.png"
    image.save(ruta_img)

    mostrar_imagen(ruta_img)

    # Mostrar características
    mostrar_caracteristicas(animal1, animal2)

def mostrar_imagen(path):
    img = Image.open(path)
    img = img.resize((400, 400))
    img_tk = ImageTk.PhotoImage(img)
    label_imagen.config(image=img_tk)
    label_imagen.image = img_tk

def mostrar_caracteristicas(animal1, animal2):
    texto1 = caracteristicas.get(animal1, "Sin información.")
    texto2 = caracteristicas.get(animal2, "Sin información.")
    mezcla = random.choice([
        "Combina la fuerza de uno y la agilidad del otro.",
        "Su apariencia es sorprendente, con habilidades únicas.",
        "Posee lo mejor de ambos mundos, terrestre y aéreo.",
        "Un ser extraordinario con instinto y elegancia fusionados."
    ])
    hibrido = f"El híbrido entre {animal1} y {animal2} tiene {mezcla}"

    texto_final = (
        f"🐾 {animal1}: {texto1}\n"
        f"🐾 {animal2}: {texto2}\n\n"
        f"🌟 Híbrido: {hibrido}"
    )

    label_info.config(text=texto_final)

# ===============================
# INTERFAZ GRÁFICA
# ===============================
root = tk.Tk()
root.title("Simulador de Cruce Genético 🧬")
root.geometry("950x700")
root.config(bg="#18122B")

style = ttk.Style()
style.theme_use("clam")

frame = tk.Frame(root, bg="#443C68", bd=10, relief="ridge")
frame.pack(pady=20)

tk.Label(frame, text="Selecciona los animales para el cruce 🧬", font=("Arial", 16), bg="#443C68", fg="white").pack(pady=10)

# Combos de selección
frame_select = tk.Frame(frame, bg="#443C68")
frame_select.pack(pady=10)

combo1 = ttk.Combobox(frame_select, values=todos, width=25, font=("Arial", 12))
combo1.grid(row=0, column=0, padx=20)
combo2 = ttk.Combobox(frame_select, values=todos, width=25, font=("Arial", 12))
combo2.grid(row=0, column=1, padx=20)

# Botón generar
btn = tk.Button(frame, text="🔬 Generar Cruce", font=("Arial", 14), bg="#635985", fg="white", command=generar_imagen)
btn.pack(pady=20)

# Imagen del híbrido
label_imagen = tk.Label(root, bg="#18122B")
label_imagen.pack(pady=10)

# Características
label_info = tk.Label(root, text="", font=("Arial", 12), fg="white", bg="#18122B", justify="left", wraplength=800)
label_info.pack(pady=10)

root.mainloop()
