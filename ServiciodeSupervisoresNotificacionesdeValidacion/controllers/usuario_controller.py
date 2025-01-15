from models.usuario import Usuario
from models.ubicacion import Ubicacion

class UsuarioController:
    @staticmethod
    def crear_usuario(id, nombre, apellido, correo, contrasena, lat, lng):
        ubicacion = Ubicacion(lat, lng)
        usuario = Usuario(id, nombre, apellido, correo, contrasena, ubicacion)
        usuario_id = usuario.save()
        return str(usuario_id)
    
    @staticmethod
    def reportar_corte(usuario, tipo, sector):
        return usuario.reportarCorte(tipo, sector)