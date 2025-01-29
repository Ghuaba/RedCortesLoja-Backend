from datetime import datetime
from config.db import db
import uuid
from bson import ObjectId

class Corte:
    def __init__(self, tipo, tipoCorte, sector, estado, fecha_reporte=None, external_id=None):
        self.tipo = tipo  # Tipo de corte (directo o con validación)
        self.tipoCorte = tipoCorte  # Agua/Luz
        self.sector = sector  # ID del sector
        self.estado = estado  # Estado del corte
        self.fecha_reporte = fecha_reporte if fecha_reporte else datetime.utcnow()  # Fecha actual por defecto
        self.external_id = external_id or str(uuid.uuid4())  # Generar un UUID si no se proporciona
        self.collection = db["cortes"]

    # Método para serializar la instancia
    @property
    def serialize(self):
        return {
            'external_id': self.external_id,  # Ahora usamos external_id
            'tipo': self.tipo,
            'tipoCorte': self.tipoCorte,
            'sector': self.sector,
            'estado': self.estado,
            "fecha_reporte": self.fecha_reporte.isoformat() if isinstance(self.fecha_reporte, datetime) else self.fecha_reporte,
        }

    # Método para guardar el documento en MongoDB
    def save(self):
        # Preparar los datos para la inserción
        corte_data = self.serialize
        # Insertar el documento en la colección y obtener el _id generado
        result = self.collection.insert_one(corte_data)
        return str(result.inserted_id)  # Retornar el _id generado por MongoDB

    # Método estático para obtener un corte por external_id
    @staticmethod
    def get_by_external_id(external_id):
        corte_data = db["cortes"].find_one({"external_id": external_id})
        if corte_data:
            return corte_data  # Devuelve los datos tal cual están en MongoDB
        return None
