import requests
from typing import List, Dict
from config.db import db

class ExpoService:
    EXPO_API_URL = "https://exp.host/--/api/v2/push/send"
    
    @staticmethod
    def send_push_notifications(tokens: List[str], title: str, body: str, data: Dict = None) -> Dict:
        """
        Envía notificaciones push a múltiples tokens usando la API de Expo.
        """
        messages = []
        for token in tokens:
            message = {
                "to": token,
                "sound": "default",
                "title": title,
                "body": body,
                "data": data or {},
                "priority": "high",
                "badge": 1,
            }
            messages.append(message)

        try:
            response = requests.post(
                ExpoService.EXPO_API_URL,
                json=messages,
                headers={
                    "Accept": "application/json",
                    "Accept-encoding": "gzip, deflate",
                    "Content-Type": "application/json",
                }
            )
            return response.json()
        except Exception as e:
            print(f"Error sending push notifications: {str(e)}")
            return {"error": str(e)}

    @staticmethod
    def notify_sector(sector_id: str, title: str, body: str, data: Dict = None) -> Dict:
        """
        Envía notificaciones a todos los usuarios de un sector específico.
        """
        try:
            # Obtener todos los tokens del sector
            tokens = list(db.push_tokens.find({"sector_id": sector_id}))
            if not tokens:
                return {"message": "No hay tokens registrados para este sector"}

            token_list = [token["token"] for token in tokens]
            result = ExpoService.send_push_notifications(token_list, title, body, data)
            
            return result
        except Exception as e:
            return {"error": str(e)}