from flask import Flask
from flask_pymongo import PyMongo
from flask_socketio import SocketIO
from flask_cors import CORS  # Importa flask-cors
from routes.notificacion_routes import notificacion_routes
from routes.corte_routes import corte_routes



app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://pf_cloud:x4O20JELjV7WL7Ze@dbcloud.k63k2.mongodb.net/?retryWrites=true&w=majority"


# Inicializa PyMongo con la aplicación
mongo = PyMongo(app)

# Habilita CORS para toda la aplicación
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})



app.register_blueprint(notificacion_routes, url_prefix='/notificaciones')
app.register_blueprint(corte_routes, url_prefix='/cortes')


socketio = SocketIO(app, cors_allowed_origins="*")

if __name__ == "__main__":
    socketio.run(app, debug=True)