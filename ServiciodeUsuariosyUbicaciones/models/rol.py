from pymongo import MongoClient
import uuid
from config import MONGODB_URI, MONGODB_DB

client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000, tls=True)
db = client[str(MONGODB_DB)]
rol_collection = db['rol']

class Rol:
    def __init__(self, nombre):
        self.nombre = nombre

    def save(self):
        rol_data = {
            "nombre": self.nombre
        }
        result = rol_collection.insert_one(rol_data)
        return str(result.inserted_id)

# Inicializar roles
def inicializar_roles():
    if rol_collection.count_documents({}) == 0:
        roles = ["Supervisor", "Usuario"]
        for nombre in roles:
            rol = Rol(nombre)
            rol.save()

# Llamar a la función para inicializar los roles
inicializar_roles()

def listar_roles():
    roles = rol_collection.find({})
    return [{"nombre": rol["nombre"], "id": str(rol["_id"])} for rol in roles]