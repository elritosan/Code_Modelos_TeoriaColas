// frontend/src/services/Basicos/queueModelsService.jsx
import axios from 'axios';

const API_URL = "http://localhost:5000/api/queue-models";

export const queueModelsService = {
  /**
   * Calcula las métricas para un modelo de cola
   * @param {Object} config - Configuración del cálculo
   * @param {string} config.modelType - Tipo de modelo (PICS, PICM, PFCS, PFCM)
   * @param {Object} config.params - Parámetros del modelo
   * @param {Object} [config.operations] - Operaciones adicionales
   * @returns {Promise<Object>} Resultados del cálculo
   */
  calcularMetricas: async ({ modelType, params, operations }) => {
    try {
      const response = await axios.post(`${API_URL}/calculate`, {
        modelType,
        params,
        operations
      });
      
      // Adaptamos ligeramente la respuesta para el frontend
      return {
        ...response.data,
        metrics: {
          ...response.data.metrics,
          // Añadimos propiedades calculadas para conveniencia
          utilization: params.lam / (params.mu * (params.k || 1)),
          ...(response.data.metrics.costs && {
            costs: {
              ...response.data.metrics.costs,
              // Añadimos costos por hora
              hourly: Object.entries(response.data.metrics.costs.daily)
                .filter(([key]) => key !== 'total')
                .reduce((acc, [key, value]) => ({
                  ...acc,
                  [key]: value / (params.hrlab || 8)
                }), {})
            }
          })
        }
      };
    } catch (error) {
      throw new Error(
        error.response?.data?.detalles || 
        error.response?.data?.error || 
        "Error al calcular métricas"
      );
    }
  },

  /**
   * Genera un rango de probabilidades para visualización
   * @param {Object} model - Modelo instanciado
   * @param {number} max - Valor máximo a calcular
   * @returns {Array<{n: number, pn: number}>} Array de probabilidades
   */
  generarRangoProbabilidades: (model, max) => {
    const resultados = [];
    for (let n = 0; n <= max; n++) {
      resultados.push({
        n,
        pn: model.Pn(n),
        enCola: Math.max(0, n - (model.k || 1))
      });
    }
    return resultados;
  },

  /**
   * Calcula métricas para un rango de valores de λ
   * @param {Object} config - Configuración base
   * @param {Array<number>} lambdas - Valores de λ a evaluar
   * @returns {Promise<Array>} Resultados por cada λ
   */
  calcularRangoLambdas: async (config, lambdas) => {
    const resultados = [];
    for (const lam of lambdas) {
      try {
        const res = await queueModelsService.calcularMetricas({
          ...config,
          params: { ...config.params, lam }
        });
        resultados.push(res);
      } catch (error) {
        console.error(`Error con λ=${lam}:`, error.message);
        resultados.push({ error: true, lam, message: error.message });
      }
    }
    return resultados;
  }
};

export default queueModelsService;