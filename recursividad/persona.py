class Persona: 
    nombre: str
    edad: int
    peso: float
    altura: float
    
    def __init__(self, n: str, e: int, p: float, a: float):
        self.nombre = n
        self.edad = e
        self.peso = p
        self.altura = a

    def caminar(self, distancia: float) -> bool:
        
        if 30 <= self.edad <= 40:
            max_km = 20
        elif self.edad > 40:
            max_km = 10
        else:
            return distancia > 20
        return distancia <= max_km
    
persona1 = Persona("Juan", 15, 70.5, 1.75)
print(persona1.caminar(15))  # True