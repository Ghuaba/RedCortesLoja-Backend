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