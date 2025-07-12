// backend/routes/apiRoutes.js
const express = require("express");
const router = express.Router();

router.use("/queue-models", require("./Basicos/queueModels_Routes"));

module.exports = router;