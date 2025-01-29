from datetime import datetime
from config.db import db
import uuid

class TipoNotificacion:
    OFICIAL = "oficial"
    ALERTA = "alerta"
    GENERAL = "general"


class Notificacion:
    def __init__(self, mensaje, tipo, usuario_id, espera_respuesta=False):
        self.mensaje = mensaje
        self.tipo = tipo
        self.usuario_id = usuario_id
        self.fecha = datetime.utcnow()
        self.external_id = str(uuid.uuid4())
        self.external_id_corte = None  # Relacionamos con el corte
        self.espera_respuesta = espera_respuesta  # Indicamos si se espera una respuesta
        self.collection = db["notificaciones"]

    def save(self):
        """Guarda la notificación en MongoDB."""
        notificacion_data = {
            "external_id": self.external_id,
            "mensaje": self.mensaje,
            "tipo": self.tipo,
            "usuario_id": self.usuario_id,
            "fecha": self.fecha,
            "external_id_corte": self.external_id_corte,
            "espera_respuesta": self.espera_respuesta  # Añadimos la información sobre si se espera respuesta
        }
        result = self.collection.insert_one(notificacion_data)
        return str(result.inserted_id)