import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_DB = os.getenv('MONGODB_DB', 'red_cortes_loja_usuarios')
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret')
PORT = int(os.getenv('PORT', 5000))

print(f"Conectando a MongoDB: {MONGODB_URI}")
print(f"Base de datos: {MONGODB_DB}")
print(f"Puerto: {PORT}")