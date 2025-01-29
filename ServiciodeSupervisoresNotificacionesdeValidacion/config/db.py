from pymongo import MongoClient

MONGO_URI = "mongodb+srv://pool:YCMcMjLBGoedfK9q@cluster0.dkbxw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)

db = client['ServicioSupervisorNotificaciones']
