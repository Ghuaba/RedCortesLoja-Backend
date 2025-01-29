from models.corte import Corte
from models.sector import Sector

class CorteController:
    @staticmethod
    def crear_corte(tipo, tipoCorte, sector, estado="pendiente"):
        # Generar automáticamente la fecha del reporte
        fecha_reporte = datetime.now()

        nuevo_corte = Corte(tipo=tipo, tipoCorte=tipoCorte, sector=sector, estado=estado, fecha_reporte=fecha_reporte)

        corte_id = nuevo_corte.save()

        # Crear la notificación
        mensaje = f"El corte de {tipoCorte} en el sector {sector} ha sido creado."

        # Si el corte es de tipo "porConfirmar", esperamos una respuesta del usuario
        espera_respuesta = tipo == "porConfirmar"

        notificacion = Notificacion(mensaje, TipoNotificacion.OFICIAL, sector, espera_respuesta)
        notificacion.external_id_corte = nuevo_corte.external_id  # Relacionamos la notificación con el corte
        notificacion.save()  # Guardamos la notificación

        # Retornar el corte serializado con su nuevo ID
        return nuevo_corte.serialize

    @staticmethod
    def obtener_todos_los_cortes():
        """
        Obtiene todos los cortes de la base de datos.

        Returns:
            list: Lista de cortes en formato JSON.
        """
        cortes = db["cortes"].find()  # Obtener todos los documentos de la colección "cortes"
        lista_cortes = []

        for corte in cortes:
            lista_cortes.append({
                "id": str(corte["_id"]),
                "tipo": corte.get("tipo"),
                "sector": corte.get("sector"),
                "estado": corte.get("estado"),
                "fechaReporte": corte.get("fechaReporte").isoformat() if "fechaReporte" in corte else None,
                "usuario_id": str(corte["usuario_id"]) if corte.get("usuario_id") else None
            })

        return lista_cortes