from datetime import datetime
from config.db import db

class Ubicacion:
    def __init__(self, latitud, longitud):
        self.latitud = latitud
        self.longitud = longitud

    def to_dict(self):
        return {
            "latitud": self.latitud,
            "longitud": self.longitud
        }

    def geolocalizacion(self, tipo, sector):
       
        print(f"Geolocalización del sector '{sector.nombre}' es: ({self.latitud}, {self.longitud})")