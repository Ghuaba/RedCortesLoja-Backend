from flask import Flask, jsonify
from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv
from routes.route_usuario import usuario_bp

def create_app():
    load_dotenv(dotenv_path='config/.env')
    MONGODB_URI = os.getenv('MONGODB_URI')
    
    app = Flask(__name__)

    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000, tls=True)
        client.admin.command('ping')
        connection_status = {"message": "MongoDB conectado correctamente", "status": "success"}
    except errors.ServerSelectionTimeoutError as e:
        connection_status = {"message": f"Error al conectar con MongoDB: {e}", "status": "failure"}

    @app.route('/')
    def index():
        return jsonify(connection_status)
    
    app.register_blueprint(usuario_bp, url_prefix='/usuario')

    return app