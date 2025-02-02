from models.model_usuario import Usuario
import re
import uuid
from pymongo import MongoClient
from config import MONGODB_URI, MONGODB_DB
import logging
from bcrypt import hashpw, gensalt
from models.rol import listar_roles as listar_roles_model  

client = MongoClient(MONGODB_URI)
db = client[str(MONGODB_DB)]
usuarios_collection = db['usuarios']
rol_collection = db['rol']

logging.basicConfig(level=logging.ERROR)  # Set logging level to ERROR

def validar_datos_usuario(nombre, apellido, correo, contraseña,ubicacion):
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
def validar_datos_supervisor(nombre, apellido, correo, contraseña, ubicacion=None):
    # Implementa la validación de los datos del usuario aquí
    # Si ubicacion no es necesario, puedes ignorarlo o establecer un valor predeterminado
    if not nombre or not apellido or not correo or not contraseña:
        return False, "Todos los campos son obligatorios"
    # Agrega más validaciones según sea necesario
    return True, ""

def crear_usuario(nombre, apellido, correo, contraseña,ubicacion):
    try:
        valido, mensaje = validar_datos_usuario(nombre, apellido, correo, contraseña,ubicacion)
        if not valido:
            return {"message": mensaje}, 400  # Devuelve un código 400 para error de validación
        if usuarios_collection.find_one({"correo": correo}):
            return {"message": "Correo ya registrado"}, 400
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
        return {"message": "Usuario creado exitosamente", "id": str(result.inserted_id)}, 200
    except Exception as e:
        logging.error(f"Error al crear usuario: {e}")
        return {"message": "Error interno del servidor"},500
    

def crearSupervisor(nombre, apellido, correo, contraseña):
    try:
        valido, mensaje = validar_datos_supervisor(nombre, apellido, correo, contraseña)
        if not valido:
            return {"message": mensaje}, 400  # Devuelve un código 400 para error de validación
        
        if usuarios_collection.find_one({"correo": correo}):
            return {"message": "Correo de supervisor ya registrado"}, 400
        
        hashed_password = hashpw(contraseña.encode('utf-8'), gensalt())
        
        external_id = str(uuid.uuid4())
        estado = "activo"
        
        rol_supervisor = rol_collection.find_one({"nombre": "Supervisor"})
        if not rol_supervisor:
            return {"message": "Rol Supervisor no encontrado"}, 400
        
        nuevo_usuario = {
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "contraseña": hashed_password.decode('utf-8'),
            "external_id": external_id,
            "estado": estado,
            "rol_id": rol_supervisor["_id"]
        }
        
        usuarios_collection.insert_one(nuevo_usuario)
        return {"message": "Usuario creado exitosamente"}, 201
    except Exception as e:
        return {"message": str(e)}, 500
    

def obtener_usuarios():
    try:
        usuarios = list(usuarios_collection.find({}, {"_id": 0, "nombre": 1, "apellido": 1, "correo": 1, "estado": 1, "external_id": 1}))
        return {"code": 200, "datos": usuarios}
    except Exception as e:
        logging.error(f"Error al obtener usuarios: {e}")
        return {"code": 500, "message": "Error interno del servidor"}

def obtener_usuario_por_external_id(external_id):
    usuario = usuarios_collection.find_one({"external_id": external_id}, {"_id": 0, "nombre": 1, "apellido": 1})
    if not usuario:
        return {"code": 404, "message": "Usuario no encontrado"}
    return {"code": 200, "datos":usuario}

def actualizar_usuario(external_id, nombre, apellido):
    try:
        valido, mensaje = validar_datos_usuario(nombre, apellido)
        if not valido:
            return {"message": mensaje}
        
        usuario = usuarios_collection.find_one({"external_id": external_id})
        if not usuario:
            return {"message": "Usuario no encontrado"}
        
        usuarios_collection.update_one(
            {"external_id": external_id},
            {
                "$set": {
                    "nombre": nombre,
                    "apellido": apellido                    
                }
            }
        )
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
    
def actualizarEstado(external_id):
    try:
        usuario = usuarios_collection.find_one({"external_id": external_id})
        if not usuario:
            return {"message": "Usuario no encontrado"}

        nuevo_estado = not usuario["estado"]
        usuarios_collection.update_one(
            {"external_id": external_id},
            {"$set": {"estado": nuevo_estado}}
        )
        
        estado_str = "ACTIVADA" if nuevo_estado else "DESACTIVADA"
        print(f"Estado del usuario {usuario['correo']} actualizado a {estado_str}")
        return {"message": f"Estado del usuario actualizado a {estado_str}"}
    except Exception as e:
        logging.error(f"Error al actualizar estado del usuario: {e}")
        return {"message": "Error interno del servidor"}, 500
    
def listar_roles():
    try:
        roles = listar_roles_model()
        return { "datos": roles}, 200
    except Exception as e:
        return {"message":str(e)}, 500