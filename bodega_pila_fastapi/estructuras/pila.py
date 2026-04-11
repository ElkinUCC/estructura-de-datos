from __future__ import annotations
from typing import Optional

class NodoCaja:
    def __init__(self, codigo: str, descripcion: str, cantidad: int, siguiente: Optional[NodoCaja] = None):
        self.codigo = codigo
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.siguiente = siguiente

    def __repr__(self) -> str:
        return f"Nodo({self.codigo})"

    def to_dict(self) -> dict[str, object]:
        return {
            "codigo": self.codigo,
            "descripcion": self.descripcion,
            "cantidad": self.cantidad,
        }


class PilaEstante:
    def __init__(self, nombre: str, capacidad: int = 10):
        self.nombre = nombre
        self.capacidad = capacidad
        self.tope: Optional[NodoCaja] = None
        self.cantidad = 0

    def es_vacia(self) -> bool:
        return self.tope is None

    def esta_llena(self) -> bool:
        return self.cantidad >= self.capacidad

    def push(self, caja: NodoCaja) -> None:
        if self.esta_llena():
            raise OverflowError("El estante está lleno")
        caja.siguiente = self.tope
        self.tope = caja
        self.cantidad += 1

    def pop(self) -> NodoCaja:
        if self.es_vacia():
            raise IndexError("El estante está vacío")
        nodo = self.tope
        assert nodo is not None
        self.tope = nodo.siguiente
        nodo.siguiente = None
        self.cantidad -= 1
        return nodo

    def peek(self) -> NodoCaja:
        if self.es_vacia():
            raise IndexError("El estante está vacío")
        assert self.tope is not None
        return self.tope

    def listar(self) -> list[dict[str, object]]:
        cajas: list[dict[str, object]] = []
        actual = self.tope
        while actual is not None:
            cajas.append(actual.to_dict())
            actual = actual.siguiente
        return cajas

    def nodos(self) -> str:
        partes: list[str] = []
        actual = self.tope
        while actual is not None:
            partes.append(repr(actual))
            actual = actual.siguiente
        partes.append("NULL")
        return " → ".join(partes)
