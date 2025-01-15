from datetime import datetime
from config.db import db
from flask_socketio import emit

class Notificacion:
    def __init__(self, mensaje, fecha_envio, tipo):
        self.id = None  
        self.mensaje = mensaje
        self.fecha_envio = fecha_envio
        self.tipo = tipo
        self.collection = db["notificaciones"]

    def save(self):
        notificacion_data = {
            "mensaje": self.mensaje,
            "fecha_envio": self.fecha_envio,
            "tipo": self.tipo
        }
        result = self.collection.insert_one(notificacion_data)
        self.id = result.inserted_id 
        return result.inserted_id

    def enviar(self, usuarios):
        for usuario in usuarios:
            emit("notificacion", {"mensaje": self.mensaje, "fecha": self.fecha_envio}, room=usuario.id)