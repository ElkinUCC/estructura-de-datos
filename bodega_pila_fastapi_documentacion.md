# Sistema de Inventario de Bodega - TransCarga S.A.S.

## Descripción
Proyecto de inventario que modela estantes de bodega como pilas LIFO usando nodos enlazados propios.

## Estructura creada
- `bodega_pila_fastapi/estructuras/pila.py`
  - `NodoCaja`
  - `PilaEstante`
- `bodega_pila_fastapi/models.py`
- `bodega_pila_fastapi/repo.py`
- `bodega_pila_fastapi/main.py`
- `bodega_pila_fastapi/README.md`
- `requirements.txt`

## Endpoints disponibles
- `POST /estantes` — crear estante nuevo
- `POST /estantes/{nombre}/push` — apilar caja
- `POST /estantes/{nombre}/pop` — desapilar caja
- `GET /estantes/{nombre}/peek` — ver caja del tope
- `GET /estantes/{nombre}/cajas` — listar cajas de tope a base
- `GET /estantes` — listar estantes
- `GET /estantes/{nombre}/nodos` — mostrar nodos en cadena

## Reglas clave implementadas
- La pila no usa `list`, `deque` ni `queue`.
- `push()` arroja `HTTP 409` si el estante está lleno.
- `pop()` arroja `HTTP 409` si el estante está vacío.
- `listar()` devuelve las cajas del tope a la base.
- `/nodos` devuelve la cadena `Nodo(X) → Nodo(Y) → NULL`.

## Ejecución
```bash
pip install -r requirements.txt
uvicorn bodega_pila_fastapi.main:app --reload --port 8000
```

## Verificación
La implementación se validó con una prueba simple de `push`, `peek`, `listar` y `nodos` en el entorno local.
