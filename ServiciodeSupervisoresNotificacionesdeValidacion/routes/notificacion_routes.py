from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from config.db import db
from models.notificacion import Notificacion
from bson import ObjectId


from controllers.notificacion_controller import NotificacionController

notificacion_routes = Blueprint('notificaciones', __name__)


@notificacion_routes.route("/respuesta_notificacion", methods=["POST"])
def respuesta_notificacion():
    """
    Endpoint para recibir la respuesta de un usuario a una notificación.
    """
    try:
        data = request.get_json()
        corte_id = data.get("corte_id")
        respuesta = data.get("respuesta")

        if not corte_id or respuesta is None:
            return jsonify({"error": "Faltan datos obligatorios"}), 400

        # Buscar la notificación asociada al corte
        notificacion = db["notificaciones"].find_one({"external_id_corte": corte_id})

        if not notificacion:
            return jsonify({"error": "No se encontró la notificación asociada al corte"}), 404

        # Verificar si ya no se pueden aceptar más respuestas
        if notificacion.get("espera_respuesta") is False:
            return jsonify({"message": "El tiempo para responder ha terminado"}), 400

        # Verificar si han pasado más de 15 minutos desde la creación
        tiempo_creacion = notificacion["fecha"]
        if datetime.utcnow() - tiempo_creacion > timedelta(minutes=15):
            # Cerrar la posibilidad de respuestas
            db["notificaciones"].update_one(
                {"external_id_corte": corte_id},
                {"$set": {"espera_respuesta": False}}
            )

            # Obtener todas las respuestas registradas
            notificacion_actualizada = db["notificaciones"].find_one({"external_id_corte": corte_id})
            respuestas = notificacion_actualizada.get("respuestas_usuario", [])
            total_respuestas = len(respuestas)
            respuestas_true = sum(1 for res in respuestas if res["respuesta"] is True)

            # Evaluar si se confirma o se rechaza
            if total_respuestas == 0 or (respuestas_true / total_respuestas) < 0.65:
                estado_final = "rechazado"
            else:
                estado_final = "confirmado"

            # Actualizar el estado del corte
            db["cortes"].update_one(
                {"external_id": corte_id},
                {"$set": {"estado": estado_final}}
            )

            return jsonify({"message": f"El tiempo de respuesta ha finalizado. Corte marcado como {estado_final}"}), 200

        # Si aún está en el tiempo permitido, agregar la respuesta
        db["notificaciones"].update_one(
            {"external_id_corte": corte_id},
            {"$push": {"respuestas_usuario": {"respuesta": respuesta, "fecha": datetime.utcnow()}}}
        )

        return jsonify({"message": "Respuesta registrada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@notificacion_routes.route("/enviar", methods=["POST"])
def enviar_notificacion():
    """
    Ruta para enviar una notificación a un usuario específico.

    Recibe un JSON con los siguientes campos:
    - mensaje (str): Mensaje de la notificación.
    - tipo (str): Tipo de la notificación (OFICIAL, ALERTA, GENERAL).
    - usuario_id (str): ID del usuario al que se le enviará la notificación.

    Retorna:
        - Código 201 si la notificación fue enviada con éxito.
        - Código 400 si falta algún dato o hay un error.
    """
    try:
        data = request.get_json()

        if not data or "mensaje" not in data or "tipo" not in data or "usuario_id" not in data:
            return jsonify({"error": "Faltan datos obligatorios (mensaje, tipo, usuario_id)"}), 400

        mensaje = data["mensaje"]
        tipo = data["tipo"]
        usuario_id = data["usuario_id"]

        resultado = NotificacionController.enviar_notificacion(mensaje, tipo, usuario_id)

        if "error" in resultado:
            return jsonify({"error": resultado["error"]}), 400

        return jsonify(resultado), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400