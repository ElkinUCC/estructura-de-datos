from datetime import datetime
from .nodo import Nodo
from .automovil import Automovil
from .motocicleta import Motocicleta

class ColasVehiculo:
    """
    Clase que gestiona la cola de vehículos en el CDA.
    Implementa operaciones FIFO (First In First Out) para el procesamiento de vehículos.
    """
    
    def __init__(self):
        self.inicio = None  # Primer vehículo en la cola
        self.fin = None     # Último vehículo en la cola
        self.vehiculos_procesados = []  # Vehículos que han sido despachados
        self.vehiculos_retirados = []   # Vehículos retirados
        self.total_vehiculos = 0

    def agregar_vehiculo(self, marca: str, modelo: str, anio: int, tipo: str):
        """
        Agrega un nuevo vehículo a la cola.
        
        :param marca: Marca del vehículo
        :param modelo: Modelo del vehículo
        :param anio: Año del vehículo
        :param tipo: Tipo del vehículo (Automóvil o Motocicleta)
        :return: El vehículo creado o None si el tipo no es válido
        """
        vehiculo = None
        
        if tipo == "Automóvil":
            vehiculo = Automovil(marca, modelo, anio)
        elif tipo == "Motocicleta":
            vehiculo = Motocicleta(marca, modelo, anio)
        else:
            return None
        
        # Asignar fecha de ingreso
        vehiculo.fecha_ingreso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        vehiculo.estado = "En espera"
        
        # Crear nodo y agregarlo a la cola
        nodo = Nodo(vehiculo)
        
        if self.inicio is None:
            self.inicio = nodo
            self.fin = nodo
        else:
            self.fin.siguiente = nodo
            self.fin = nodo
        
        self.total_vehiculos += 1
        return vehiculo

    def despachar_vehiculo(self):
        """
        Despecha el primer vehículo de la cola.
        
        :return: El vehículo despachado o None si la cola está vacía
        """
        if self.inicio is None:
            return None
        
        nodo = self.inicio
        vehiculo = nodo.dato
        
        # Mover al siguiente vehículo
        self.inicio = self.inicio.siguiente
        
        if self.inicio is None:
            self.fin = None
        
        # Marcar como despachado
        vehiculo.estado = "Despachado"
        vehiculo.fecha_despacho = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.vehiculos_procesados.append(vehiculo)
        self.total_vehiculos -= 1
        
        return vehiculo

    def retirar_vehiculo(self, marca: str, modelo: str):
        """
        Permite que un cliente retire su vehículo antes de la revisión.
        
        :param marca: Marca del vehículo a retirar
        :param modelo: Modelo del vehículo a retirar
        :return: El vehículo retirado o None si no se encuentra
        """
        if self.inicio is None:
            return None
        
        # Caso especial: si es el primer vehículo
        if (self.inicio.dato.marca == marca and 
            self.inicio.dato.modelo == modelo):
            vehiculo = self.inicio.dato
            self.inicio = self.inicio.siguiente
            if self.inicio is None:
                self.fin = None
            vehiculo.estado = "Retirado"
            self.vehiculos_retirados.append(vehiculo)
            self.total_vehiculos -= 1
            return vehiculo
        
        # Buscar en el resto de la cola
        nodo_anterior = self.inicio
        nodo_actual = self.inicio.siguiente
        
        while nodo_actual is not None:
            if (nodo_actual.dato.marca == marca and 
                nodo_actual.dato.modelo == modelo):
                vehiculo = nodo_actual.dato
                nodo_anterior.siguiente = nodo_actual.siguiente
                
                if nodo_actual == self.fin:
                    self.fin = nodo_anterior
                
                vehiculo.estado = "Retirado"
                self.vehiculos_retirados.append(vehiculo)
                self.total_vehiculos -= 1
                return vehiculo
            
            nodo_anterior = nodo_actual
            nodo_actual = nodo_actual.siguiente
        
        return None

    def agregar_resultado_prueba(self, marca: str, modelo: str, resultado: str, observaciones: str = ""):
        """
        Agrega el resultado de las pruebas a un vehículo.
        
        :param marca: Marca del vehículo
        :param modelo: Modelo del vehículo
        :param resultado: Resultado de la prueba (APROBADO o REPROBADO)
        :param observaciones: Observaciones adicionales
        """
        nodo = self.inicio
        while nodo is not None:
            if (nodo.dato.marca == marca and 
                nodo.dato.modelo == modelo):
                nodo.dato.resultado_prueba = {
                    "estado": resultado,
                    "observaciones": observaciones,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                nodo.dato.estado = "Revisado"
                return nodo.dato
            nodo = nodo.siguiente
        return None

    def mostrar_vehiculo(self):
        """
        Muestra el primer vehículo de la cola.
        
        :return: Información del primer vehículo o None si la cola está vacía
        """
        if self.inicio is None:
            return None
        return self.inicio.dato

    def mostrar_todos_vehiculos(self):
        """
        Retorna una lista de todos los vehículos en la cola.
        
        :return: Lista con información de todos los vehículos
        """
        vehiculos = []
        nodo = self.inicio
        while nodo is not None:
            vehiculos.append(nodo.dato)
            nodo = nodo.siguiente
        return vehiculos

    def cantidad_vehiculos_operacion(self):
        """
        Retorna la cantidad de vehículos en operación (en la cola).
        
        :return: Número de vehículos esperando procesamiento
        """
        return self.total_vehiculos

    def reportar_vehiculos_revisados_hoy(self):
        """
        Retorna los vehículos que han sido revisados hoy.
        
        :return: Lista de vehículos con resultado de prueba
        """
        hoy = datetime.now().strftime("%Y-%m-%d")
        revisados = []
        
        for vehiculo in self.vehiculos_procesados:
            if (vehiculo.resultado_prueba and 
                hoy in vehiculo.resultado_prueba["fecha"]):
                revisados.append(vehiculo)
        
        return revisados

    def limpiar_cola(self):
        """
        Limpia la cola de vehículos.
        """
        self.inicio = None
        self.fin = None
        self.total_vehiculos = 0

    def __str__(self):
        resultados = []
        nodo = self.inicio
        while nodo is not None:
            resultados.append(str(nodo.dato))
            nodo = nodo.siguiente
        return "[" + ", ".join(resultados) + "]"