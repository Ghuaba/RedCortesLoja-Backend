from models.corte import Corte
from models.notificacion import Notificacion, TipoNotificacion
from datetime import datetime
from config.db import db
from controllers.expo_service import ExpoService

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
            fecha_reporte = corte.get("fecha_reporte")
            if isinstance(fecha_reporte, str):  
                try:
                    fecha_reporte = datetime.fromisoformat(fecha_reporte)  
                except ValueError:
                    fecha_reporte = None  # Si hay un error en el formato, asignar None
            
            lista_cortes.append({
                "id": str(corte["_id"]),
                "tipo": corte.get("tipo"),
                "tipoCorte": corte.get("tipoCorte"),                
                "sector": corte.get("sector"),
                "estado": corte.get("estado"),
                "fechaReporte": fecha_reporte.isoformat() if fecha_reporte else None,
                "usuario_id": str(corte["usuario_id"]) if corte.get("usuario_id") else None
            })

        return lista_cortes


    @staticmethod
    def registrar_respuesta(corte_id, usuario_id, respuesta):
        """
        Registra la respuesta de un usuario sobre si hubo un corte.

        Args:
            corte_id (str): External ID del corte.
            usuario_id (str): ID del usuario que responde.
            respuesta (bool): True si confirma el corte, False si lo rechaza.

        Returns:
            dict: Mensaje indicando el estado de la operación.
        """
        collection_respuestas = db["respuestas"]  # Colección para registrar las respuestas

        # Validar que el corte exista
        corte = Corte.get_by_external_id(corte_id)
        if not corte:
            raise ValueError(f"No se encontró el corte con ID {corte_id}")

        # Registrar la respuesta
        respuesta_data = {
            "corte_id": corte_id,
            "usuario_id": usuario_id,
            "respuesta": respuesta,
            "fecha_respuesta": datetime.utcnow(),
        }

        # Asegurarnos de que un usuario no responda dos veces al mismo corte
        existing_response = collection_respuestas.find_one(
            {"corte_id": corte_id, "usuario_id": usuario_id}
        )
        if existing_response:
            raise ValueError("El usuario ya respondió a este corte")

        # Insertar la nueva respuesta
        collection_respuestas.insert_one(respuesta_data)
        return {"message": "Respuesta registrada con éxito"}


    @staticmethod
    def registrar_respuesta(corte_id, usuario_id, respuesta):
        """
        Registra la respuesta de un usuario sobre si hubo un corte.

        Args:
            corte_id (str): External ID del corte.
            usuario_id (str): ID del usuario que responde.
            respuesta (bool): True si confirma el corte, False si lo rechaza.

        Returns:
            dict: Mensaje indicando el estado de la operación.
        """
        collection_respuestas = db["respuestas"] 

        # Validar que el corte exista
        corte = Corte.get_by_external_id(corte_id)
        if not corte:
            raise ValueError(f"No se encontró el corte con ID {corte_id}")

        # Registrar la respuesta
        respuesta_data = {
            "corte_id": corte_id,
            "usuario_id": usuario_id,
            "respuesta": respuesta,
            "fecha_respuesta": datetime.utcnow(),
        }

        # Asegurarnos de que un usuario no responda dos veces al mismo corte
        existing_response = collection_respuestas.find_one(
            {"corte_id": corte_id, "usuario_id": usuario_id}
        )
        if existing_response:
            raise ValueError("El usuario ya respondió a este corte")

        # Insertar la nueva respuesta
        collection_respuestas.insert_one(respuesta_data)
        return {"message": "Respuesta registrada con éxito"}

    @staticmethod
    def validar_respuestas(corte_id):
        """
        Valida las respuestas de los usuarios y decide si hubo un corte.

        Args:
            corte_id (str): External ID del corte.

        Returns:
            dict: Mensaje indicando el resultado de la validación.
        """
        collection_respuestas = db["respuestas"]
        collection_notificaciones = db["notificaciones"]

        corte = Corte.get_by_external_id(corte_id)
        if not corte:
            raise ValueError("Corte no encontrado")

        # Obtener todas las respuestas del corte
        respuestas = list(collection_respuestas.find({"corte_id": corte_id}))
        if not respuestas:
            raise ValueError("No se han recibido respuestas para este corte")

        # Contar respuestas afirmativas y negativas
        total_respuestas = len(respuestas)
        respuestas_afirmativas = sum(1 for r in respuestas if r["respuesta"] is True)
        porcentaje_aceptacion = (respuestas_afirmativas / total_respuestas) * 100

        # Determinar si se debe generar una notificación oficial
        if porcentaje_aceptacion >= 65:
            # Actualizar el estado del corte a "confirmado"
            db["cortes"].update_one(
                {"external_id": corte_id},
                {"$set": {"estado": "confirmado"}}
            )

            # Crear una notificación oficial
            notificacion = {
                "corte_id": corte_id,
                "mensaje": "Se ha confirmado un corte en el sector",
                "tipo": "oficial",
                "fecha_creacion": datetime.utcnow(),
            }
            collection_notificaciones.insert_one(notificacion)

            ExpoService.notify_sector(
                sector_id=str(corte["sector"]),
                title=f"Corte de {corte['tipoCorte']} Confirmado",
                body=f"Se ha confirmado un corte de {corte['tipoCorte']} en su sector",
                data={"corte_id": corte_id}
            )

            return {
                "message": "El corte ha sido confirmado",
                "porcentaje_aceptacion": porcentaje_aceptacion,
                "estado": "confirmado",
            }

        # Si no se cumple el porcentaje mínimo
        return {
            "message": "El corte no pudo ser confirmado por falta de aceptación",
            "porcentaje_aceptacion": porcentaje_aceptacion,
            "estado": "pendiente",
        }