# Sistema de Inventario de Bodega - TransCarga S.A.S.

Este proyecto implementa un WebService REST con FastAPI para gestionar estantes de bodega como pilas LIFO construidas con nodos enlazados.

## Estructura
- `bodega_pila_fastapi/estructuras/pila.py`
  - `NodoCaja` — nodo que guarda la información de una caja.
  - `PilaEstante` — pila enlazada que representa un estante.
- `bodega_pila_fastapi/models.py` — modelos Pydantic para validación.
- `bodega_pila_fastapi/repo.py` — repositorio en memoria de estantes.
- `bodega_pila_fastapi/main.py` — aplicación FastAPI.

## Endpoints
- `POST /estantes` — crea un estante nuevo.
- `POST /estantes/{nombre}/push` — apila una caja en el estante.
- `POST /estantes/{nombre}/pop` — desapila la caja del tope.
- `GET /estantes/{nombre}/peek` — muestra la caja del tope sin quitarla.
- `GET /estantes/{nombre}/cajas` — lista las cajas del tope a la base.
- `GET /estantes` — lista los estantes creados.
- `GET /estantes/{nombre}/nodos` — muestra la cadena de nodos como `Nodo(X) → Nodo(Y) → NULL`.

## Ejecución
```bash
pip install -r requirements.txt
uvicorn bodega_pila_fastapi.main:app --reload --port 8000
```

Swagger UI disponible en `http://localhost:8000/docs`.

## Validaciones importantes
- La pila no usa `list`, `deque` ni `queue` para su implementación.
- `push()` lanza HTTP 409 cuando el estante está lleno.
- `pop()` lanza HTTP 409 cuando el estante está vacío.
- `listar()` devuelve las cajas en orden de tope a base.
- El endpoint `/nodos` devuelve `Nodo(...) → ... → NULL`.
