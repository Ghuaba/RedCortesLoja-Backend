from models.model_usuario import Usuario
import re
import uuid
from pymongo import MongoClient
from config import MONGODB_URI, MONGODB_DB
import logging
from bcrypt import hashpw, gensalt

client = MongoClient(MONGODB_URI)
db = client[str(MONGODB_DB)]
usuarios_collection = db['usuarios']

logging.basicConfig(level=logging.ERROR)  # Set logging level to ERROR

def validar_datos_usuario(nombre, apellido, correo, contraseña, ubicacion):
    if not re.match(r'^[a-zA-Z]{2,}$', nombre):
        return False, "Nombre inválido"
    if not re.match(r'^[a-zA-Z]{2,}$', apellido):
        return False, "Apellido inválido"
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo):
        return False, "Correo inválido"
    if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', contraseña):
        return False, "Contraseña inválida"
    if not re.match(r'^[a-zA-Z\s]{2,}$', ubicacion):
        return False, "Ubicación inválida"
    return True, ""

def crear_usuario(nombre, apellido, correo, contraseña, ubicacion):
    try:
        valido, mensaje = validar_datos_usuario(nombre, apellido, correo, contraseña, ubicacion)
        if not valido:
            return {"message": mensaje}
        
        if usuarios_collection.find_one({"correo": correo}):
            return {"message": "Correo ya registrado"}
        
        hashed_password = hashpw(contraseña.encode('utf-8'), gensalt())
        
        external_id = str(uuid.uuid4())
        estado = "activo"
        
        nuevo_usuario = {
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "contraseña": hashed_password.decode('utf-8'),
            "ubicacion": ubicacion,
            "external_id": external_id,
            "estado": estado
        }
        
        result = usuarios_collection.insert_one(nuevo_usuario)
        print(f"Usuario creado exitosamente: {nuevo_usuario['correo']}")
        return {"message": "Usuario creado exitosamente", "id": str(result.inserted_id)}
    except Exception as e:
        logging.error(f"Error al crear usuario: {e}")
        return {"message": "Error interno del servidor"}, 500
    
def obtener_usuarios():
    try:
        usuarios = list(usuarios_collection.find({}, {"_id": 0, "nombre": 1, "apellido": 1, "correo": 1, "estado": 1, "external_id": 1}))
        return {"code": 200, "datos": usuarios}
    except Exception as e:
        logging.error(f"Error al obtener usuarios: {e}")
        return {"code": 500, "message": "Error interno del servidor"}

def obtener_usuario_por_external_id(external_id):
    usuario = usuarios_collection.find_one({"external_id": external_id}, {"_id": 0, "nombre": 1, "apellido": 1, "correo": 1, "ubicacion": 1})
    return usuario

def actualizar_usuario(external_id, nombre, apellido, correo, contraseña, ubicacion):
    try:
        valido, mensaje = validar_datos_usuario(nombre, apellido, correo, contraseña, ubicacion)
        if not valido:
            return {"message": mensaje}
        
        usuario = usuarios_collection.find_one({"external_id": external_id})
        if not usuario:
            return {"message": "Usuario no encontrado"}
        
        hashed_password = hashpw(contraseña.encode('utf-8'), gensalt())
        
        usuarios_collection.update_one(
            {"external_id": external_id},
            {
                "$set": {
                    "nombre": nombre,
                    "apellido": apellido,
                    "correo": correo,
                    "contraseña": hashed_password.decode('utf-8'),
                    "ubicacion": ubicacion
                }
            }
        )
        print(f"Usuario actualizado exitosamente: {correo}")
        return {"message": "Usuario actualizado exitosamente"}
    except Exception as e:
        logging.error(f"Error al actualizar usuario: {e}")
        return {"message": "Error interno del servidor"}, 500
    
def eliminar_usuario(external_id):
    try:
        usuario = usuarios_collection.find_one({"external_id": external_id})
        if not usuario:
            return {"message": "Usuario no encontrado"}
        
        usuarios_collection.delete_one({"external_id": external_id})
        print(f"Usuario eliminado exitosamente: {usuario['correo']}")
        return {"message": "Usuario eliminado exitosamente"}
    except Exception as e:
        logging.error(f"Error al eliminar usuario: {e}")
        return {"message": "Error interno del servidor"}, 500