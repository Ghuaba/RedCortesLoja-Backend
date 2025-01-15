from datetime import datetime
from config.db import db
from models.corte import Corte
from models.notificacion import Notificacion

class Usuario:
    def __init__(self, id, nombre, apellido, correo, contrasena, ubicacion):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.contrasena = contrasena
        self.ubicacion = ubicacion
        self.collection = db["usuarios"]

    def save(self):
        usuario_data = {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "correo": self.correo,
            "contrasena": self.contrasena,
            "ubicacion": self.ubicacion.to_dict()
        }
        result = self.collection.insert_one(usuario_data)
        return result.inserted_id

    def reportarCorte(self, tipo, sector):
        corte = Corte(tipo, sector, "pendiente", datetime.now())
        corte.save()

    def validarCorte(self, corte):
        if corte.calcular_porcentaje_validacion() >= 65:
            corte.estado = "validado"
            corte.save()
            notificacion = Notificacion(f"Corte validado: {corte.tipo} en sector {corte.sector.nombre}", datetime.now(), "msj")
            notificacion.enviar(self)
            return True
        return False

    def recibirNotificacion(self, mensaje):
        notificacion = Notificacion(mensaje, datetime.now(), "msj")
        notificacion.enviar(self)