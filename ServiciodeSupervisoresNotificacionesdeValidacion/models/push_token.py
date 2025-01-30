from datetime import datetime
from config.db import db

class PushToken:
    def __init__(self, token: str, sector_id: str, usuario_id: str = None):
        self.token = token
        self.sector_id = sector_id
        self.usuario_id = usuario_id
        self.fecha_registro = datetime.utcnow()
        self.collection = db["push_tokens"]

    def save(self):
        token_data = {
            "token": self.token,
            "sector_id": self.sector_id,
            "usuario_id": self.usuario_id,
            "fecha_registro": self.fecha_registro
        }
        
        # Actualizar si existe, insertar si no
        result = self.collection.update_one(
            {"token": self.token},
            {"$set": token_data},
            upsert=True
        )
        return str(result.upserted_id) if result.upserted_id else None