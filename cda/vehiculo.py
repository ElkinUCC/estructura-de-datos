class Vehiculo:
    def __init__(self, marca: str, modelo: str, anio: int, tipo: str):
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.tipo = tipo
        self.estado = "En espera"
        self.resultado_prueba = None
        self.fecha_ingreso = None
        self.fecha_despacho = None

    def mostrar_informacion(self):
        return f"{self.marca} {self.modelo} {self.tipo} ({self.anio})"

    def __str__(self):
        return self.mostrar_informacion()

    def __repr__(self):
        return f"Vehiculo({self.marca}, {self.modelo}, {self.anio}, {self.tipo})"