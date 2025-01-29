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


@corte_routes.route("/actualizar_estado_corte", methods=["POST"])
def actualizar_estado_corte():
    """
    Endpoint para actualizar el estado de un corte y generar una notificación cuando se confirma.
    """
    try:
        data = request.get_json()
        corte_id = data.get("corte_id")
        nuevo_estado = data.get("estado")

        if not corte_id or not nuevo_estado:
            return jsonify({"error": "Faltan datos obligatorios"}), 400

        # Obtener el corte
        corte = Corte.get_by_external_id(corte_id)
        if not corte:
            return jsonify({"error": "Corte no encontrado"}), 404

        # Si el estado cambia a "confirmado", generamos una nueva notificación
        if nuevo_estado == "confirmado" and corte["estado"] != "confirmado":
            # Actualizamos el estado del corte
            db["cortes"].update_one(
                {"external_id": corte_id},
                {"$set": {"estado": "confirmado"}}
            )

            # Generamos la nueva notificación
            mensaje = f"El servicio de {corte['tipoCorte']} no está disponible en su sector {corte['sector']}." \
                if corte['estado'] == "confirmado" else \
                f"¿Existe servicio de {corte['tipoCorte']} en su sector {corte['sector']}?\n" \
                "Respuestas disponibles: Sí / No"

            notificacion = Notificacion(
                mensaje=mensaje,
                tipo=TipoNotificacion.OFICIAL,
                usuario_id=corte["sector"]
            )

            # Enviamos la notificación directamente, sin esperar respuesta
            notificacion.save()

            return jsonify({"message": "Corte confirmado y notificación enviada correctamente"}), 200

        # Si no es el estado "confirmado", solo actualizamos el estado
        db["cortes"].update_one(
            {"external_id": corte_id},
            {"$set": {"estado": nuevo_estado}}
        )

        return jsonify({"message": "Estado de corte actualizado correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500