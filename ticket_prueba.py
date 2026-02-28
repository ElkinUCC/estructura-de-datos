from datetime import datetime
from enum import Enum
import random


class Prioridad(Enum):
    ALTA = 1
    MEDIA = 2
    BAJA = 3


class Ticket:
    def __init__(self, id_ticket, descripcion, prioridad, tecnico):
        self.id_ticket = id_ticket
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.tecnico = tecnico
        self.creado_en = datetime.now()
        self.anterior = None
        self.siguiente = None


class ListaTickets:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.total = 0

    # 🔹 Inserta manteniendo orden por prioridad
    def insertar(self, ticket):

        if self.cabeza is None:
            self.cabeza = ticket
            self.cola = ticket
            self.total += 1
            return

        actual = self.cabeza

        while actual is not None:
            # Si encontramos menor prioridad numérica (más importante)
            if ticket.prioridad.value < actual.prioridad.value:
                # Insertar antes de actual
                ticket.siguiente = actual
                ticket.anterior = actual.anterior

                if actual.anterior is not None:
                    actual.anterior.siguiente = ticket
                else:
                    self.cabeza = ticket

                actual.anterior = ticket
                self.total += 1
                return

            # Si es misma prioridad, seguir hasta el último del mismo nivel
            if ticket.prioridad == actual.prioridad:
                while actual.siguiente is not None and \
                        actual.siguiente.prioridad == ticket.prioridad:
                    actual = actual.siguiente

                ticket.siguiente = actual.siguiente
                ticket.anterior = actual

                if actual.siguiente is not None:
                    actual.siguiente.anterior = ticket
                else:
                    self.cola = ticket

                actual.siguiente = ticket
                self.total += 1
                return

            actual = actual.siguiente

        # Si no se insertó antes, va al final
        self.cola.siguiente = ticket
        ticket.anterior = self.cola
        self.cola = ticket
        self.total += 1

    def atender_primero(self):
        if self.cabeza is None:
            return None

        atendido = self.cabeza
        self.cabeza = self.cabeza.siguiente

        if self.cabeza is not None:
            self.cabeza.anterior = None
        else:
            self.cola = None

        self.total -= 1
        return atendido

    def buscar(self, id_ticket):
        actual = self.cabeza
        while actual is not None:
            if actual.id_ticket == id_ticket:
                return actual
            actual = actual.siguiente
        return None

    def recorrer_adelante(self):
        actual = self.cabeza
        while actual is not None:
            print(f"[{actual.id_ticket} - {actual.prioridad.name}]",
                  end=" <-> ")
            actual = actual.siguiente
        print("None")

    def recorrer_atras(self):
        actual = self.cola
        while actual is not None:
            print(f"[{actual.id_ticket} - {actual.prioridad.name}]",
                  end=" <-> ")
            actual = actual.anterior
        print("None")

if __name__ == "__main__":

    lista = ListaTickets()

    # 1 insertar en lista vacía
    lista.insertar(Ticket(1, "T1", Prioridad.MEDIA, "A"))

    # 2 insertar mayor prioridad
    lista.insertar(Ticket(2, "T2", Prioridad.ALTA, "B"))

    # 3 insertar menor prioridad
    lista.insertar(Ticket(3, "T3", Prioridad.BAJA, "C"))

    # 4 insertar misma prioridad ALTA
    lista.insertar(Ticket(4, "T4", Prioridad.ALTA, "D"))

    # 5 insertar misma prioridad MEDIA
    lista.insertar(Ticket(5, "T5", Prioridad.MEDIA, "E"))

    # 6 buscar existente
    print("Buscar ID 3:", lista.buscar(3) is not None)

    # 7 buscar inexistente
    print("Buscar ID 99:", lista.buscar(99) is None)

    # 8 atender primero
    print("Atendido:", lista.atender_primero().id_ticket)

    # 9 verificar total
    print("Total actual:", lista.total)

    # 10 recorrido adelante
    lista.recorrer_adelante()

    # 11 recorrido atrás
    lista.recorrer_atras()