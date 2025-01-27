// Crear índice para búsquedas por rótulo
db.Estaciones.createIndex({ rotulo: 1 });

// Crear índice para búsquedas geográficas
db.Estaciones.createIndex({ "coordenadas.latitud": 1, "coordenadas.longitud": 1 });
