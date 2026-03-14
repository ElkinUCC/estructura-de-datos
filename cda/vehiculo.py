class Vehiculo:
    def __init__(self, marca: str, modelo: str, anio: int, tipo: str):
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.tipo = tipo

def mostrar_informacion (self):
    return f"{self.marca} {self.modelo} {self.tipo} ({self.anio})"