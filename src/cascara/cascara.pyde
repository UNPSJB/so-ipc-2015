# src/cascara/imagenes.pyde 
from random import seed, randint
from conexiones import escuchar_clientes_en_hilo
from imagenes import cargar_imagenes_carpeta

# Variables Globales
ancho, alto = 500, 500
conexion = None
fondo = None
IMAGENES = cargar_imagenes_carpeta("*.png")
seed()

elem_pantalla = {
    1: {"x": randint(0, ancho), "y": randint(0, alto), "imagen": "1.png"}, 
    2: {"x": randint(0, ancho), "y": randint(0, alto),   "imagen": "2.png"},
    3: {"x": randint(0, ancho), "y": randint(0, alto),  "imagen": "3.png"},
}
fondo = loadImage('bg.jpg')

def setup():
    '''Inicialización'''
    global conexion
    size(500, 500)
     
    conexion = escuchar_clientes_en_hilo(
        on_mensaje=procesar_mensaje,
        matar_otros=True
    )
    
def procesar_mensaje(mensaje):
    n = mensaje["numero"]
    
    if n not in elem_pantalla:
        elem_pantalla[n] = {"imagen": "", "x": 250, "y": 250}
        
    if 'x' in mensaje:
        elem_pantalla[n]['x'] = mensaje['x']
    if 'y' in mensaje:
        elem_pantalla[n]['y'] = mensaje['y']
    
    # Si viene la imagen, existe en las cargadas?
    if "imagen" in mensaje:
        elem_pantalla[n]["imagen"] = mensaje["imagen"]


def stop():
    print "Cerrando"
    if conexion:
        conexion.close()

def draw():
    background(255, 255, 255) # Limpiar
    #image(fondo, 0, 0, ancho, alto)
    for id, elem in elem_pantalla.items():
        try:
            imagen = IMAGENES[elem["imagen"]]
        except KeyError:
            pass
        else:
            image(imagen, elem["x"], elem["y"])
