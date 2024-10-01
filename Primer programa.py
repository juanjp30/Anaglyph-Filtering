from tkinter import *
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import imutils
import PIL, PIL.Image, PIL.ImageOps, PIL.ImageEnhance

# Variables globales
left_image = None
right_image = None
left_label = None
right_label = None
image_window = None
left_image_pil = None
right_image_pil = None
original_left_image_pil = None
original_right_image_pil = None
tamaño_vertical = 0
tamaño_horizontal = 0
Filtrado = False

# Función para abrir y seleccionar archivos de imagen
def open_file():
    global left_image, right_image, left_label, right_label, image_window, left_image_pil, right_image_pil, tamaño_horizontal, tamaño_vertical
    
    if image_window is None or not image_window.winfo_exists():
        image_window = tk.Toplevel(root)
        image_window.title("Imagen")
        image_window.attributes('-fullscreen', True)
    
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp")])
    if not file_path:
        return
    
    image = Image.open(file_path)

    tamaño = image.size
    tamaño_vertical = tamaño[1]
    tamaño_horizontal = tamaño[0]

    # Imprime el tamaño de la imagen importada
    print(f"Tamaño de la imagen importada: {tamaño}")
    print(f"Tamaño de la imagen importada: {tamaño_vertical}")
    print(f"Tamaño de la imagen importada: {tamaño_horizontal}")
    
    if left_image is None:
        #image = image.resize((tamaño_vertical // 2, tamaño_horizontal), Image.LANCZOS)
        image.thumbnail((tamaño_horizontal // 2, tamaño_vertical), Image.LANCZOS)
        image_tk = ImageTk.PhotoImage(image)
        left_image, left_image_pil = image_tk, image
        left_label = tk.Label(image_window, image=left_image)
        left_label.pack(side="left", padx=1, pady=1, expand=True, fill='both')
    elif right_image is None:
        #image = image.resize((tamaño_vertical // 2, tamaño_horizontal), Image.LANCZOS)
        image.thumbnail((tamaño_horizontal // 2, tamaño_vertical), Image.LANCZOS)
        image_tk = ImageTk.PhotoImage(image)
        right_image, right_image_pil = image_tk, image
        right_label = tk.Label(image_window, image=right_image)
        right_label.pack(side="left", padx=1, pady=1, expand=True, fill='both')
    else:
        image = image.resize((image_window.winfo_screenwidth() // 2, image_window.winfo_screenheight()), Image.LANCZOS)
        image_tk = ImageTk.PhotoImage(image)
        right_image, right_image_pil = image_tk, image
        right_label.config(image=right_image)
        right_label.image = right_image

# Función auxiliar para redimensionar y actualizar las imágenes
def resize_and_update_images(max_width, max_height, maintain_aspect_ratio=False):
    global left_image, right_image, left_image_pil, right_image_pil, tamaño_horizontal, tamaño_vertical

    if maintain_aspect_ratio:
        left_image_pil.thumbnail((max_width, max_height), Image.LANCZOS)
        right_image_pil.thumbnail((max_width, max_height), Image.LANCZOS)
    else:
        left_image_pil = left_image_pil.resize((max_width, max_height), Image.LANCZOS)
        right_image_pil = right_image_pil.resize((max_width, max_height), Image.LANCZOS)
    
    left_image = ImageTk.PhotoImage(left_image_pil)
    right_image = ImageTk.PhotoImage(right_image_pil)

    left_label.config(image=left_image)
    left_label.image = left_image
    right_label.config(image=right_image)
    right_label.image = right_image

# Función para colocar dos imágenes una al lado de la otra
def arrange_horizontal():
    global left_image_pil, right_image_pil, left_image, right_image, left_label, right_label
    
    if left_image_pil is not None and right_image_pil is not None:
        # Obtener las dimensiones de la pantalla
        screen_width = image_window.winfo_screenwidth()
        screen_height = image_window.winfo_screenheight()

        # Redimensionar cada imagen para que ocupe la mitad de la pantalla en ancho
        new_width = screen_width // 2
        new_height = screen_height
        
        # Aplastar las imágenes: reducir el ancho al 50% del tamaño original
        left_image_pil_resized = left_image_pil.resize((new_width, new_height), Image.LANCZOS)
        right_image_pil_resized = right_image_pil.resize((new_width, new_height), Image.LANCZOS)
        
        # Convertir a ImageTk para mostrar en la interfaz
        left_image = ImageTk.PhotoImage(left_image_pil_resized)
        right_image = ImageTk.PhotoImage(right_image_pil_resized)
        
        # Actualizar las etiquetas
        if left_label is not None:
            left_label.config(image=left_image)
        if right_label is not None:
            right_label.config(image=right_image)
        
        # Posicionar las imágenes en la vista horizontal
        left_label.pack(side="left", expand=True, fill='both')
        right_label.pack(side="right", expand=True, fill='both')


# Función para colocar dos imágenes una encima de la otra
def arrange_vertical():
    #screen_width = image_window.winfo_screenwidth()
    #screen_height = image_window.winfo_screenheight()
    global tamaño_vertical, tamaño_horizontal
    print(f"Tamaño de la imagen importada: {tamaño_vertical}")
    print(f"Tamaño de la imagen importada: {tamaño_horizontal}")
    resize_and_update_images(tamaño_horizontal, tamaño_vertical // 2, maintain_aspect_ratio=True)
    left_label.pack(side="top", padx=1, pady=1, expand=True, fill='both')
    right_label.pack(side="top", padx=1, pady=1, expand=True, fill='both')

# Función para intercambiar las imágenes de lugar
def swap_images():
    global left_image, right_image, left_image_pil, right_image_pil

    if left_image and right_image:
        left_image, right_image = right_image, left_image
        left_image_pil, right_image_pil = right_image_pil, left_image_pil

        if left_label.pack_info()['side'] == 'left':
            arrange_horizontal()
        else:
            arrange_vertical()

#Funcion para el filtrado
def filtrado():
    
    global left_image_pil, right_image_pil, left_image, right_image, original_left_image_pil, original_right_image_pil, Filtrado

    # Guarda las imágenes originales si no se han guardado aún
    if original_left_image_pil is None and original_right_image_pil is None:
        original_left_image_pil = left_image_pil.copy()
        original_right_image_pil = right_image_pil.copy()

    #Filtrado
    if left_label is not None and right_label is not None:
        if left_label.winfo_exists() and right_label.winfo_exists():
            left_image_pil = PIL.ImageOps.grayscale(left_image_pil)
            right_image_pil = PIL.ImageOps.grayscale(right_image_pil)
            left_image_pil = PIL.ImageOps.colorize(left_image_pil, (0, 0, 0), (255, 0, 0))
            right_image_pil = PIL.ImageOps.colorize(right_image_pil, (0, 0, 0), (0, 255, 255))
            arrange_horizontal()
    else:
        print("Error: No se han inicializado left_label o right_label")
Filtrado = True      
    
#Funcion para visualizar de manera 3D
def TresD():
    global left_image_pil, right_image_pil, left_image, right_image, original_left_image_pil, original_right_image_pil, Filtrado
    #Visualizacion 3D
    if left_label.pack_info()['side'] == 'left' and Filtrado:
        blend = PIL.Image.blend(left_image_pil, right_image_pil, alpha=0.5)
        np_blend = np.array(blend)
        Im_3D = imutils.resize(np_blend, width=700)
        Im_3D = cv2.cvtColor(Im_3D, cv2.COLOR_BGR2RGB)  
        cv2.imshow("Imagen 3D", Im_3D)
        cv2.waitKey(0)
        

# Función para restaurar las imágenes originales
def restaurar_imagenes():
    global left_image_pil, right_image_pil, left_image, right_image, original_left_image_pil, original_right_image_pil
    
    if original_left_image_pil is not None and original_right_image_pil is not None:
        left_image_pil = original_left_image_pil.copy()
        right_image_pil = original_right_image_pil.copy()
        
        # Actualiza las imágenes en los labels
        left_image = PIL.ImageTk.PhotoImage(left_image_pil)
        right_image = PIL.ImageTk.PhotoImage(right_image_pil)
        
        if left_label.winfo_exists() and right_label.winfo_exists():
            left_label.config(image=left_image)
            right_label.config(image=right_image)

# Crear la ventana principal
root = tk.Tk()
root.title("Interfaz Gráfica con Botones")

# Crear los botones y asignar las funciones
btn_open = tk.Button(root, text="Abrir Archivo", command=open_file)
btn_open.pack(pady=5)

btn_horizontal = tk.Button(root, text="Colocar Horizontal", command=arrange_horizontal)
btn_horizontal.pack(pady=5)

btn_vertical = tk.Button(root, text="Colocar Vertical", command=arrange_vertical)
btn_vertical.pack(pady=5)

btn_swap = tk.Button(root, text="Intercambiar Imágenes", command=swap_images)
btn_swap.pack(pady=5)

btn_swap = tk.Button(root, text="Filtrar imagenes", command=filtrado)
btn_swap.pack(pady=5)

btn_swap = tk.Button(root, text="Mostrar en 3D", command=TresD)
btn_swap.pack(pady=5)

btn_swap = tk.Button(root, text="Modo Normal", command=restaurar_imagenes)
btn_swap.pack(pady=5)

# Ejecutar el bucle principal de la aplicación
root.mainloop()