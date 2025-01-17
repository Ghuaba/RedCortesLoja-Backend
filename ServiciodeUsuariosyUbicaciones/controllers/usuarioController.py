from models.model_usuario import Usuario
import re

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
    valido, mensaje = validar_datos_usuario(nombre, apellido, correo, contraseña, ubicacion)
    if not valido:
        return {"message": mensaje}
    
    nuevo_usuario = Usuario(nombre, apellido, correo, contraseña, ubicacion)
    usuario_id = nuevo_usuario.save()
    return {"message": "Usuario creado exitosamente", "id": usuario_id}