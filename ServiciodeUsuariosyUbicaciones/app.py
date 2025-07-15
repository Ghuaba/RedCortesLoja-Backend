from flask import Flask, jsonify
from pymongo import MongoClient, errors
from config import MONGODB_URI, MONGODB_DB, SECRET_KEY, JWT_SECRET_KEY, PORT
from routes.route_usuario import usuario_bp
from routes.route_login import login_bp
from routes.route_validartoken import api_validarToken
from routes.route_ubicaciones import api_ubicaciones
from flask_cors import CORS
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

    CORS(app)  # Enable CORS for all routes

    # Probar conexión a MongoDB
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
    except Exception as e:
        connection_status = {
            "message": f"Error inesperado: {e}", 
            "status": "failure"
        }
        logger.error(f"Error inesperado: {e}")

    @app.route('/')
    def index():
        return jsonify(connection_status)
    
    # Registrar blueprints
    app.register_blueprint(usuario_bp, url_prefix='/usuario')
    app.register_blueprint(login_bp, url_prefix='/home')
    app.register_blueprint(api_validarToken, url_prefix='/validaciones')
    app.register_blueprint(api_ubicaciones, url_prefix='/ubicacion')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=PORT)