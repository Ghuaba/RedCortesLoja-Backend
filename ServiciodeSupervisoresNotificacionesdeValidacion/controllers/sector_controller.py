from models.sector import Sector

class SectorController:
    @staticmethod
    def crear_sector(id, nombre, lat, lng):
        ubicacion = {"lat": lat, "lng": lng}
        sector = Sector(id, nombre, ubicacion)
        sector_id = sector.save()
        print(f"ID del sector creado: {sector_id}")
        return str(sector_id)  # Convertir ObjectId a cadena
    #@staticmethod
    #def crear_sector(id, nombre, ubicacion):
    #    sector = Sector(id, nombre, ubicacion)
    #    sector.save()
    #    return sector

    @staticmethod
    def agregar_usuario_a_sector(sector, usuario):
        sector.agregarUsuario(usuario)
        sector.save()