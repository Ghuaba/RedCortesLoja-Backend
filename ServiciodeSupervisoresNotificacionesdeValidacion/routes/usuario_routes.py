from flask import Blueprint, request, jsonify
from controllers.usuario_controller import UsuarioController

usuario_routes = Blueprint('usuarios', __name__)

@usuario_routes.route('/crear', methods=['POST'])
def crear_usuario():
    data = request.json
    id = data['id']
    nombre = data['nombre']
    apellido = data['apellido']
    correo = data['correo']
    contrasena = data['contrasena']
    lat = data['lat']
    lng = data['lng']
    
    usuario_id = UsuarioController.crear_usuario(id, nombre, apellido, correo, contrasena, lat, lng)
    return jsonify({"usuario_id": usuario_id}), 201