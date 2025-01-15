from flask import Blueprint, request, jsonify
from controllers.corte_controller import CorteController
from models.sector import Sector

corte_routes = Blueprint('cortes', __name__)

@corte_routes.route('/crear', methods=['POST'])
def crear_corte():
    data = request.json
    print(f"Datos recibidos: {data}") 

    tipo = data['tipo']
    sector_id = data['sector']
    estado = "pendiente"
    fecha_reporte = data['fecha_reporte']
    
    try:
        corte_id = CorteController.crear_corte(tipo, sector_id, estado, fecha_reporte)
        return jsonify({"corte_id": str(corte_id)}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400