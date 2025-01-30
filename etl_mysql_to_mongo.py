import pymysql
import pymongo
import os
from dotenv import load_dotenv
from pymongo import UpdateOne

# Función para dividir en lotes
def dividir_en_lotes(lista, tamano_lote):
    for i in range(0, len(lista), tamano_lote):
        yield lista[i:i + tamano_lote]

# Conectar a MySQL
try:
    conexion_mysql = pymysql.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "mysql"),
        db=os.getenv("MYSQL_DB", "bbdda_etl")
    )
    cursor = conexion_mysql.cursor(pymysql.cursors.DictCursor)
except pymysql.MySQLError as e:
    print(f"Error conectando a MySQL: {e}")
    exit(1)

# Ejecutar consulta SQL
consulta_sql = """
    SELECT es.estacion_id, r.rotulo_id, r.nombre AS rotulo, 
           p.nombre AS provincia, m.nombre AS municipio, 
           te.descripcion AS tipo_estacion, tv.descripcion AS tipo_venta, 
           c.carburante_id, c.nombre AS nombre_carburante, pc.precio, 
           es.codigo_postal, es.direccion, es.latitud, es.longitud, es.horario 
    FROM EstacionServicio es
    JOIN Rotulo r ON es.rotulo_id = r.rotulo_id
    JOIN Localidad l ON es.localidad_id = l.localidad_id
    JOIN Municipio m ON l.municipio_id = m.municipio_id
    JOIN Provincia p ON m.provincia_id = p.provincia_id
    JOIN TipoEstacion te ON es.tipo_estacion_id = te.tipo_estacion_id
    JOIN TipoVenta tv ON es.tipo_venta_id = tv.tipo_venta_id
    JOIN PrecioCarburante pc ON es.estacion_id = pc.estacion_id
    JOIN Carburante c ON pc.carburante_id = c.carburante_id;
"""

cursor.execute(consulta_sql)
datos_mysql = cursor.fetchall()
conexion_mysql.close()

# Si no hay datos, salir
if not datos_mysql:
    print("No se encontraron datos en MySQL.")
    exit(1)

print(f"Total de registros obtenidos de MySQL: {len(datos_mysql)}")

# **Transformación de datos**
empresas = {}
estaciones = {}
precios_combustible = []

for row in datos_mysql:
    estacion_id = row["estacion_id"]
    rotulo_id = row["rotulo_id"]
    carburante_id = row["carburante_id"]

    # **Colección Empresas**
    if rotulo_id not in empresas:
        empresas[rotulo_id] = {
            "rotulo_id": rotulo_id,
            "nombre": row["rotulo"]
        }

    # **Colección Estaciones**
    if estacion_id not in estaciones:
        estaciones[estacion_id] = {
            "estacion_id": estacion_id,
            "rotulo_id": rotulo_id,
            "rotulo": row["rotulo"],
            "tipo_estacion": row["tipo_estacion"],
            "direccion": {
                "codigo_postal": row["codigo_postal"],
                "direccion": row["direccion"],
                "localidad": {
                    "nombre": row["municipio"],
                    "provincia": {
                        "nombre": row["provincia"]
                    }
                }
            },
            "coordenadas": {
                "latitud": float(row["latitud"]) if row["latitud"] else None,
                "longitud": float(row["longitud"]) if row["longitud"] else None
            },
            "tipo_venta": row["tipo_venta"],
            "horario": row["horario"]
        }

    # **Colección PreciosCombustible**
    precios_combustible.append({
        "estacion_id": estacion_id,
        "carburante_id": carburante_id,
        "nombre_carburante": row["nombre_carburante"],
        "precio": float(row["precio"])
    })

print(f"Total de empresas a insertar en MongoDB: {len(empresas)}")
print(f"Total de estaciones a insertar en MongoDB: {len(estaciones)}")
print(f"Total de precios de combustible a insertar en MongoDB: {len(precios_combustible)}")

# **Conectar a MongoDB**
try:
    uri_mongo = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    cliente_mongo = pymongo.MongoClient(uri_mongo)
    db = cliente_mongo["bbdda_mongo"]

    coleccion_empresas = db["Empresas"]
    coleccion_estaciones = db["Estaciones"]
    coleccion_precios_combustible = db["PreciosCombustible"]
except pymongo.errors.ConnectionFailure as e:
    print(f"Error conectando a MongoDB: {e}")
    exit(1)

# **Eliminar datos anteriores (opcional, para evitar duplicidad)**
coleccion_empresas.delete_many({})
coleccion_estaciones.delete_many({})
coleccion_precios_combustible.delete_many({})

# **Insertar Empresas**
TAMANO_LOTE = 5000
contador = 0
for lote in dividir_en_lotes(list(empresas.values()), TAMANO_LOTE):
    operaciones = [UpdateOne({"rotulo_id": emp["rotulo_id"]}, {"$set": emp}, upsert=True) for emp in lote]
    coleccion_empresas.bulk_write(operaciones)
    contador += len(lote)
    print(f"Empresas procesadas: {contador} de {len(empresas)}")

# **Insertar Estaciones**
contador = 0
for lote in dividir_en_lotes(list(estaciones.values()), TAMANO_LOTE):
    operaciones = [UpdateOne({"estacion_id": est["estacion_id"]}, {"$set": est}, upsert=True) for est in lote]
    coleccion_estaciones.bulk_write(operaciones)
    contador += len(lote)
    print(f"Estaciones procesadas: {contador} de {len(estaciones)}")

# **Insertar Precios de Combustible**
contador = 0
for lote in dividir_en_lotes(precios_combustible, TAMANO_LOTE):
    operaciones = [UpdateOne({"estacion_id": precio["estacion_id"], "carburante_id": precio["carburante_id"]},
                             {"$set": precio}, upsert=True) for precio in lote]
    coleccion_precios_combustible.bulk_write(operaciones)
    contador += len(lote)
    print(f"Precios procesados: {contador} de {len(precios_combustible)}")

print("Datos insertados en MongoDB correctamente.")

cliente_mongo.close()
