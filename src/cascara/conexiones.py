# coding: utf-8
import subprocess
import json
from thread import start_new_thread, allocate_lock
import socket

hilos_lock = allocate_lock()
hilos = {} # Evitar que sean eliminados por el GC

def kill_procesos_escuchando_en_puerto(puerto):
    assert 1024 < puerto < 65536
    comando = "lsof -i TCP:%d | grep LISTEN | awk '{print $2}'" % puerto
    pids = subprocess.check_output(comando, shell=True).split()
    for pid in pids:
        if pid and int(pid) != os.getpid():
            print "Matando proceso %s que escucha el puerto 4455"
            subprocess.call('kill -9 %s' % pid, shell=True)

def espera_clientes(conexion, on_mensaje):
    while True:
        cliente, (ip, puerto) = conexion.accept()
        hilo = start_new_thread(atiende_cliente, (cliente, ip, puerto, on_mensaje))
        with hilos_lock:
            hilos[puerto] = hilo

def atiende_cliente(cliente, ip, puerto, on_mensaje):
    print "Llegó cliente desde %s %d" % (ip, puerto)
    while True:
        cadena = cliente.recv(100)
        if not cadena:
            print "Se fue el cliente!"
            cliente.close()
            with hilos_lock:
                del hilos[puerto] # Eliminar referencia para ser GC'd
            break
        try:
            mensaje = json.loads(cadena)
            if 'numero' not in mensaje:
                print "El cliente no dijo que modificar"
            else:
                on_mensaje(mensaje)
        except ValueError:
            print "Porblemas con JSON"
        except KeyError as e:
            print "JSON no tiene algun atributo necesario %s" % e

def escuchar_clientes_en_hilo(on_mensaje=None, puerto=4455, matar_otros=False):
    """
    Lanza un hilo escuchando conexiones en el puerto ``puerto``.
    Retorna la conexion para poder ser cerrada
    """
    assert callable(on_mensaje), "Se esperaba una función"
    if matar_otros:
        kill_procesos_escuchando_en_puerto(puerto)
        
    conexion = socket.socket()
    conexion.bind(('localhost', 4455))
    conexion.listen(10)
    start_new_thread(espera_clientes, (conexion, on_mensaje))
    return conexion

    start_new_thread(espera_clientes, (conexion, ))
    
