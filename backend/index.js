// backend/index.js
const express = require("express");
const cors = require("cors");
const routes = require("./routes/apiRoutes");

const app = express();

// Configuración de middlewares
app.use(cors());
app.use(express.json());

// Configuración de rutas
app.use("/api", routes); // Todas las rutas ahora empiezan con /api

// Manejo de errores global
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Algo salió mal en el servidor' });
});

// Inicio del servidor
if (require.main === module) {
  const PORT = process.env.PORT || 5000;
  app.listen(PORT, () => {
    console.log(`🚀 Servidor corriendo en http://localhost:${PORT}`);
    console.log(`📚 API disponible en http://localhost:${PORT}/api`);
  });
}

module.exports = app; // Exportamos para pruebas