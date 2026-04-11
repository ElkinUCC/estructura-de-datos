from fastapi import FastAPI, HTTPException, status
from .models import (
    CajaCrear,
    CajaResponse,
    EstanteCrear,
    EstanteDetalleResponse,
    EstanteResponse,
    NodosResponse,
)
from .repo import crear_estante, listar_estantes, obtener_estante
from .estructuras.pila import NodoCaja

app = FastAPI(
    title="Inventario de Bodega TransCarga",
    description="WebService FastAPI que gestiona estantes como pilas LIFO con nodos enlazados.",
    version="1.0.0",
)


@app.post("/estantes", response_model=EstanteResponse, status_code=status.HTTP_201_CREATED)
def crear_nuevo_estante(estante: EstanteCrear) -> EstanteResponse:
    try:
        creado = crear_estante(estante.nombre, estante.capacidad)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))
    return EstanteResponse(
        nombre=creado.nombre,
        capacidad=creado.capacidad,
        cantidad=creado.cantidad,
    )


@app.post("/estantes/{nombre}/push", response_model=CajaResponse, status_code=status.HTTP_201_CREATED)
def push_caja(nombre: str, caja: CajaCrear) -> CajaResponse:
    try:
        estante = obtener_estante(nombre)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))

    try:
        nodo = NodoCaja(codigo=caja.codigo, descripcion=caja.descripcion, cantidad=caja.cantidad)
        estante.push(nodo)
    except OverflowError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))

    return CajaResponse(codigo=nodo.codigo, descripcion=nodo.descripcion, cantidad=nodo.cantidad)


@app.post("/estantes/{nombre}/pop", response_model=CajaResponse)
def pop_caja(nombre: str) -> CajaResponse:
    try:
        estante = obtener_estante(nombre)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))

    try:
        eliminado = estante.pop()
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))

    return CajaResponse(codigo=eliminado.codigo, descripcion=eliminado.descripcion, cantidad=eliminado.cantidad)


@app.get("/estantes/{nombre}/peek", response_model=CajaResponse)
def peek_caja(nombre: str) -> CajaResponse:
    try:
        estante = obtener_estante(nombre)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))

    try:
        caja = estante.peek()
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))

    return CajaResponse(codigo=caja.codigo, descripcion=caja.descripcion, cantidad=caja.cantidad)


@app.get("/estantes/{nombre}/cajas", response_model=EstanteDetalleResponse)
def listar_cajas(nombre: str) -> EstanteDetalleResponse:
    try:
        estante = obtener_estante(nombre)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))

    return EstanteDetalleResponse(
        nombre=estante.nombre,
        capacidad=estante.capacidad,
        cantidad=estante.cantidad,
        cajas=[CajaResponse(**caja) for caja in estante.listar()],
    )


@app.get("/estantes", response_model=list[EstanteResponse])
def obtener_estantes() -> list[EstanteResponse]:
    return [EstanteResponse(**estante) for estante in listar_estantes()]


@app.get("/estantes/{nombre}/nodos", response_model=NodosResponse)
def ver_nodos(nombre: str) -> NodosResponse:
    try:
        estante = obtener_estante(nombre)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))

    return NodosResponse(nodos=estante.nodos())
