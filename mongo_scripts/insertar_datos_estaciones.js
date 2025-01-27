// Insertar un ejemplo de estación en la colección
db.Estaciones.insertOne({
    estacion_id: 1,
    rotulo: "Repsol",
    tipo_estacion: "Terrestre",
    direccion: {
      codigo_postal: "28001",
      direccion: "Calle Mayor, 123",
      localidad: {
        nombre: "Madrid",
        municipio: {
          nombre: "Madrid",
          provincia: {
            nombre: "Madrid",
            comunidad: {
              nombre: "Comunidad de Madrid"
            }
          }
        }
      }
    },
    coordenadas: { latitud: 40.416775, longitud: -3.703790 },
    margen: "Derecha",
    tipo_venta: "Minorista",
    carburantes: [
      { nombre: "Gasolina 95", precio: 1.589 },
      { nombre: "Diesel", precio: 1.479 }
    ],
    horario: "24 horas"
  });
  