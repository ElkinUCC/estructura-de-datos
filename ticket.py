from datetime import datetime
from enum import Enum


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
    """Lista doblemente enlazada de tickets ordenados por prioridad."""

    def __init__(self):
        self.cabeza = None    # Mayor prioridad
        self.extremo = None   # Menor prioridad
        self._total = 0


    # ----------------------------------------------------
    # INSERTAR ORDENADO POR PRIORIDAD  O(n)
    # ----------------------------------------------------
    def agregar_ticket(self, ticket):

        # 1️⃣ Si la lista está vacía
        if self.cabeza is None:
            self.cabeza = ticket
            self.extremo = ticket
            self._total += 1
            return

        actual = self.cabeza

        # 2️⃣ Recorrer la lista
        while actual is not None:

            # 🔹 Caso 1: nueva prioridad es MÁS ALTA
            if ticket.prioridad.value < actual.prioridad.value:

                ticket.siguiente = actual
                ticket.anterior = actual.anterior

                if actual.anterior is not None:
                    actual.anterior.siguiente = ticket
                else:
                    self.cabeza = ticket

                actual.anterior = ticket
                self._total += 1
                return

            # 🔹 Caso 2: misma prioridad
            if ticket.prioridad == actual.prioridad:

                # avanzar hasta el último del mismo nivel
                while actual.siguiente is not None and \
                        actual.siguiente.prioridad == ticket.prioridad:
                    actual = actual.siguiente

                ticket.siguiente = actual.siguiente
                ticket.anterior = actual

                if actual.siguiente is not None:
                    actual.siguiente.anterior = ticket
                else:
                    self.extremo = ticket

                actual.siguiente = ticket
                self._total += 1
                return

            actual = actual.siguiente

        # 🔹 Caso 3: es la menor prioridad → va al final
        self.extremo.siguiente = ticket
        ticket.anterior = self.extremo
        self.extremo = ticket
        self._total += 1

    # ----------------------------------------------------
    # ATENDER PRIMERO  O(1)
    # ----------------------------------------------------
    def atender_primero(self):

        if self.cabeza is None:
            return None

        eliminado = self.cabeza
        self.cabeza = eliminado.siguiente

        if self.cabeza is not None:
            self.cabeza.anterior = None
        else:
            self.extremo = None  # quedó vacía

        self._total -= 1
        return eliminado

    # ----------------------------------------------------
    # BUSCAR  O(n)
    # ----------------------------------------------------
    def buscar_ticket(self, id_ticket):

        actual = self.cabeza

        while actual is not None:
            if actual.id_ticket == id_ticket:
                return actual
            actual = actual.siguiente

        return None

    # ----------------------------------------------------
    # REASIGNAR  O(n)
    # ----------------------------------------------------
    def reasignar(self, id_ticket, nuevo_tecnico):

        nodo = self.buscar_ticket(id_ticket)

        if nodo is not None:
            nodo.tecnico = nuevo_tecnico
            return True

        return False

    # ----------------------------------------------------
    # LISTAR ADELANTE  O(n)
    # ----------------------------------------------------
    def listar_adelante(self):

        actual = self.cabeza

        while actual is not None:
            print(f"[{actual.id_ticket} - {actual.prioridad.name}]",
                  end=" <-> ")
            actual = actual.siguiente

        print("None")

    # ----------------------------------------------------
    # LISTAR ATRÁS  O(n)
    # ----------------------------------------------------
    def listar_atras(self):

        actual = self.extremo

        while actual is not None:
            print(f"[{actual.id_ticket} - {actual.prioridad.name}]",
                  end=" <-> ")
            actual = actual.anterior

        print("None")

    # ----------------------------------------------------
    # ESTADÍSTICAS  O(n)
    # ----------------------------------------------------
    def estadisticas(self):

        alta = 0
        media = 0
        baja = 0

        actual = self.cabeza

        while actual is not None:

            if actual.prioridad == Prioridad.ALTA:
                alta += 1
            elif actual.prioridad == Prioridad.MEDIA:
                media += 1
            else:
                baja += 1

            actual = actual.siguiente

        print("ALTA:", alta)
        print("MEDIA:", media)
        print("BAJA:", baja)

if __name__ == "__main__":

    print("=========== PRUEBA GENERAL COMPLETA ===========\n")

    lista = ListaTickets()

    # 1️⃣ Insertamos tickets en desorden de prioridad
    lista.agregar_ticket(Ticket(1, "Media 1", Prioridad.MEDIA, "Carlos"))
    lista.agregar_ticket(Ticket(2, "Alta 1", Prioridad.ALTA, "Ana"))
    lista.agregar_ticket(Ticket(3, "Baja 1", Prioridad.BAJA, "Luis"))
    lista.agregar_ticket(Ticket(4, "Alta 2", Prioridad.ALTA, "Pedro"))
    lista.agregar_ticket(Ticket(5, "Media 2", Prioridad.MEDIA, "Laura"))

    print("→ Recorrido hacia adelante (debe ser ALTA, ALTA, MEDIA, MEDIA, BAJA):")
    lista.listar_adelante()

    print("\n→ Recorrido hacia atrás:")
    lista.listar_atras()

    print("\n→ Total actual:", lista._total)

    # 2️⃣ Buscar ticket
    print("\n→ Buscar ID 3:")
    encontrado = lista.buscar_ticket(3)
    print("Encontrado:", encontrado is not None)

    # 3️⃣ Reasignar técnico
    print("\n→ Reasignar técnico del ID 5:")
    lista.reasignar(5, "Miguel")
    print("Nuevo técnico:", lista.buscar_ticket(5).tecnico)

    # 4️⃣ Atender primero (debe eliminar la primera ALTA)
    print("\n→ Atender primero:")
    atendido = lista.atender_primero()
    print("Se atendió:", atendido.id_ticket, "-", atendido.prioridad.name)

    print("\n→ Lista después de atender:")
    lista.listar_adelante()

    # 5️⃣ Mostrar estadísticas
    print("\n→ Estadísticas:")
    lista.estadisticas()

    print("\n=========== FIN PRUEBA ===========")