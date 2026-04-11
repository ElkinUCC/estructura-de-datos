from pydantic import BaseModel, Field


class EstanteCrear(BaseModel):
    nombre: str = Field(..., min_length=1)
    capacidad: int = Field(default=10, ge=1)


class CajaCrear(BaseModel):
    codigo: str = Field(..., min_length=1)
    descripcion: str = Field(..., min_length=1)
    cantidad: int = Field(..., ge=1)


class CajaResponse(BaseModel):
    codigo: str
    descripcion: str
    cantidad: int


class EstanteResponse(BaseModel):
    nombre: str
    capacidad: int
    cantidad: int


class EstanteDetalleResponse(EstanteResponse):
    cajas: list[CajaResponse]


class NodosResponse(BaseModel):
    nodos: str
