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

# Actividad 1: Bases de Datos NoSQL y Motores de Búsqueda

Este repositorio contiene los scripts y documentación relacionados con la actividad grupal de la asignatura **Bases de Datos Avanzadas**. El objetivo principal es diseñar y configurar un modelo de base de datos NoSQL utilizando MongoDB y Elasticsearch.

## Enlace al repositorio original
Puedes acceder al repositorio principal del equipo en GitHub:

[Repositorio GitHub](https://github.com/TheHacha167/BBDDA-Actividad-1)

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
Para implementar el clúster, lo primero será descargar e instalar Elasticsearch. Luego, configuramos el archivo `elasticsearch.yml` dentro de la carpeta `config`, con la siguiente configuración:

```yaml
cluster.name: estacion-cluster
node.name: nodo1
path.data: /var/lib/elasticsearch/data
path.logs: /var/log/elasticsearch
network.host: 0.0.0.0
http.port: 9200

# Para varios nodos:
discovery.seed_hosts: ["192.168.1.11", "192.168.1.12"]
cluster.initial_master_nodes: ["nodo1", "nodo2"]
```

Luego, se inicia Elasticsearch con el comando:
```bash
./bin/elasticsearch
```

De esta manera, el clúster quedará configurado y listo para su uso.


---

### **Enlaces de referencia**
- Documentación oficial de MongoDB: [https://www.mongodb.com/docs/](https://www.mongodb.com/docs/)
- Repositorio GitHub del equipo: [https://github.com/TheHacha167/BBDDA-Actividad-1](https://github.com/TheHacha167/BBDDA-Actividad-1)

---

### **Autores**
Este trabajo forma parte de la actividad grupal para la asignatura de Bases de Datos Avanzadas. Todos los integrantes del equipo han contribuido en la definición y desarrollo del proyecto.
