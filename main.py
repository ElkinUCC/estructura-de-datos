from fastapi import FastAPI
from calculadora import Multiplicacion, suma
from cda import ColasVehiculo

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World", "mensaje": "Bienvenido a la API"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get ("/suma/{a}/{b}")
def sumar (a: int, b: int):
    resultado = suma(a, b)
    return {"resultado": resultado}

@app.get("/multiplicacion/{a}/{b}")
def multiplicar(a: int, b: int):
    resultado = a * b
    return {"resultado": resultado}

@app.post("/registrar_vehiculo/")
def registrar_vehiculo(marca: str, modelo: str, anio: int, tipo: str):
    colas_vehiculo = ColasVehiculo()
    vehiculo = colas_vehiculo.agregar_vehiculo(marca, modelo, anio, tipo)
    return {"vehiculo": vehiculo}

@app.get("/despachar_vehiculo/")
def despachar_vehiculo():
    colas_vehiculo = ColasVehiculo()
    vehiculo_despachado = colas_vehiculo.despachar_vehiculo()
    return {"vehiculo_despachado": vehiculo_despachado}