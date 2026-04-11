# Sistema de Inventario de Bodega - TransCarga S.A.S.

## Resumen del proyecto
Este es un WebService REST construido con FastAPI y Pydantic v2 para gestionar estantes de bodega como pilas LIFO.
Cada estante es una pila implementada con nodos enlazados propios y no se usan estructuras de Python como `list`, `deque` o `queue`.

## Estructura del código
- `bodega_pila_fastapi/estructuras/pila.py`
  - `NodoCaja` — nodo sencillo que guarda `codigo`, `descripcion`, `cantidad` y el enlace `siguiente`.
  - `PilaEstante` — pila enlazada que almacena cajas desde el `tope` hasta la base.
- `bodega_pila_fastapi/models.py` — modelos Pydantic para solicitudes y respuestas.
- `bodega_pila_fastapi/repo.py` — repositorio en memoria `_bodega` con CRUD básico de estantes.
- `bodega_pila_fastapi/main.py` — aplicación FastAPI con los endpoints requeridos.
- `requirements.txt` — dependencias del proyecto.

## Endpoints implementados
1. `POST /estantes`
   - Crea un nuevo estante.
   - Request body: `{"nombre": "A1", "capacidad": 10}`
   - Respuesta: `201 Created`
   - Error: `409 Conflict` si el estante ya existe.

2. `POST /estantes/{nombre}/push`
   - Inserta una caja en el tope de la pila del estante.
   - Request body: `{"codigo": "C001", "descripcion": "Zapatos", "cantidad": 5}`
   - Respuesta: `201 Created`
   - Error: `409 Conflict` si el estante está lleno.

3. `POST /estantes/{nombre}/pop`
   - Elimina la caja del tope y la devuelve.
   - Respuesta: `200 OK`
   - Error: `409 Conflict` si el estante está vacío.

4. `GET /estantes/{nombre}/peek`
   - Muestra la caja del tope sin quitarla.
   - Respuesta: `200 OK`
   - Error: `409 Conflict` si el estante está vacío.

5. `GET /estantes/{nombre}/cajas`
   - Lista las cajas del tope a la base.
   - Respuesta: `200 OK`

6. `GET /estantes`
   - Lista todos los estantes creados.
   - Respuesta: `200 OK`

7. `GET /estantes/{nombre}/nodos`
   - Muestra la cadena de nodos enlazados como `Nodo(C001) → Nodo(C002) → NULL`.
   - Respuesta: `200 OK`

## Reglas y restricciones cumplidas
- La pila está implementada con `NodoCaja` y `PilaEstante` en `estructuras/pila.py`.
- No se usa `list`, `deque`, `queue` ni colecciones externas para la estructura de la pila.
- `push()` lanza `OverflowError` convertido a `HTTP 409` cuando la pila está llena.
- `pop()` lanza `IndexError` convertido a `HTTP 409` cuando la pila está vacía.
- `listar()` devuelve las cajas en orden de tope a base, sin invertir el orden.
- El endpoint `/nodos` devuelve la representación `Nodo(X) → Nodo(Y) → NULL`.

## Cómo ejecutar el proyecto
1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Iniciar el servidor:
   ```bash
   uvicorn bodega_pila_fastapi.main:app --reload --port 8000
   ```
3. Abrir Swagger UI:
   - `http://localhost:8000/docs`

## Pruebas realizadas
- Creación de estante.
- Push de caja en estante.
- Pop de caja del estante.
- Peek de la caja del tope.
- Listado de cajas en orden de tope a base.
- Verificación del endpoint de nodos.

## Archivo disponible para descarga
- `FINAL_DOCUMENTACION.md`

## Notas finales
El proyecto ya está implementado en el workspace bajo la carpeta `bodega_pila_fastapi`.
Si necesitas, puedo también crear un archivo `bodega-pila-fastapi.zip` listo para entregar (sin `venv/` ni `__pycache__/`).
