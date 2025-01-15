from flask import Blueprint, request, jsonify
from controllers.notificacion_controller import NotificacionController

notificacion_routes = Blueprint('notificaciones', __name__)

@notificacion_routes.route('/enviar', methods=['POST'])
def enviar_notificacion():
    data = request.json
    usuario_id = data['usuario_id']
    mensaje = data['mensaje']
    
    usuario = get_usuario_by_id(usuario_id)  # falta implementar esta parte
    NotificacionController.enviar_notificacion(usuario, mensaje)
    
    return jsonify({"mensaje": "Notificación enviada"}), 200