// Conexión a la base de datos
use Actividad_1_BBDDA;

// Crear la colección "Estaciones" con un validador
db.createCollection("Estaciones", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["estacion_id", "rotulo", "direccion", "carburantes"],
      properties: {
        estacion_id: { bsonType: "int" },
        rotulo: { bsonType: "string" },
        direccion: {
          bsonType: "object",
          required: ["codigo_postal", "localidad"],
          properties: {
            codigo_postal: { bsonType: "string" },
            localidad: {
              bsonType: "object",
              required: ["nombre"],
              properties: {
                nombre: { bsonType: "string" }
              }
            }
          }
        },
        carburantes: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: ["nombre", "precio"],
            properties: {
              nombre: { bsonType: "string" },
              precio: { bsonType: "double" }
            }
          }
        },
        tipo_estacion: { bsonType: "string" },
        coordenadas: {
          bsonType: "object",
          properties: {
            latitud: { bsonType: "double" },
            longitud: { bsonType: "double" }
          }
        },
        margen: { bsonType: "string" },
        tipo_venta: { bsonType: "string" },
        horario: { bsonType: "string" }
      }
    }
  }
});
