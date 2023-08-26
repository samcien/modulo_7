from pymongo import MongoClient

# Inicializacion de Base de Datos
mongo_url = "mongodb://localhost:27017"
mongo_db = MongoClient(mongo_url)

# Crear base de datos
db = mongo_db["diccionario"]

collection = db.get_collection("Palabras")

if collection is None:
    collection = db.create_collection("Palabras")
else:
    pass

