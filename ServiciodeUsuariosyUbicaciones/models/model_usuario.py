from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='config/.env')
MONGODB_URI = os.getenv('MONGODB_URI')

client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000, tls=True)
db = client['dbcloud']
usuarios_collection = db['usuarios']

class Usuario:
    def __init__(self, nombre, apellido, correo, contraseña, ubicacion):
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.contraseña = contraseña
        self.ubicacion = ubicacion

    def save(self):
        usuario_data = {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "correo": self.correo,
            "contraseña": self.contraseña,
            "ubicacion": self.ubicacion
        }
        result = usuarios_collection.insert_one(usuario_data)
        return str(result.inserted_id)