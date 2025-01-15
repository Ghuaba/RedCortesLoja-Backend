from datetime import datetime
from config.db import db
from models.notificacion import Notificacion

class Corte:
    def __init__(self, tipo, sector, estado, fecha_reporte):
        self.id = None  
        self.tipo = tipo
        self.sector = sector 
        self.estado = estado
        self.fecha_reporte = fecha_reporte
        self.usuarios_validaciones = []
        self.collection = db["cortes"]

    def save(self):
        corte_data = {
            "tipo": self.tipo,
            "sector": self.sector.id,  
            "estado": self.estado,
            "fecha_reporte": self.fecha_reporte,
            "usuarios_validaciones": [usuario.id for usuario in self.usuarios_validaciones]  
        }
        if self.id:
            # Actualiza si ya existe
            self.collection.update_one({"_id": self.id}, {"$set": corte_data})
        else:
            # Inserta si es nuevo
            result = self.collection.insert_one(corte_data)
            self.id = result.inserted_id
        return self.id

    def calcular_porcentaje_validacion(self):
        total_usuarios = db["usuarios"].count_documents({"ubicacion": self.sector.id})
        if total_usuarios == 0:
            return 0
        return (len(self.usuarios_validaciones) / total_usuarios) * 100

    def validarCorte(self, usuario):
        if usuario not in self.usuarios_validaciones:
            self.usuarios_validaciones.append(usuario)
            self.save()

        if self.calcular_porcentaje_validacion() >= 65:
            self.estado = "validado"
            self.save()
            self.difundir_alerta()
            return True
        return False

    def difundir_alerta(self):
        notificacion = Notificacion(f"Alerta: Corte validado en sector {self.sector.nombre}", datetime.now(), "msj")
        notificacion.enviar(self)

    def supervisorCorte(self, usuario):
        self.estado = "supervisado"
        self.save()

    def rechazarCorte(self, usuario):
        self.estado = "rechazado"
        self.save()