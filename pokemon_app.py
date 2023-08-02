import requests
import random
import tkinter as tk
from tkinter import Label, Button, messagebox
from PIL import Image, ImageTk
from io import BytesIO

imagen_tk = None  # Variable global para almacenar la imagen del Pokémon

def obtener_pokemon_aleatorio():
    url_base = "https://pokeapi.co/api/v2/pokemon/"
    numero_pokemon = random.randint(1, 898)  # Hay 898 Pokémon en total hasta septiembre de 2021.
    url = f"{url_base}{numero_pokemon}/"

    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        pokemon = respuesta.json()
        return pokemon
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudo obtener el Pokémon: {e}")
        return None

def mostrar_pokemon():
    global imagen_tk  # Indicamos que queremos utilizar la variable global

    pokemon_aleatorio = obtener_pokemon_aleatorio()

    if pokemon_aleatorio:
        nombre = pokemon_aleatorio["name"].capitalize()
        id_pokemon = pokemon_aleatorio["id"]
        imagen_url = pokemon_aleatorio["sprites"]["other"]["official-artwork"]["front_default"]
        tipos = ", ".join(tipo["type"]["name"].capitalize() for tipo in pokemon_aleatorio["types"])
        habilidades = ", ".join(habilidad["ability"]["name"].capitalize() for habilidad in pokemon_aleatorio["abilities"])
        stats = "\n".join(
            f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}"
            for stat in pokemon_aleatorio["stats"]
        )

        ventana = tk.Toplevel()
        ventana.title(f"Información del Pokémon: {nombre}")
        ventana.geometry("500x600")

        etiqueta_nombre = Label(ventana, text=f"Nombre: {nombre}", font=("Helvetica", 16, "bold"))
        etiqueta_nombre.pack(pady=5)

        etiqueta_id = Label(ventana, text=f"Número de Pokédex: {id_pokemon}", font=("Helvetica", 12))
        etiqueta_id.pack(pady=2)

        etiqueta_tipos = Label(ventana, text=f"Tipos: {tipos}", font=("Helvetica", 12))
        etiqueta_tipos.pack(pady=2)

        etiqueta_habilidades = Label(ventana, text=f"Habilidades: {habilidades}", font=("Helvetica", 12))
        etiqueta_habilidades.pack(pady=2)

        etiqueta_stats = Label(ventana, text="Estadísticas:", font=("Helvetica", 14, "bold"))
        etiqueta_stats.pack(pady=5)

        etiqueta_stats_info = Label(ventana, text=stats, font=("Helvetica", 12))
        etiqueta_stats_info.pack()

        imagen_respuesta = requests.get(imagen_url)
        imagen_pil = Image.open(BytesIO(imagen_respuesta.content))
        imagen_pil.thumbnail((200, 200))
        imagen_tk = ImageTk.PhotoImage(imagen_pil)

        etiqueta_imagen = Label(ventana, image=imagen_tk)
        etiqueta_imagen.image = imagen_tk
        etiqueta_imagen.pack(pady=10)

        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() - ventana.winfo_reqwidth()) // 2
        y = (ventana.winfo_screenheight() - ventana.winfo_reqheight()) // 2
        ventana.geometry(f"+{x}+{y}")

    else:
        messagebox.showwarning("Error", "No se pudo obtener información del Pokémon.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pokémon Aleatorio")

    boton_mostrar = Button(root, text="Mostrar Pokémon", command=mostrar_pokemon, font=("Helvetica", 14, "bold"))
    boton_mostrar.pack(pady=20)

    root.mainloop()








