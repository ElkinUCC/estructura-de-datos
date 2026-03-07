from enum import Enum

class EstadoProceso(Enum):
    NUEVO = 'NUEVO'
    LISTO = 'LISTO'
    EJECUTANDO = 'EJECUTANDO'
    BLOQUEADO = 'BLOQUEADO'
    TERMINADO = 'TERMINADO'

class Proceso:

    def __init__(self, pid, nombre, burst_total, llegada=0, prioridad=0):

        self.pid = pid
        self.nombre = nombre
        self.burst_total = burst_total
        self.burst_restante = burst_total
        self.llegada = llegada

        self.estado = EstadoProceso.NUEVO

        self.tiempo_espera = 0
        self.tiempo_respuesta = -1
        self.tiempo_finalizacion = 0

        self.siguiente = None
class AnilloProcesos:

    def __init__(self):

        self.actual = None
        self._total = 0


    def insertar_proceso(self, proceso):

        if self.actual is None:

            self.actual = proceso
            proceso.siguiente = proceso
            self._total += 1
            return

        ultimo = self.actual

        while ultimo.siguiente != self.actual:
            ultimo = ultimo.siguiente

        ultimo.siguiente = proceso
        proceso.siguiente = self.actual

        self._total += 1


    def retirar_proceso(self, pid):

        if self.actual is None:
            return None

        actual = self.actual
        anterior = None

        while True:

            if actual.pid == pid:

                if anterior:
                    anterior.siguiente = actual.siguiente
                else:
                    ultimo = self.actual
                    while ultimo.siguiente != self.actual:
                        ultimo = ultimo.siguiente

                    if actual == actual.siguiente:
                        self.actual = None
                    else:
                        ultimo.siguiente = actual.siguiente
                        self.actual = actual.siguiente

                self._total -= 1
                return actual

            anterior = actual
            actual = actual.siguiente

            if actual == self.actual:
                break

        return None


    def rotar(self):

        if self.actual:
            self.actual = self.actual.siguiente


    def esta_vacio(self):
        return self.actual is None

class SchedulerRoundRobin:

    def __init__(self, quantum):

        self.quantum = quantum
        self.anillo_activos = AnilloProcesos()

        self.procesos = []
        self.procesos_terminados = []

        self.tiempo_actual = 0
        self.gantt = []


    def agregar_proceso(self, proceso):

        self.procesos.append(proceso)

    def tick(self):

        # agregar procesos que llegaron
        for p in self.procesos:

            if p.estado == EstadoProceso.NUEVO and p.llegada <= self.tiempo_actual:

                p.estado = EstadoProceso.LISTO
                self.anillo_activos.insertar_proceso(p)


        if self.anillo_activos.esta_vacio():

            self.tiempo_actual += 1
            self.gantt.append("Idle")
            return


        proceso = self.anillo_activos.actual

        if proceso.tiempo_respuesta == -1:
            proceso.tiempo_respuesta = self.tiempo_actual - proceso.llegada


        proceso.estado = EstadoProceso.EJECUTANDO

        tiempo_ejecucion = min(self.quantum, proceso.burst_restante)

        for _ in range(tiempo_ejecucion):

            self.gantt.append(proceso.nombre)
            self.tiempo_actual += 1
            proceso.burst_restante -= 1

            if proceso.burst_restante == 0:
                break


        if proceso.burst_restante == 0:

            proceso.estado = EstadoProceso.TERMINADO
            proceso.tiempo_finalizacion = self.tiempo_actual

            self.procesos_terminados.append(proceso)

            self.anillo_activos.retirar_proceso(proceso.pid)

        else:

            proceso.estado = EstadoProceso.LISTO
            self.anillo_activos.rotar()

    def ejecutar_simulacion(self):

        while len(self.procesos_terminados) < len(self.procesos):

            self.tick()

    def calcular_metricas(self):

        total_turnaround = 0
        total_espera = 0
        total_respuesta = 0

        print("Proceso | Llegada | Fin | Turnaround | Espera")

        for p in self.procesos_terminados:

            turnaround = p.tiempo_finalizacion - p.llegada
            espera = turnaround - p.burst_total

            total_turnaround += turnaround
            total_espera += espera
            total_respuesta += p.tiempo_respuesta

            print(p.nombre, p.llegada, p.tiempo_finalizacion, turnaround, espera)

        n = len(self.procesos)

        print("\nPromedio turnaround:", total_turnaround / n)
        print("Promedio espera:", total_espera / n)
        print("Promedio respuesta:", total_respuesta / n)

    def gantt_chart(self):

        print("\nDIAGRAMA DE GANTT\n")

        tiempo = 0

        for proceso in self.gantt:
            print(f"|{proceso}", end="")
        print("|")

        for _ in self.gantt:
            print(f"{tiempo:2}", end=" ")
            tiempo += 1

        print()

