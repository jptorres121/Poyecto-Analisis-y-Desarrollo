import tkinter as tk
from tkinter import ttk, messagebox
import random
from PIL import Image, ImageTk
from io import BytesIO

# Si usas stable diffusion localmente:
from diffusers import StableDiffusionPipeline
import torch

from data.animales import terrestres, aereos, acuaticos
from data.caracteristicas import rasgos, mutaciones

# ======================================
# CARGAR MODELO DE STABLE DIFFUSION
# ======================================
print("Cargando modelo de Stable Diffusion... esto puede tardar un poco.")

# Elegir dtype según dispositivo (evita usar float16 en CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if device == "cuda" else torch.float32

try:
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch_dtype
    )
    pipe = pipe.to(device)
    print(f"Modelo cargado correctamente en {device} ✅")
except Exception as e:
    # Si falla la carga del modelo, dejamos pipe = None y se mostrará un error al intentar generar la imagen
    pipe = None
    print("No se pudo cargar el modelo de Stable Diffusion:", e)

# ======================================
# FUNCIÓN PRINCIPAL
# ======================================
def crear_pestana_simulacion(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Cruce Genético")

    tk.Label(frame, text="Selecciona los animales para el cruce:", font=("Helvetica", 12, "bold")).pack(pady=10)

    todos = terrestres + aereos + acuaticos

    tk.Label(frame, text="Padre 1:", font=("Helvetica", 11)).pack()
    combo_padre1 = ttk.Combobox(frame, width=40, values=todos)
    combo_padre1.pack(pady=5)

    tk.Label(frame, text="Padre 2:", font=("Helvetica", 11)).pack()
    combo_padre2 = ttk.Combobox(frame, width=40, values=todos)
    combo_padre2.pack(pady=5)

    # Cuadro de texto
    resultado_text = tk.Text(frame, width=90, height=10, wrap="word", bg="#F8F9FA", fg="#000", font=("Courier", 10))
    resultado_text.pack(pady=10)

    # Etiqueta para imagen
    lbl_imagen = tk.Label(frame, bg="#DDE6ED")
    lbl_imagen.pack(pady=10)

    # Función para realizar el cruce genético
    def realizar_cruce():
        animal1 = combo_padre1.get()
        animal2 = combo_padre2.get()

        if not animal1 or not animal2:
            messagebox.showwarning("Selección incompleta", "Debes elegir dos animales para realizar el cruce.")
            return

        rasgo1 = random.choice(rasgos)
        rasgo2 = random.choice(rasgos)
        mutacion = random.choice(mutaciones)

        prompt = (
            f"Ilustración científica 2D de un híbrido entre un {animal1} y un {animal2}, "
            f"representado con proporciones anatómicas coherentes y estilo naturalista. "
            f"El entorno combina los hábitats típicos de ambos animales, con iluminación suave y fondo realista. "
            f"El híbrido presenta rasgos combinados de {animal1} y {animal2}, "
            f"sin deformidades, sin duplicaciones, sin errores anatómicos. "
            f"Estilo de ilustración biológica profesional, textura detallada, colores naturales."
        )

        resultado = f"""
Resultado del cruce genético:
---------------------------------
Padre 1: {animal1}
Padre 2: {animal2}

Rasgos heredados:
- De {animal1}: {rasgo1}
- De {animal2}: {rasgo2}

Mutación: {mutacion if mutacion else 'No presenta mutaciones detectables.'}

🧠 Prompt IA usado:
{prompt}
"""

        resultado_text.delete("1.0", tk.END)
        resultado_text.insert(tk.END, resultado.strip())

        # Generar imagen con Stable Diffusion (si el modelo está cargado)
        if pipe is None:
            messagebox.showerror("Modelo no disponible", "El modelo de Stable Diffusion no está cargado. Revisa la consola.")
            return

        try:
            resultado_text.insert(tk.END, "\n\nGenerando imagen...")
            # actualizar solo el frame para reflejar el texto "Generando imagen..."
            frame.update()

            # generar imagen (esto puede tardar)
            sd_output = pipe(prompt)
            image = sd_output.images[0]
            image = image.resize((512, 512))  # redimensiona

            img_tk = ImageTk.PhotoImage(image)

            # actualizar label con la imagen (guardar referencia para evitar garbage collector)
            lbl_imagen.config(image=img_tk)
            lbl_imagen.image = img_tk
        except Exception as e:
            messagebox.showerror("Error al generar imagen", str(e))

    # Botón
    tk.Button(
        frame,
        text="🔬 Realizar Cruce y Generar Imagen",
        command=realizar_cruce,
        bg="#526D82",
        fg="white",
        font=("Helvetica", 12, "bold"),
        relief="flat",
        padx=10, pady=5
    ).pack(pady=15)

    return frame
