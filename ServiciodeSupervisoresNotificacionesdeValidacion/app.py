from flask import Flask
from flask_socketio import SocketIO
from routes.usuario_routes import usuario_routes
from routes.sector_routes import sector_routes
from routes.corte_routes import corte_routes
from routes.notificacion_routes import notificacion_routes
from routes.supervisor_routes import supervisor_routes
from routes.ubicacion_routes import ubicacion_routes

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

app.register_blueprint(usuario_routes, url_prefix='/usuarios')
app.register_blueprint(sector_routes, url_prefix='/sectores')
app.register_blueprint(corte_routes, url_prefix='/cortes')
app.register_blueprint(notificacion_routes, url_prefix='/notificaciones')
app.register_blueprint(supervisor_routes, url_prefix='/supervisores')
app.register_blueprint(ubicacion_routes, url_prefix='/ubicaciones')

#if __name__ == '__main__':
#    app.run(debug=True)

@socketio.on("connect")
def handle_connect():
    print("Cliente conectado")

@socketio.on("disconnect")
def handle_disconnect():
    print("Cliente desconectado")

if __name__ == "__main__":
    socketio.run(app, debug=True)