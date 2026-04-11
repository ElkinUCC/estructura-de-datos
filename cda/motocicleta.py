from .vehiculo import Vehiculo

class Motocicleta(Vehiculo):
    tipo = "Motocicleta"
    
    def __init__(self, marca: str, modelo: str, anio: int):
        super().__init__(marca, modelo, anio, self.tipo)

    def mostrar_informacion(self) -> str:
        return f"{self.marca} {self.modelo} {self.tipo} ({self.anio})"