from flask import Blueprint, request, jsonify
from controllers.usuarioController import crear_usuario

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/adduser', methods=['POST'])
def add_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    correo = data.get('correo')
    contraseña = data.get('contraseña')
    ubicacion = data.get('ubicacion')
    
    result = crear_usuario(nombre, apellido, correo, contraseña, ubicacion)
    return jsonify(result)