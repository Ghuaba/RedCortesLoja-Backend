from flask import Flask, jsonify
from pymongo import MongoClient, errors
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    load_dotenv()
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    MONGODB_DB = os.getenv('MONGODB_DB', 'red_cortes_loja_notificaciones')
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    PORT = int(os.getenv('PORT', 5002))
    
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    
    CORS(app)  # Enable CORS for all routes

    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        connection_status = {
            "message": "MongoDB conectado correctamente - Ambiente Local", 
            "status": "success",
            "database": MONGODB_DB
        }
        logger.info("Conexión a MongoDB local establecida exitosamente")
    except errors.ServerSelectionTimeoutError as e:
        connection_status = {
            "message": f"Error al conectar con MongoDB local: {e}", 
            "status": "failure"
        }
        logger.error(f"Error de conexión a MongoDB: {e}")

    @app.route('/')
    def index():
        return jsonify(connection_status)

    return app

if __name__ == "__main__":
    app = create_app()
    PORT = int(os.getenv('PORT', 5002))
    app.run(debug=True, host="0.0.0.0", port=PORT)