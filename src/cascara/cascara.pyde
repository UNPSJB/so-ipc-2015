# src/cascara/imagenes.pyde 

from conexiones import escuchar_clientes_en_hilo
from imagenes import cargar_imagenes_carpeta

# Variables Globales
conexion = None
IMAGENES = cargar_imagenes_carpeta("*.png")

elem_pantalla = {
    1: {"x": 100, "y": 100, "imagen": "1.png"}, 
    2: {"x": 0, "y": 200,   "imagen": "2.png"},
    3: {"x": 80, "y": 200,  "imagen": "2.png"},
}

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
    for id, elem in elem_pantalla.items():
        try:
            imagen = IMAGENES[elem["imagen"]]
        except KeyError:
            pass
        else:
            image(imagen, elem["x"], elem["y"])
