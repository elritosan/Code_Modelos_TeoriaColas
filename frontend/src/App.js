// frontend\src\App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import TeoriaColasLayout from './views/teoriaColas/TeoriaColasLayout';
import TeoriaColasDashboard from './views/teoriaColas/TeoriaColasDashboard';
import ModeloColas from './views/teoriaColas/ModeloColas';

function App() {
  return (
    <Router>
      <Routes>
        {/* Ruta principal redirige al dashboard de teoría de colas */}
        <Route path="/" element={<Navigate to="/teoria-colas" replace />} />

        {/* Rutas de Teoría de Colas */}
        <Route path="/teoria-colas" element={<TeoriaColasLayout />}>
          <Route index element={<TeoriaColasDashboard />} />
          <Route path=":modelType" element={<ModeloColas />} />
        </Route>

        {/* Redirección para cualquier otra ruta no definida */}
        <Route path="*" element={<Navigate to="/teoria-colas" replace />} />
      </Routes>
    </Router>
  );
}

export default App;