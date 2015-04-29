# src/imagenes/imagenes.pyde
import socket
from thread import start_new_thread # versión de pthread_create
import json 
import os # trabajar con rutas de archivos
import subprocess # Llamara a BASH

# Variables Globales
conexion = None
hilos = []
IMAGENES = {}


def cargar_imagen(ruta, destino=IMAGENES):
    if not os.path.isfile(ruta):
        print "Error: %s no es un archivo en %s" % (ruta, os.getcwd())
    else:
        # Calcular el nombre de archivo
        basename = os.path.basename(ruta) # /ruta/a/fichero.jpg -> fichero.jpg
        # Usarlo como clave
        destino[basename] = loadImage(ruta)

cargar_imagen("1.png")
cargar_imagen("2.png")

# Debug
print IMAGENES

cajas = {
    1: {"x": 100, "y": 100, "imagen": "1.png"}, 
    2: {"x": 0, "y": 200,   "imagen": "2.png"},
    3: {"x": 80, "y": 200,  "imagen": "2.png"},
}

def kill_procesos_escuchando_en_puerto(puerto):
    assert 1024 < puerto < 65536
    comando = "lsof -i TCP:%d | grep LISTEN | awk '{print $2}'" % puerto
    pids = subprocess.check_output(comando, shell=True).split()
    for pid in pids:
        if pid and int(pid) != os.getpid():
            print "Matando proceso %s que escucha el puerto 4455"
            subprocess.call('kill -9 %s' % pid, shell=True) 
    
def setup():
    '''Inicialización'''
    global conexion
    size(500, 500)
    kill_procesos_escuchando_en_puerto(4455)
    conexion = socket.socket()
    conexion.bind(('localhost', 4455))
    conexion.listen(10)
    start_new_thread(espera_clientes, (conexion, ))

def procesar_mensaje(mensaje):
    n = mensaje["numero"]
    
    if 'x' in mensaje:
        cajas[n]['x'] = mensaje['x']
    if 'y' in mensaje:
        cajas[n]['y'] = mensaje['y']
    
    # Si viene la imagen, existe en las cargadas?
    if "imagen" in mensaje:
        if mensaje["imagen"] not in IMAGENES or IMAGENES[mensaje["imagen"]] is None:
            print "No existe %s" % mensaje["imagen"]
        else:
            cajas[n]["imagen"] = mensaje["imagen"]

def atiende_cliente(cliente, direccion):
    print "Llegó cliente desde %s %d" % direccion
    while True:
        cadena = cliente.recv(100)
        if not cadena:
            print "Se fue el cliente!"
            break
        try:
            mensaje = json.loads(cadena)
            if 'numero' not in mensaje:
                print "El cliente no dijo que modificar"
            else:
                procesar_mensaje(mensaje)
        except ValueError:
            print "Porblemas con JSON"
        except KeyError as e:
            print "JSON no tiene algun atributo necesario %s" % e


def espera_clientes(conexion):
    global cajas
    while True:
        cliente, direccion = conexion.accept()
        hilo = start_new_thread(atiende_cliente, (cliente, direccion))
        hilos.append(hilo)

def stop():
    if conexion:
        conexion.close()

def draw():
    background(255, 255, 255) # Limpiar
    for id, caja in cajas.items():
        imagen = IMAGENES[caja["imagen"]]
        image(imagen, caja["x"], caja["y"])
