from flask import Blueprint, request, jsonify
from controllers.corte_controller import CorteController
from datetime import datetime
from config.db import db

from models.notificacion import Notificacion, TipoNotificacion
from models.corte import Corte
from bson import ObjectId

corte_routes = Blueprint('cortes', __name__)

#Creacion cortes
@corte_routes.route("/crear", methods=["POST"])
def crear_corte():
    """
    Ruta para crear un nuevo corte.

    Recibe datos en formato JSON con los campos:
    - tipo (str): Tipo de corte (directo o porConfirmar).
    - sector (int): ID del sector asociado al corte.

    Retorna:
        - Código 201 con el corte creado si tiene éxito.
        - Código 400 si falta algún dato o ocurre un error.
    """
    try:
        data = request.get_json()

        if not data or "tipo" not in data or "sector" not in data or "tipoCorte" not in data:
            return jsonify({"error": "Faltan campos requeridos (tipo, sector)"}), 400


        tipo = data["tipo"]
        tipoCorte = data["tipoCorte"]
        sector = data["sector"]
        estado = "pendiente" if tipo == "porConfirmar" else "confirmado"

        corte_creado = CorteController.crear_corte(tipo=tipo, tipoCorte = tipoCorte, sector=sector, estado=estado)

        respuesta = {
            "message": "Corte creado con éxito",
            "corte": corte_creado
        }

        return jsonify(respuesta), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

#Obtencion de los cortes registrados
@corte_routes.route("/cortes", methods=["GET"])
def obtener_cortes():
    """
    Ruta para obtener todos los cortes registrados en la base de datos.

    Retorna:
        - Código 200 con la lista de cortes si tiene éxito.
        - Código 500 si ocurre un error.
    """
    try:
        cortes = CorteController.obtener_todos_los_cortes()
        return jsonify({"cortes": cortes}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500