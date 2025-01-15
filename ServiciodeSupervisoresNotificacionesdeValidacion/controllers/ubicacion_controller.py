from models.ubicacion import Ubicacion

class UbicacionController:
    @staticmethod
    def obtener_geolocalizacion(ubicacion):
        return ubicacion.geolocalizacion()