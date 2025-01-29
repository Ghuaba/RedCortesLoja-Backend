from models.notificacion import Notificacion, TipoNotificacion
from config.db import db

class NotificacionController:

    @staticmethod
    def enviar_notificacion(mensaje, tipo, usuario_id):
        """
        Envía una notificación a un usuario específico.

        Args:
            mensaje (str): Mensaje de la notificación.
            tipo (str): Tipo de notificación.
            usuario_id (str): ID del usuario al que se le enviará la notificación.

        Returns:
            dict: Respuesta con el estado de la notificación enviada.
        """
        try:
            if tipo not in [TipoNotificacion.OFICIAL, TipoNotificacion.ALERTA, TipoNotificacion.GENERAL]:
                raise ValueError("Tipo de notificación no válido")
            
            notificacion = Notificacion(mensaje, tipo, usuario_id)
            resultado = notificacion.save()

            return {"message": "Notificación enviada con éxito", "data": {"external_id": resultado}}

        except Exception as e:
            return {"error": str(e)}


    @staticmethod
    def obtener_notificaciones(usuario_id):
        """
        Obtiene todas las notificaciones enviadas a un usuario específico.

        Args:
            usuario_id (str): ID del usuario para el que se desean obtener las notificaciones.

        Returns:
            list: Lista de notificaciones para el usuario.
        """
        try:
            notificaciones = db["notificaciones"].find({"usuario_id": usuario_id})
            lista_notificaciones = []

            for notificacion in notificaciones:
                lista_notificaciones.append({
                    "external_id": str(notificacion["_id"]),
                    "mensaje": notificacion["mensaje"],
                    "tipo": notificacion["tipo"],
                    "fecha": notificacion["fecha"]
                })

            return lista_notificaciones

        except Exception as e:
            return {"error": str(e)}