from flask import Blueprint, request, jsonify
from controllers.usuarioController import crear_usuario , obtener_usuarios, obtener_usuario_por_external_id
from controllers.usuarioController import actualizar_usuario,eliminar_usuario,actualizarEstado,listar_roles,crearSupervisor

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/crear', methods=['POST'])
def add_user():
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    correo = data.get('correo')
    contraseña = data.get('contraseña')
    ubicacion = data.get('ubicacion')

    response = crear_usuario(nombre, apellido, correo, contraseña,ubicacion)
    return jsonify(response)

@usuario_bp.route('/obtener', methods=['GET'])
def listar_usuarios():
    usuarios = obtener_usuarios()
    print(usuarios)
    return jsonify(usuarios)

@usuario_bp.route('/obtener/<external_id>', methods=['GET'])
def listar_usuario_por_external_id(external_id):
    usuario = obtener_usuario_por_external_id(external_id)
    if usuario:
        return jsonify(usuario)
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
@usuario_bp.route('/actualizar/<external_id>', methods=['POST'])
def actualizar(external_id):
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')

    response = actualizar_usuario(external_id, nombre, apellido)
    return jsonify(response)

@usuario_bp.route('/eliminar/<external_id>', methods=['DELETE'])
def eliminar(external_id):
    response = eliminar_usuario(external_id)
    return jsonify(response)

@usuario_bp.route('/actualizar_estado/<external_id>', methods=['POST'])
def actualizar_estado(external_id):
    response = actualizarEstado(external_id)
    return jsonify(response)

@usuario_bp.route('/listar', methods=['GET'])
def listar():
    roles = listar_roles()
    return jsonify(roles)

@usuario_bp.route('/crearSupervisor', methods=['POST'])
def add_supervisor():
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    correo = data.get('correo')
    contraseña = data.get('contraseña')

    response = crearSupervisor(nombre, apellido, correo, contraseña)
    return jsonify(response)