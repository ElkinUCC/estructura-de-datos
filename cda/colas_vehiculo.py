class ColasVehiculo:

    def agregar_vehiculo(self, marca: str, modelo: str, anio: int, tipo: str):
        vehiculo = None
        if tipo == "Automóvil":
            vehiculo = Automovil(marca, modelo, anio)
        elif tipo == "Motocicleta":
            vehiculo = Motocicleta(marca, modelo, anio)

    def despachar_vehiculo (self):
        pass

    def mostrar_vehiculo (self):
        pass