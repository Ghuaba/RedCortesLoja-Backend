from datetime import datetime
from config.db import db

class Supervisor:
    def __init__(self, privilegios, sectores_asignados):
        self.privilegios = privilegios
        self.sectores_asignados = sectores_asignados
        self.collection = db["supervisores"]

    def save(self):
        """Guardar el supervisor"""
        supervisor_data = {
            "privilegios": self.privilegios,
            "sectores_asignados": [sector.id for sector in self.sectores_asignados]
        }
        result = self.collection.insert_one(supervisor_data)
        return result.inserted_id

    def declararCorte(self, tipo, sector):
        """Declarar un corte"""
        corte = Corte(tipo, sector, "pendiente", datetime.now())
        corte.save()

    def recibirNotificacion(self, mensaje):
        """Recibir notificación"""
        notificacion = Notificacion(mensaje, datetime.now(), "oficial")
        notificacion.save()