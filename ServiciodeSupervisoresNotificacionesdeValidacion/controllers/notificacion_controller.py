from models.notificacion import Notificacion

class NotificacionController:
    @staticmethod
    def enviar_notificacion(usuario, mensaje):
        notificacion = Notificacion(mensaje, datetime.now(), "msj")
        return notificacion.enviar(usuario)