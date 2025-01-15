from datetime import datetime
from config.db import db
from bson import ObjectId

class Sector:
    def __init__(self, id, nombre, ubicacion):
        self.id = id
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.usuarios = []
        self.collection = db["sectores"]

    def save(self):
        sector_data = {
            "id": self.id,
            "nombre": self.nombre,
            "ubicacion": self.ubicacion,
            "usuarios": [usuario.id for usuario in self.usuarios]
        }
        print(f"Intentando guardar el sector: {sector_data}")
        result = self.collection.insert_one(sector_data)
        print(f"Resultado de la inserción: {result.inserted_id}")
        return result.inserted_id


    def agregar_usuario(self, usuario):
        if usuario.id not in self.usuarios:
            self.usuarios.append(usuario.id)
            self.save()

    def get_sector_by_id(sector_id):
        if isinstance(sector_id, str):
            sector_id = ObjectId(sector_id)
        
        sector_data = db["sectores"].find_one({"_id": sector_id})
        if sector_data:
            sector = Sector(sector_data["id"], sector_data["nombre"], sector_data["ubicacion"])
            sector.usuarios = sector_data["usuarios"]
            return sector
        return None