from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from config import MONGODB_URI, MONGODB_DB

client = MongoClient(MONGODB_URI)
db = client[str(MONGODB_DB)]
ubicaciones_collection = db['ubicaciones']

ubicaciones_bp = Blueprint('ubicaciones', __name__)

@ubicaciones_bp.route('/ubicaciones', methods=['POST'])
def agregar_ubicacion():
    data = request.get_json()
    nombre = data.get('nombre')
    latitud = data.get('latitud')
    longitud = data.get('longitud')

    if not nombre or not latitud or not longitud:
        return jsonify({"error": "Faltan datos"}), 400

    ubicacion = {
        "nombre": nombre,
        "latitud": latitud,
        "longitud": longitud
    }

    ubicaciones_collection.insert_one(ubicacion)
    return jsonify({"message": "Ubicación agregada correctamente"}), 201