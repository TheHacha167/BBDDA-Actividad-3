from pymongo import MongoClient
from elasticsearch import Elasticsearch, helpers

# Conectar con MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["Actividad_1_BBDDA"]
mongo_collection = mongo_db["Estaciones"]

# Conectar con Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Extraer datos de MongoDB
estaciones = list(mongo_collection.find({}, {"_id": 0}))  # Excluir _id de MongoDB

# Crear lista de documentos para indexar en Elasticsearch
acciones = [
    {
        "_index": "estaciones",
        "_id": estacion["estacion_id"],  # Usamos el ID de la estación como identificador
        "_source": estacion
    }
    for estacion in estaciones
]

# Insertar en Elasticsearch
helpers.bulk(es, acciones)

print(f"Se han indexado {len(estaciones)} estaciones en Elasticsearch.")