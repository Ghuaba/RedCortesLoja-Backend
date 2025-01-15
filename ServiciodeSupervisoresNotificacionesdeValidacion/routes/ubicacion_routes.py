from flask import Blueprint, request, jsonify
from controllers.ubicacion_controller import UbicacionController

ubicacion_routes = Blueprint('ubicaciones', __name__)

@ubicacion_routes.route('/geolocalizacion', methods=['GET'])
def obtener_geolocalizacion():
    ubicacion = get_ubicacion()  # falta implementar
    geolocalizacion = UbicacionController.obtener_geolocalizacion(ubicacion)
    
    return jsonify({"geolocalizacion": geolocalizacion}), 200