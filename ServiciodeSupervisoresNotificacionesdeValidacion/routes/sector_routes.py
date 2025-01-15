from flask import Blueprint, request, jsonify
from controllers.sector_controller import SectorController

sector_routes = Blueprint('sectores', __name__)

@sector_routes.route('/crear', methods=['POST'])
def crear_sector():
    data = request.json
    id = data['id']
    nombre = data['nombre']
    lat = data['lat']
    lng = data['lng']
    
    sector_id = SectorController.crear_sector(id, nombre, lat, lng)
    return jsonify({"sector_id": sector_id}), 201