from flask import Blueprint, request, jsonify
from controllers.supervisor_controller import SupervisorController

supervisor_routes = Blueprint('supervisores', __name__)

@supervisor_routes.route('/crear', methods=['POST'])
def crear_supervisor():
    data = request.json
    privilegios = data['privilegios']
    sectores_asignados = data['sectores_asignados']
    
    supervisor_id = SupervisorController.crear_supervisor(privilegios, sectores_asignados)
    return jsonify({"supervisor_id": supervisor_id}), 201