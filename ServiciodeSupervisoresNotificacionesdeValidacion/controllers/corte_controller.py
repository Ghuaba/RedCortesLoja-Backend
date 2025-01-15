from models.corte import Corte
from models.sector import Sector

class CorteController:
    @staticmethod
    def crear_corte(tipo, sector_id, estado, fecha_reporte):
        sector = Sector.get_sector_by_id(sector_id)
        
        if not sector:
            raise ValueError(f"Sector con ID {sector_id} no encontrado")
        
        corte = Corte(tipo, sector, estado, fecha_reporte)
        return corte.save()
    
    @staticmethod
    def validar_corte(corte, usuario):
        corte.validarCorte(usuario)
    
    @staticmethod
    def supervisor_corte(corte, usuario):
        corte.supervisorCorte(usuario)
    
    @staticmethod
    def rechazar_corte(corte, usuario):
        corte.rechazarCorte(usuario)