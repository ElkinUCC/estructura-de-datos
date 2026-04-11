# 📋 CÓDIGO COMPLETO DEL SISTEMA CDA

## Sistema de Recepción y Despacho de Vehículos

Documento generado el: **11 de Abril de 2026**

---

## 📑 Tabla de Contenidos

1. [vehiculo.py](#vehiculopy) - Clase Base
2. [nodo.py](#nodopy) - Estructura de Datos Enlazada
3. [automovil.py](#automovilst) - Clase Especializada
4. [motocicleta.py](#motocicletapy) - Clase Especializada
5. [colas_vehiculo.py](#colas_vehiculopy) - Gestor de Cola FIFO
6. [api_cda.py](#api_cdapy) - Servicio Web REST
7. [__init__.py](#__init__py) - Módulo
8. [Requisitos de Instalación](#requisitos-de-instalación)
9. [Documentación de Rutas API](#documentación-de-rutas-api)

---

## `vehiculo.py`

Clase base que define la estructura de todos los vehículos en el sistema.

```python
class Vehiculo:
    def __init__(self, marca: str, modelo: str, anio: int, tipo: str):
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.tipo = tipo
        self.estado = "En espera"
        self.resultado_prueba = None
        self.fecha_ingreso = None
        self.fecha_despacho = None

    def mostrar_informacion(self):
        return f"{self.marca} {self.modelo} {self.tipo} ({self.anio})"

    def __str__(self):
        return self.mostrar_informacion()

    def __repr__(self):
        return f"Vehiculo({self.marca}, {self.modelo}, {self.anio}, {self.tipo})"
```

**Atributos:**
- `marca`: Marca del vehículo
- `modelo`: Modelo del vehículo
- `anio`: Año de fabricación
- `tipo`: Tipo de vehículo
- `estado`: Estado actual (En espera, Revisado, Despachado, Retirado)
- `resultado_prueba`: Diccionario con resultado de pruebas
- `fecha_ingreso`: Fecha de ingreso al sistema
- `fecha_despacho`: Fecha de salida del sistema

---

## `nodo.py`

Implementación de nodo para estructura de datos enlazada.

```python
class Nodo:
    """
    Clase que representa un nodo en una estructura de datos enlazada.
    Cada nodo contiene datos y una referencia al siguiente nodo.
    """

    def __init__(self, dato):
        """
        Inicializa un nuevo nodo con el dato proporcionado.

        :param dato: El dato que almacenará el nodo.
        """
        self.dato = dato
        self.siguiente = None

    def __str__(self):
        """
        Devuelve una representación en cadena del nodo.

        :return: Cadena que representa el dato del nodo.
        """
        return str(self.dato)

    def __repr__(self):
        """
        Devuelve una representación detallada del nodo para depuración.

        :return: Cadena que representa el nodo con su dato.
        """
        return f"Nodo({self.dato})"
```

**Propósito:** Forma la base de la estructura de cola FIFO que mantiene los vehículos en orden de llegada.

---

## `automovil.py`

Especialización de la clase Vehiculo para automóviles.

```python
from .vehiculo import Vehiculo

class Automovil(Vehiculo):
    tipo = "Automóvil"
    
    def __init__(self, marca: str, modelo: str, anio: int):
        super().__init__(marca, modelo, anio, self.tipo)

    def mostrar_informacion(self) -> str:
        return f"{self.marca} {self.modelo} {self.tipo} ({self.anio})"
```

**Características:**
- Hereda de `Vehiculo`
- Tipo automáticamente establecido como "Automóvil"
- Requiere marca, modelo y año

---

## `motocicleta.py`

Especialización de la clase Vehiculo para motocicletas.

```python
from .vehiculo import Vehiculo

class Motocicleta(Vehiculo):
    tipo = "Motocicleta"
    
    def __init__(self, marca: str, modelo: str, anio: int):
        super().__init__(marca, modelo, anio, self.tipo)

    def mostrar_informacion(self) -> str:
        return f"{self.marca} {self.modelo} {self.tipo} ({self.anio})"
```

**Características:**
- Hereda de `Vehiculo`
- Tipo automáticamente establecido como "Motocicleta"
- Requiere marca, modelo y año

---

## `colas_vehiculo.py`

Gestor principal de la cola de vehículos utilizando estructura FIFO.

```python
from datetime import datetime
from .nodo import Nodo
from .automovil import Automovil
from .motocicleta import Motocicleta

class ColasVehiculo:
    """
    Clase que gestiona la cola de vehículos en el CDA.
    Implementa operaciones FIFO (First In First Out) para el procesamiento de vehículos.
    """
    
    def __init__(self):
        self.inicio = None  # Primer vehículo en la cola
        self.fin = None     # Último vehículo en la cola
        self.vehiculos_procesados = []  # Vehículos que han sido despachados
        self.vehiculos_retirados = []   # Vehículos retirados
        self.total_vehiculos = 0

    def agregar_vehiculo(self, marca: str, modelo: str, anio: int, tipo: str):
        """
        Agrega un nuevo vehículo a la cola.
        
        :param marca: Marca del vehículo
        :param modelo: Modelo del vehículo
        :param anio: Año del vehículo
        :param tipo: Tipo del vehículo (Automóvil o Motocicleta)
        :return: El vehículo creado o None si el tipo no es válido
        """
        vehiculo = None
        
        if tipo == "Automóvil":
            vehiculo = Automovil(marca, modelo, anio)
        elif tipo == "Motocicleta":
            vehiculo = Motocicleta(marca, modelo, anio)
        else:
            return None
        
        # Asignar fecha de ingreso
        vehiculo.fecha_ingreso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        vehiculo.estado = "En espera"
        
        # Crear nodo y agregarlo a la cola
        nodo = Nodo(vehiculo)
        
        if self.inicio is None:
            self.inicio = nodo
            self.fin = nodo
        else:
            self.fin.siguiente = nodo
            self.fin = nodo
        
        self.total_vehiculos += 1
        return vehiculo

    def despachar_vehiculo(self):
        """
        Despecha el primer vehículo de la cola.
        
        :return: El vehículo despachado o None si la cola está vacía
        """
        if self.inicio is None:
            return None
        
        nodo = self.inicio
        vehiculo = nodo.dato
        
        # Mover al siguiente vehículo
        self.inicio = self.inicio.siguiente
        
        if self.inicio is None:
            self.fin = None
        
        # Marcar como despachado
        vehiculo.estado = "Despachado"
        vehiculo.fecha_despacho = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.vehiculos_procesados.append(vehiculo)
        self.total_vehiculos -= 1
        
        return vehiculo

    def retirar_vehiculo(self, marca: str, modelo: str):
        """
        Permite que un cliente retire su vehículo antes de la revisión.
        
        :param marca: Marca del vehículo a retirar
        :param modelo: Modelo del vehículo a retirar
        :return: El vehículo retirado o None si no se encuentra
        """
        if self.inicio is None:
            return None
        
        # Caso especial: si es el primer vehículo
        if (self.inicio.dato.marca == marca and 
            self.inicio.dato.modelo == modelo):
            vehiculo = self.inicio.dato
            self.inicio = self.inicio.siguiente
            if self.inicio is None:
                self.fin = None
            vehiculo.estado = "Retirado"
            self.vehiculos_retirados.append(vehiculo)
            self.total_vehiculos -= 1
            return vehiculo
        
        # Buscar en el resto de la cola
        nodo_anterior = self.inicio
        nodo_actual = self.inicio.siguiente
        
        while nodo_actual is not None:
            if (nodo_actual.dato.marca == marca and 
                nodo_actual.dato.modelo == modelo):
                vehiculo = nodo_actual.dato
                nodo_anterior.siguiente = nodo_actual.siguiente
                
                if nodo_actual == self.fin:
                    self.fin = nodo_anterior
                
                vehiculo.estado = "Retirado"
                self.vehiculos_retirados.append(vehiculo)
                self.total_vehiculos -= 1
                return vehiculo
            
            nodo_anterior = nodo_actual
            nodo_actual = nodo_actual.siguiente
        
        return None

    def agregar_resultado_prueba(self, marca: str, modelo: str, resultado: str, observaciones: str = ""):
        """
        Agrega el resultado de las pruebas a un vehículo.
        
        :param marca: Marca del vehículo
        :param modelo: Modelo del vehículo
        :param resultado: Resultado de la prueba (APROBADO o REPROBADO)
        :param observaciones: Observaciones adicionales
        """
        nodo = self.inicio
        while nodo is not None:
            if (nodo.dato.marca == marca and 
                nodo.dato.modelo == modelo):
                nodo.dato.resultado_prueba = {
                    "estado": resultado,
                    "observaciones": observaciones,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                nodo.dato.estado = "Revisado"
                return nodo.dato
            nodo = nodo.siguiente
        return None

    def mostrar_vehiculo(self):
        """
        Muestra el primer vehículo de la cola.
        
        :return: Información del primer vehículo o None si la cola está vacía
        """
        if self.inicio is None:
            return None
        return self.inicio.dato

    def mostrar_todos_vehiculos(self):
        """
        Retorna una lista de todos los vehículos en la cola.
        
        :return: Lista con información de todos los vehículos
        """
        vehiculos = []
        nodo = self.inicio
        while nodo is not None:
            vehiculos.append(nodo.dato)
            nodo = nodo.siguiente
        return vehiculos

    def cantidad_vehiculos_operacion(self):
        """
        Retorna la cantidad de vehículos en operación (en la cola).
        
        :return: Número de vehículos esperando procesamiento
        """
        return self.total_vehiculos

    def reportar_vehiculos_revisados_hoy(self):
        """
        Retorna los vehículos que han sido revisados hoy.
        
        :return: Lista de vehículos con resultado de prueba
        """
        hoy = datetime.now().strftime("%Y-%m-%d")
        revisados = []
        
        for vehiculo in self.vehiculos_procesados:
            if (vehiculo.resultado_prueba and 
                hoy in vehiculo.resultado_prueba["fecha"]):
                revisados.append(vehiculo)
        
        return revisados

    def limpiar_cola(self):
        """
        Limpia la cola de vehículos.
        """
        self.inicio = None
        self.fin = None
        self.total_vehiculos = 0

    def __str__(self):
        resultados = []
        nodo = self.inicio
        while nodo is not None:
            resultados.append(str(nodo.dato))
            nodo = nodo.siguiente
        return "[" + ", ".join(resultados) + "]"
```

**Métodos Principales:**
1. `agregar_vehiculo()` - Registra un nuevo vehículo
2. `despachar_vehiculo()` - Retira el primer vehículo de la cola
3. `retirar_vehiculo()` - Permite retiro antes de revisión
4. `agregar_resultado_prueba()` - Registra resultados de pruebas
5. `mostrar_todos_vehiculos()` - Lista todos los vehículos
6. `cantidad_vehiculos_operacion()` - Cuenta vehículos activos
7. `reportar_vehiculos_revisados_hoy()` - Reporta revisiones del día

---

## `api_cda.py`

Servicio web REST con Flask para interactuar con el sistema.

```python
"""
API REST para el sistema de gestión de vehículos en CDA
Desarrollado con Flask
"""

from flask import Flask, request, jsonify
from datetime import datetime
from .colas_vehiculo import ColasVehiculo

app = Flask(__name__)

# Instancia global del gestor de colas
cola_vehiculos = ColasVehiculo()

# RUTAS DE LA API

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifica el estado del servidor"""
    return jsonify({
        "estado": "OK",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "servicio": "CDA - Sistema de Recepción y Despacho de Vehículos"
    }), 200


@app.route('/api/vehiculos/registrar', methods=['POST'])
def registrar_vehiculo():
    """
    Registra un nuevo vehículo en el sistema.
    
    JSON requerido:
    {
        "marca": "Chevrolet",
        "modelo": "Tracker",
        "anio": 2020,
        "tipo": "Automóvil"
    }
    """
    try:
        datos = request.get_json()
        
        # Validar datos requeridos
        if not all(k in datos for k in ['marca', 'modelo', 'anio', 'tipo']):
            return jsonify({
                "error": "Faltan campos requeridos",
                "campos_requeridos": ["marca", "modelo", "anio", "tipo"]
            }), 400
        
        # Registrar vehículo
        vehiculo = cola_vehiculos.agregar_vehiculo(
            datos['marca'],
            datos['modelo'],
            datos['anio'],
            datos['tipo']
        )
        
        if vehiculo is None:
            return jsonify({
                "error": "Tipo de vehículo no válido",
                "tipos_permitidos": ["Automóvil", "Motocicleta"]
            }), 400
        
        return jsonify({
            "mensaje": "Vehículo registrado exitosamente",
            "vehiculo": {
                "marca": vehiculo.marca,
                "modelo": vehiculo.modelo,
                "anio": vehiculo.anio,
                "tipo": vehiculo.tipo,
                "estado": vehiculo.estado,
                "fecha_ingreso": vehiculo.fecha_ingreso
            }
        }), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/vehiculos/despachar', methods=['POST'])
def despachar_vehiculo():
    """
    Despache el primer vehículo de la cola.
    """
    try:
        vehiculo = cola_vehiculos.despachar_vehiculo()
        
        if vehiculo is None:
            return jsonify({
                "error": "No hay vehículos en la cola para despachar"
            }), 404
        
        return jsonify({
            "mensaje": "Vehículo despachado exitosamente",
            "vehiculo": {
                "marca": vehiculo.marca,
                "modelo": vehiculo.modelo,
                "anio": vehiculo.anio,
                "tipo": vehiculo.tipo,
                "estado": vehiculo.estado,
                "fecha_despacho": vehiculo.fecha_despacho,
                "resultado_prueba": vehiculo.resultado_prueba
            }
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/vehiculos/retirar', methods=['POST'])
def retirar_vehiculo():
    """
    Permite que un cliente retire su vehículo antes de la revisión.
    
    JSON requerido:
    {
        "marca": "Chevrolet",
        "modelo": "Tracker"
    }
    """
    try:
        datos = request.get_json()
        
        if not all(k in datos for k in ['marca', 'modelo']):
            return jsonify({
                "error": "Faltan campos requeridos",
                "campos_requeridos": ["marca", "modelo"]
            }), 400
        
        vehiculo = cola_vehiculos.retirar_vehiculo(datos['marca'], datos['modelo'])
        
        if vehiculo is None:
            return jsonify({
                "error": "Vehículo no encontrado en la cola"
            }), 404
        
        return jsonify({
            "mensaje": "Vehículo retirado exitosamente",
            "vehiculo": {
                "marca": vehiculo.marca,
                "modelo": vehiculo.modelo,
                "anio": vehiculo.anio,
                "tipo": vehiculo.tipo,
                "estado": vehiculo.estado
            }
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/vehiculos/agregar-resultado', methods=['POST'])
def agregar_resultado_prueba():
    """
    Agrega el resultado de las pruebas a un vehículo.
    
    JSON requerido:
    {
        "marca": "Chevrolet",
        "modelo": "Tracker",
        "resultado": "APROBADO",
        "observaciones": "Vehículo en buen estado"
    }
    """
    try:
        datos = request.get_json()
        
        if not all(k in datos for k in ['marca', 'modelo', 'resultado']):
            return jsonify({
                "error": "Faltan campos requeridos",
                "campos_requeridos": ["marca", "modelo", "resultado"]
            }), 400
        
        observaciones = datos.get('observaciones', '')
        
        vehiculo = cola_vehiculos.agregar_resultado_prueba(
            datos['marca'],
            datos['modelo'],
            datos['resultado'],
            observaciones
        )
        
        if vehiculo is None:
            return jsonify({
                "error": "Vehículo no encontrado en la cola"
            }), 404
        
        return jsonify({
            "mensaje": "Resultado de prueba registrado exitosamente",
            "vehiculo": {
                "marca": vehiculo.marca,
                "modelo": vehiculo.modelo,
                "resultado": vehiculo.resultado_prueba
            }
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/operacion/cantidad', methods=['GET'])
def cantidad_vehiculos_operacion():
    """
    Retorna la cantidad de vehículos que hay en operación.
    """
    try:
        cantidad = cola_vehiculos.cantidad_vehiculos_operacion()
        
        return jsonify({
            "cantidad_vehiculos_en_operacion": cantidad,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/reportes/revisados-hoy', methods=['GET'])
def reportar_vehiculos_revisados():
    """
    Retorna los vehículos revisados en el día.
    """
    try:
        revisados = cola_vehiculos.reportar_vehiculos_revisados_hoy()
        
        vehiculos_info = []
        for v in revisados:
            vehiculos_info.append({
                "marca": v.marca,
                "modelo": v.modelo,
                "anio": v.anio,
                "tipo": v.tipo,
                "resultado": v.resultado_prueba["estado"],
                "observaciones": v.resultado_prueba["observaciones"],
                "fecha": v.resultado_prueba["fecha"]
            })
        
        return jsonify({
            "total_revisados": len(revisados),
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "vehiculos": vehiculos_info
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/vehiculos/lista', methods=['GET'])
def listar_vehiculos():
    """
    Retorna la lista de todos los vehículos en la cola.
    """
    try:
        vehiculos = cola_vehiculos.mostrar_todos_vehiculos()
        
        vehiculos_info = []
        for v in vehiculos:
            vehiculos_info.append({
                "marca": v.marca,
                "modelo": v.modelo,
                "anio": v.anio,
                "tipo": v.tipo,
                "estado": v.estado,
                "fecha_ingreso": v.fecha_ingreso
            })
        
        return jsonify({
            "total": len(vehiculos_info),
            "vehiculos": vehiculos_info
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/vehiculos/proximo', methods=['GET'])
def proximo_vehiculo():
    """
    Retorna el próximo vehículo a ser procesado.
    """
    try:
        vehiculo = cola_vehiculos.mostrar_vehiculo()
        
        if vehiculo is None:
            return jsonify({
                "error": "No hay vehículos en la cola"
            }), 404
        
        return jsonify({
            "vehiculo": {
                "marca": vehiculo.marca,
                "modelo": vehiculo.modelo,
                "anio": vehiculo.anio,
                "tipo": vehiculo.tipo,
                "estado": vehiculo.estado,
                "fecha_ingreso": vehiculo.fecha_ingreso
            }
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def no_encontrado(error):
    """Maneja errores 404"""
    return jsonify({
        "error": "Recurso no encontrado",
        "codigo": 404
    }), 404


@app.errorhandler(500)
def error_interno(error):
    """Maneja errores 500"""
    return jsonify({
        "error": "Error interno del servidor",
        "codigo": 500
    }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

---

## `__init__.py`

```python
from .colas_vehiculo import ColasVehiculo
```

---

## Requisitos de Instalación

**Dependencias necesarias:**

```
Flask==2.3.0
```

**Instalación:**

```bash
pip install Flask
```

---

## Documentación de Rutas API

### 1. **Health Check**
```
GET /api/health
```
**Descripción:** Verifica el estado del servidor

**Respuesta:**
```json
{
    "estado": "OK",
    "timestamp": "2026-04-11 10:30:45",
    "servicio": "CDA - Sistema de Recepción y Despacho de Vehículos"
}
```

---

### 2. **Registrar Vehículo**
```
POST /api/vehiculos/registrar
```
**Descripción:** Registra un nuevo vehículo en la cola

**Request:**
```json
{
    "marca": "Chevrolet",
    "modelo": "Tracker",
    "anio": 2020,
    "tipo": "Automóvil"
}
```

**Respuesta:**
```json
{
    "mensaje": "Vehículo registrado exitosamente",
    "vehiculo": {
        "marca": "Chevrolet",
        "modelo": "Tracker",
        "anio": 2020,
        "tipo": "Automóvil",
        "estado": "En espera",
        "fecha_ingreso": "2026-04-11 10:30:45"
    }
}
```

---

### 3. **Despachar Vehículo**
```
POST /api/vehiculos/despachar
```
**Descripción:** Retira el primer vehículo de la cola y lo marca como despachado

**Respuesta:**
```json
{
    "mensaje": "Vehículo despachado exitosamente",
    "vehiculo": {
        "marca": "Chevrolet",
        "modelo": "Tracker",
        "anio": 2020,
        "tipo": "Automóvil",
        "estado": "Despachado",
        "fecha_despacho": "2026-04-11 11:00:00",
        "resultado_prueba": {
            "estado": "APROBADO",
            "observaciones": "Vehículo en buen estado",
            "fecha": "2026-04-11 10:45:00"
        }
    }
}
```

---

### 4. **Retirar Vehículo**
```
POST /api/vehiculos/retirar
```
**Descripción:** Permite a un cliente retirar su vehículo antes de la revisión

**Request:**
```json
{
    "marca": "Chevrolet",
    "modelo": "Tracker"
}
```

**Respuesta:**
```json
{
    "mensaje": "Vehículo retirado exitosamente",
    "vehiculo": {
        "marca": "Chevrolet",
        "modelo": "Tracker",
        "anio": 2020,
        "tipo": "Automóvil",
        "estado": "Retirado"
    }
}
```

---

### 5. **Agregar Resultado de Prueba**
```
POST /api/vehiculos/agregar-resultado
```
**Descripción:** Registra el resultado de las pruebas de un vehículo

**Request:**
```json
{
    "marca": "Chevrolet",
    "modelo": "Tracker",
    "resultado": "APROBADO",
    "observaciones": "Motor y sistema de frenos en perfecto estado"
}
```

**Respuesta:**
```json
{
    "mensaje": "Resultado de prueba registrado exitosamente",
    "vehiculo": {
        "marca": "Chevrolet",
        "modelo": "Tracker",
        "resultado": {
            "estado": "APROBADO",
            "observaciones": "Motor y sistema de frenos en perfecto estado",
            "fecha": "2026-04-11 10:45:00"
        }
    }
}
```

---

### 6. **Cantidad de Vehículos en Operación**
```
GET /api/operacion/cantidad
```
**Descripción:** Retorna el número de vehículos esperando procesamiento

**Respuesta:**
```json
{
    "cantidad_vehiculos_en_operacion": 5,
    "timestamp": "2026-04-11 10:30:45"
}
```

---

### 7. **Reportar Vehículos Revisados Hoy**
```
GET /api/reportes/revisados-hoy
```
**Descripción:** Retorna todos los vehículos que han sido revisados en el día actual

**Respuesta:**
```json
{
    "total_revisados": 3,
    "fecha": "2026-04-11",
    "vehiculos": [
        {
            "marca": "Chevrolet",
            "modelo": "Tracker",
            "anio": 2020,
            "tipo": "Automóvil",
            "resultado": "APROBADO",
            "observaciones": "Vehículo en buen estado",
            "fecha": "2026-04-11 10:45:00"
        },
        {
            "marca": "Honda",
            "modelo": "XRE 300",
            "anio": 2023,
            "tipo": "Motocicleta",
            "resultado": "APROBADO",
            "observaciones": "Revisión exitosa",
            "fecha": "2026-04-11 11:15:00"
        }
    ]
}
```

---

### 8. **Listar Todos los Vehículos**
```
GET /api/vehiculos/lista
```
**Descripción:** Retorna la lista completa de vehículos en la cola

**Respuesta:**
```json
{
    "total": 2,
    "vehiculos": [
        {
            "marca": "Toyota",
            "modelo": "Corolla",
            "anio": 2021,
            "tipo": "Automóvil",
            "estado": "En espera",
            "fecha_ingreso": "2026-04-11 09:00:00"
        }
    ]
}
```

---

### 9. **Próximo Vehículo a Procesar**
```
GET /api/vehiculos/proximo
```
**Descripción:** Retorna el primer vehículo de la cola a ser procesado

**Respuesta:**
```json
{
    "vehiculo": {
        "marca": "Toyota",
        "modelo": "Corolla",
        "anio": 2021,
        "tipo": "Automóvil",
        "estado": "En espera",
        "fecha_ingreso": "2026-04-11 09:00:00"
    }
}
```

---

## 📊 Estados del Vehículo

| Estado | Descripción |
|--------|-------------|
| **En espera** | Vehículo registrado, esperando revisión |
| **Revisado** | Vehículo ha pasado las pruebas |
| **Despachado** | Vehículo ha salido del CDA |
| **Retirado** | Cliente retiró el vehículo antes de revisión |

---

## 🔧 Ejemplo de Uso Completo

```python
from cda.colas_vehiculo import ColasVehiculo

# Crear instancia del gestor
gestor = ColasVehiculo()

# 1. Registrar vehículos
gestor.agregar_vehiculo("Chevrolet", "Tracker", 2020, "Automóvil")
gestor.agregar_vehiculo("Honda", "XRE 300", 2023, "Motocicleta")

# 2. Ver cantidad en operación
print(f"Vehículos en operación: {gestor.cantidad_vehiculos_operacion()}")  # Output: 2

# 3. Ver próximo vehículo
proximo = gestor.mostrar_vehiculo()
print(f"Próximo: {proximo}")

# 4. Agregar resultado de prueba
gestor.agregar_resultado_prueba("Chevrolet", "Tracker", "APROBADO", "Vehículo en buen estado")

# 5. Despachar vehículo
despachado = gestor.despachar_vehiculo()
print(f"Despachado: {despachado}")

# 6. Reportar revisados del día
revisados = gestor.reportar_vehiculos_revisados_hoy()
print(f"Revisados hoy: {len(revisados)}")
```

---

## ✅ Checklist de Funcionalidades Implementadas

- ✅ Registro de vehículos (Automóvil, Motocicleta, etc.)
- ✅ Estructura FIFO con cola de nodos enlazados
- ✅ Agregar resultado de pruebas
- ✅ Despacho de vehículos
- ✅ Retiro de vehículos antes de revisión
- ✅ Consulta de cantidad de vehículos en operación
- ✅ Reporte de vehículos revisados en el día
- ✅ Servicio web REST con Flask
- ✅ 9 rutas API completamente funcionales
- ✅ Validación de datos
- ✅ Manejo de errores
- ✅ Timestamps automáticos

---

**Proyecto completado: 11 de Abril de 2026**

---

## 📌 Notas Finales

Este documento contiene la especificación completa del Sistema CDA para la gestión de recepción y despacho de vehículos. Todos los archivos Python están listos para ser utilizados en el proyecto.

**Autor:** Ingeniero/a Desarrollador/a
**Fecha:** 11 de Abril de 2026
**Versión:** 1.0
