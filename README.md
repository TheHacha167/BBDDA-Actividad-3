# Actividad 1: Bases de Datos NoSQL y Motores de Búsqueda

Este repositorio contiene los scripts y documentación relacionados con la primera parte de la actividad grupal de la asignatura **Bases de Datos Avanzadas**. El objetivo principal es diseñar y configurar un modelo de base de datos NoSQL utilizando MongoDB.

## Enlace al repositorio original
Puedes acceder al repositorio principal del equipo en GitHub:

[Repositorio GitHub](https://github.com/TheHacha167/BBDDA-Actividad-1)

---

## Parte 1: Diseño de la base de datos NoSQL en MongoDB

### **Descripción del esquema**

El esquema seleccionado para esta actividad está basado en una estructura relacional que incluye:
- **Geografía**: Tablas como Comunidad, Provincia, Municipio y Localidad.
- **Estaciones de servicio**: Incluye informaciones como el rótulo, tipo de estación, margen respecto a la carretera y tipo de venta.
- **Carburantes y precios**: Tipos de carburantes y sus precios asociados a cada estación de servicio.

La transformación de este modelo relacional a NoSQL se ha realizado utilizando MongoDB, una base de datos documental. Este diseño aprovecha la flexibilidad y escalabilidad que ofrece MongoDB para sistemas distribuidos.

---

### **Scripts disponibles**

Los scripts están disponibles en la carpeta `mongo_scripts` del repositorio y permiten realizar diversas operaciones en MongoDB:

1. **Crear colección con validador**  
   Archivo: `mongo_scripts/crear_coleccion_estaciones.js`  
   Este script crea la colección `Estaciones` en MongoDB con un validador que asegura que los documentos insertados cumplan con el esquema lógicamente definido. 

   **Estructura básica del documento en MongoDB:**
   ```json
   {
     "estacion_id": 1,
     "rotulo": "Repsol",
     "tipo_estacion": "Terrestre",
     "direccion": {
       "codigo_postal": "28001",
       "direccion": "Calle Mayor, 123",
       "localidad": {
         "nombre": "Madrid",
         "municipio": {
           "nombre": "Madrid",
           "provincia": {
             "nombre": "Madrid",
             "comunidad": {
               "nombre": "Comunidad de Madrid"
             }
           }
         }
       }
     },
     "coordenadas": { "latitud": 40.416775, "longitud": -3.703790 },
     "margen": "Derecha",
     "tipo_venta": "Minorista",
     "carburantes": [
       { "nombre": "Gasolina 95", "precio": 1.589 },
       { "nombre": "Diesel", "precio": 1.479 }
     ],
     "horario": "24 horas"
   }
   ```

2. **Insertar datos de ejemplo**  
   Archivo: `mongo_scripts/insertar_datos_estaciones.js`  
   Este script incluye ejemplos de inserciones para poblar la colección `Estaciones` con datos iniciales.

3. **Consultar datos de estaciones**  
   Archivo: `mongo_scripts/consultar_datos_estaciones.js`  
   Este script contiene consultas comunes para obtener información de la colección `Estaciones`, como filtrado por localidad o búsqueda de estaciones con carburantes específicos.

4. **Crear índices en la colección**  
   Archivo: `mongo_scripts/crear_indices_estaciones.js`  
   Este script crea índices en los campos más utilizados en las consultas (por ejemplo, `rotulo` o `coordenadas`) para mejorar el rendimiento.

---

### **Requisitos para ejecutar los scripts**

1. Tener **MongoDB** instalado y configurado. Si utilizas Docker, puedes ejecutar MongoDB con el siguiente comando:
   ```bash
   docker run --name mongodb -d -p 27017:27017 -v mongo_data:/data/db mongo
   ```

2. **DataGrip** o el shell de MongoDB:
   - Puedes ejecutar los scripts desde **DataGrip** cargando cada archivo en el editor y ejecutándolo en la consola.
   - Alternativamente, usa el shell de MongoDB (`mongosh`) para ejecutar directamente:
     ```bash
     mongosh < mongo_scripts/crear_coleccion_estaciones.js
     ```


---

## Parte 2: Mapping de Elasticsearch

### **Archivo: `mapping_estaciones.json`**

```json
PUT /estaciones
{
  "mappings": {
    "properties": {
      "estacion_id": {
        "type": "integer"
      },
      "rotulo": {
        "type": "text",
        "fields": {
          "keyword": { "type": "keyword", "ignore_above": 256 }
        }
      },
      "tipo_estacion": {
        "type": "text",
        "fields": {
          "keyword": { "type": "keyword", "ignore_above": 256 }
        }
      },
      "margen": {
        "type": "text",
        "fields": {
          "keyword": { "type": "keyword", "ignore_above": 256 }
        }
      },
      "tipo_venta": {
        "type": "text",
        "fields": {
          "keyword": { "type": "keyword", "ignore_above": 256 }
        }
      },
      "horario": {
        "type": "text"
      },
      "direccion": {
        "properties": {
          "codigo_postal": {
            "type": "keyword"
          },
          "direccion": {
            "type": "text"
          },
          "localidad": {
            "properties": {
              "nombre": {
                "type": "text",
                "fields": {
                  "keyword": { "type": "keyword", "ignore_above": 256 }
                }
              },
              "municipio": {
                "properties": {
                  "nombre": {
                    "type": "text",
                    "fields": {
                      "keyword": { "type": "keyword", "ignore_above": 256 }
                    }
                  },
                  "provincia": {
                    "properties": {
                      "nombre": {
                        "type": "text",
                        "fields": {
                          "keyword": { "type": "keyword", "ignore_above": 256 }
                        }
                      },
                      "comunidad": {
                        "properties": {
                          "nombre": {
                            "type": "text",
                            "fields": {
                              "keyword": { "type": "keyword", "ignore_above": 256 }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      },
      "coordenadas": {
        "type": "geo_point"
      },
      "carburantes": {
        "type": "nested",
        "properties": {
          "nombre": {
            "type": "text",
            "fields": {
              "keyword": { "type": "keyword", "ignore_above": 256 }
            }
          },
          "precio": {
            "type": "float"
          }
        }
      }
    }
  }
}
```

### **Índice del clúster**
Para crear el índice en el clúster ejecutamos el siguiente comando:
```bash
curl -X PUT "http://localhost:9200/estaciones" \
  -H "Content-Type: application/json" \
  -d @mapping_estaciones.json
```

### **Implementación del clúster**
Para implementar el clúster, utilizamos el archivo que hemos creado de mongo_elastic.py:
```bash
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
```
De esta manera, ElasticSearch quedará configurado y listo para su uso.

--- 
### **Explicación del código ETL para la migración de datos de MySQL a MongoDB**

El funcionamiento del script de ETL (Extract, Transform, Load) que extrae datos desde una base de datos MySQL, los transforma en una estructura adecuada y los carga en MongoDB.  

### **Esquema planteado para la funcionalidad del Script**

1. Extraer datos desde MySQL mediante una consulta SQL con varias uniones.
2. Transformar los datos para organizarlos en las colecciones adecuadas.
3. Conectar a MongoDB y crear las colecciones necesarias.
4. Eliminar los datos anteriores en MongoDB para evitar duplicaciones.
5. Insertar los datos en lotes utilizando `bulk_write`.

### **Se han definido tres colecciones principales:**

- **Empresas**: Contiene información sobre las marcas de estaciones de servicio.
- **Estaciones**: Contiene detalles sobre cada estación de servicio, incluyendo ubicación y tipo de servicio.
- **PreciosCombustible**: Contiene los precios de los combustibles ofrecidos en cada estación.

### **Flujo del código**

#### **Conectar a MySQL y Obtener Datos**

- Se establece la conexión con MySQL utilizando `pymysql`.
- Se captura cualquier error en la conexión y se muestra un mensaje en caso de fallo.
- Se ejecuta una consulta SQL con varias uniones para obtener los datos sobre estaciones de servicio, sus rótulos, tipos de combustible y precios.

#### **Transformación de Datos**

Los datos extraídos de MySQL se transforman en estructuras adecuadas para ser insertadas en MongoDB. Se crean tres estructuras de datos:

- **Empresas**
- **Estaciones**
- **PreciosCombustible**

Se asegura que los datos sean correctos antes de insertarlos en MongoDB. También se convierte cualquier dato en formato `Decimal` a `float` para evitar errores de tipo en MongoDB.

#### **Conectar a MongoDB**

- Se establece la conexión con MongoDB y se crean las colecciones necesarias.
- Se capturan posibles errores en la conexión.

#### **Eliminación de Datos Anteriores**

Para evitar la duplicación de datos, se eliminan los registros existentes en las colecciones de MongoDB antes de insertar los nuevos datos.

#### **Inserción de Datos en MongoDB**

- Se utilizan operaciones en lote con `bulk_write` para mejorar la eficiencia en la inserción de datos en MongoDB.
- La opción `upsert=True` permite actualizar los registros existentes o insertarlos si no existen.

### **Ejecución del Script**

1. Configurar las credenciales en la línea de código 12 a 18:

   ```python
   host=os.getenv("MYSQL_HOST", "localhost"),
   user=os.getenv("MYSQL_USER", "root"),
   password=os.getenv("MYSQL_PASSWORD", "mysql"),
   db=os.getenv("MYSQL_DB", "bbdda_etl")
   ```

   Siempre y cuando se haya configurado de la misma manera, se mantiene el `host`, `user` y `password`, pero `MYSQL_DB` es necesario que apunte a la base de datos SQL donde tenemos los datos del esquema. Se debe reemplazar `bbdda_etl` por el nombre de tu base de datos.

2. Se mantiene tal cual la conexión a MongoDB:

   ```bash
   MYSQL_DB=bbdda_etl MONGO_URI=mongodb://localhost:27017/
   ```

### **PRUEBAS REALIZADAS**

#### **Antes de ejecutar el código:**

- Se verifica la estructura de la base de datos en MySQL.

#### **Después de ejecutar el código:**

1. Se crea la base de datos `bbdda_mongo` en MongoDB.
2. Accedemos a la base de datos en MongoDB:
   
   ```bash
   use bbdda_mongo
   ```
   
3. Verificamos las colecciones:
   
   ```bash
   show collections
   ```
   
   - Deben aparecer `Empresas`, `Estaciones` y `PreciosCombustible`.

4. Revisamos si las estaciones se insertaron correctamente:
   
   ```bash
   db.Estaciones.find().pretty()
   ```

5. Para verificar la información en `Empresas`:
   
   ```bash
   db.Empresas.find().pretty()
   ```

6. Consultamos los precios de combustible de una estación específica:
   
   ```bash
   db.PreciosCombustible.find({"estacion_id": 1}).pretty()
   ```

7. Para otra estación con `id=2`:
   
   ```bash
   db.PreciosCombustible.find({"estacion_id": 2}).pretty()
   


---

### **Enlaces de referencia**
- Documentación oficial de MongoDB: [https://www.mongodb.com/docs/](https://www.mongodb.com/docs/)
- Repositorio GitHub del equipo: [https://github.com/TheHacha167/BBDDA-Actividad-1](https://github.com/TheHacha167/BBDDA-Actividad-1)

---

### **Autores**
Este trabajo forma parte de la actividad grupal para la asignatura de Bases de Datos Avanzadas. Todos los integrantes del equipo han contribuido en la definición y desarrollo del proyecto.
