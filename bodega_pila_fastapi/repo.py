from .estructuras.pila import NodoCaja, PilaEstante

_bodega: dict[str, PilaEstante] = {}


def crear_estante(nombre: str, capacidad: int = 10) -> PilaEstante:
    if nombre in _bodega:
        raise KeyError(f"El estante '{nombre}' ya existe")
    estante = PilaEstante(nombre=nombre, capacidad=capacidad)
    _bodega[nombre] = estante
    return estante


def obtener_estante(nombre: str) -> PilaEstante:
    if nombre not in _bodega:
        raise KeyError(f"El estante '{nombre}' no existe")
    return _bodega[nombre]


def listar_estantes() -> list[dict[str, object]]:
    return [
        {
            "nombre": estante.nombre,
            "capacidad": estante.capacidad,
            "cantidad": estante.cantidad,
        }
        for estante in _bodega.values()
    ]


def lista_de_estantes() -> list[str]:
    return list(_bodega.keys())
