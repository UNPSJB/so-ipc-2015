import os
from glob import glob

def cargar_imagenes_carpeta(expresion="*.png"):
    imagenes = {}
    for archivo in glob(expresion):
        clave = os.path.basename(archivo)
        imagenes[clave] = loadImage(archivo)
        print "Se cargo la imagen %s" % clave
    return imagenes
