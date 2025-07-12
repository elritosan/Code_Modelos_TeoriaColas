// backend/routes/Basicos/queueModels_Routes.js
const express = require('express');
const { calculateMetrics } = require('../../controllers/Basicos/ClassQueueBase_Controller');

const router = express.Router();

// Ruta única para todos los modelos
router.post('/calculate', calculateMetrics);

module.exports = router;