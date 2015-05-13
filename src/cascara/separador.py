# coding: utf-8

from Queue import Queue


class SeparaJSON(object):
    """Maquina de pila estados para separar los paquetes, basados en la
    cantidad de llaves"""

    # Estados
    ESPERO_APERTURA = 'ESPERO_APERTURA'
    ABIERTO = 'ABIERTO'

    def __init__(self):
        """Constructor"""
        # Almacenamiento temporal
        self.buff = ''
        self.estado = self.ESPERO_APERTURA
        self.cantidad_llaves = 0
        self.mensajes = Queue()

    def procesar(self, data):
        """Procesa una cadena de entrada (de caracter a caracter)"""
        for c in data:
            self.procesar_char(c)

    def procesar_char(self, c):
        """Procesa un caracter de entrad"""

        if self.estado == self.ESPERO_APERTURA:
            if c == '{':
                self.estado = self.ABIERTO
                self.cantidad_llaves += 1
                self.buff += c
            else:
                pass  # Descarte
        elif self.estado == self.ABIERTO:
            if c == '}':
                self.cantidad_llaves -= 1
                self.buff += c
                if self.cantidad_llaves == 0:
                    # Mensaje completo, se desapilaron todas las llaves
                    self.mensajes.put(self.buff)
                    print self.buff
                    self.buff = ''
                    self.estado = self.ESPERO_APERTURA
            elif c == '{':
                self.cantidad_llaves += 1
                self.buff += c
            else:
                self.buff += c

    def disponible(self):
        return not self.mensajes.empty()

    def siguiente(self):
        """Devuelve el próximo mensaje"""
        return self.mensajes.get()

    def __iter__(self):
        """Iterador para for"""
        return IterQueue(self.mensajes)


class IterQueue(object):
    def __init__(self, q):
        self.q = q

    def next(self):
        if self.q.empty():
            raise StopIteration()
        return self.q.get()
