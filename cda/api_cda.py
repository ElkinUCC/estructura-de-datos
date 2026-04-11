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
