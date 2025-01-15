from models.supervisor import Supervisor

class SupervisorController:
    @staticmethod
    def crear_supervisor(privilegios, sectores_asignados):
        supervisor = Supervisor(privilegios, sectores_asignados)
        return supervisor.save()
    
    @staticmethod
    def declarar_corte(supervisor, tipo, sector):
        supervisor.declararCorte(tipo, sector)