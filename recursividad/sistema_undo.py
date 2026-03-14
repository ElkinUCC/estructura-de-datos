from datetime import datetime
from enum import Enum


class TipoAccion(Enum):
    INSERTAR = 'insertar'
    ELIMINAR = 'eliminar'
    REEMPLAZAR = 'reemplazar'
    FORMATO = 'formato'


class Accion:

    def __init__(self, tipo, antes, despues, posicion):
        self.tipo = tipo
        self.estado_antes = antes
        self.estado_despues = despues
        self.posicion = posicion
        self.timestamp = datetime.now()

        self.siguiente = None
        self.anterior = None


class HistorialAcciones:

    def __init__(self, max_acciones=50):
        self.cabeza = None
        self.extremo = None
        self.cursor = None
        self._total = 0
        self.max_acciones = max_acciones


# ---------------------------------------------------
# REGISTRAR ACCION
# ---------------------------------------------------

    def registrar(self, accion):

        # Si el cursor no está al final
        if self.cursor and self.cursor.siguiente:

            nodo = self.cursor.siguiente

            while nodo:
                siguiente = nodo.siguiente
                nodo.anterior = None
                nodo.siguiente = None
                nodo = siguiente
                self._total -= 1

            self.cursor.siguiente = None
            self.extremo = self.cursor

        # Insertar nuevo nodo
        if self.cabeza is None:
            self.cabeza = accion
            self.extremo = accion
            self.cursor = accion
            self._total = 1
            return

        accion.anterior = self.extremo
        self.extremo.siguiente = accion

        self.extremo = accion
        self.cursor = accion
        self._total += 1

        # Limitar historial
        if self._total > self.max_acciones:

            self.cabeza = self.cabeza.siguiente
            self.cabeza.anterior = None
            self._total -= 1


# ---------------------------------------------------
# UNDO
# ---------------------------------------------------

    def retroceder(self):

        if not self.puede_retroceder():
            return None

        accion = self.cursor
        self.cursor = self.cursor.anterior

        return accion.estado_antes


# ---------------------------------------------------
# REDO
# ---------------------------------------------------

    def avanzar(self):

        if not self.puede_avanzar():
            return None

        if self.cursor is None:
            self.cursor = self.cabeza
        else:
            self.cursor = self.cursor.siguiente

        return self.cursor.estado_despues


# ---------------------------------------------------

    def puede_retroceder(self):
        return self.cursor is not None

    def puede_avanzar(self):

        if self.cursor is None:
            return self.cabeza is not None

        return self.cursor.siguiente is not None


# ---------------------------------------------------
# VISUALIZAR HISTORIAL
# ---------------------------------------------------

    def visualizar(self):

        actual = self.cabeza

        while actual:

            marca = " "

            if actual == self.cursor:
                marca = "*"

            print(f"[{marca}] {actual.tipo.value} ({actual.timestamp})")

            actual = actual.siguiente