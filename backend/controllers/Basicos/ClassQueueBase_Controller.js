// backend/controllers/Basicos/ClassQueueBase_Controller.js

exports.calculateMetrics = async (req, res) => {
  try {
    const { modelType, params, operations } = req.body;
    
    if (!modelType || !params) {
      return res.status(400).json({
        success: false,
        error: "Datos incompletos",
        detalles: "Se requieren modelType y params"
      });
    }

    // Validación básica de parámetros comunes
    if (!params.lam || !params.mu) {
      return res.status(400).json({
        success: false,
        error: "Parámetros inválidos",
        detalles: "lam y mu son requeridos"
      });
    }

    let model;
    switch(modelType) {
      case 'PICS':
        model = new (require('../../models/Basicos/ClassPICS'))(params.lam, params.mu);
        break;
      case 'PICM':
        if (!params.k) throw new Error("k es requerido para PICM");
        model = new (require('../../models/Basicos/ClassPICM'))(params.lam, params.mu, params.k);
        break;
      case 'PFCS':
        if (!params.M) throw new Error("M es requerido para PFCS");
        model = new (require('../../models/Basicos/ClassPFCS'))(params.lam, params.mu, params.M);
        break;
      case 'PFCM':
        if (!params.M || !params.k) throw new Error("M y k son requeridos para PFCM");
        model = new (require('../../models/Basicos/ClassPFCM'))(params.lam, params.mu, params.M, params.k);
        break;
      default:
        throw new Error("Tipo de modelo no válido");
    }

    if (params.hrlab) model.setHrlab(params.hrlab);

    // Preparar respuesta base
    const response = {
      success: true,
      modelType,
      metrics: {
        numClientes: {
          L: model.L(),
          Lq: model.Lq(),
          Ln: model.Ln()
        },
        waitingTime: {
          W: model.W(),
          Wq: model.Wq(),
          Wn: model.Wn()
        },
        probabilities: {
          system: {},
          queue: {}
        }
      }
    };

    // Métodos específicos de cada modelo
    if (modelType === 'PICS') {
      response.metrics.probabilities.system.P0 = model.P0ProbSistemaDesocupado();
      response.metrics.probabilities.system.rho = model.rhoProbSistemaOcupado();
    } else if (modelType === 'PICM') {
      response.metrics.probabilities.system.P0 = model.P0ProbSistemaVacio();
      response.metrics.probabilities.system.Pk = model.PkProbSistemaOcupado();
      response.metrics.probabilities.system.PNE = model.PNEProbSistemaDesocupado();
    } else if (modelType === 'PFCS') {
      response.metrics.probabilities.system.P0 = model.P0ProbSistemaDesocupado();
      response.metrics.probabilities.system.PE = model.PEProbSistemaOcupado();
    } else if (modelType === 'PFCM') {
      response.metrics.probabilities.system.P0 = model.P0ProbSistemaVacio();
      response.metrics.probabilities.system.PE = model.PEProbSistemaOcupado();
      response.metrics.probabilities.system.PNE = model.PNEProbSistemaDesocupado();
    }

    // Procesar operaciones adicionales si existen
    if (operations) {
      // Probabilidades en el sistema
      if (operations.systemProbabilities) {
        const { exact, max, min } = operations.systemProbabilities;
        
        if (exact) {
          response.metrics.probabilities.system.exact = {};
          exact.forEach(n => {
            response.metrics.probabilities.system.exact[`P${n}`] = model.Pn(n);
          });
          response.metrics.probabilities.system.exactSum = model.probUsuariosSistema(...exact);
        }
        
        if (max !== undefined) {
          const { probabilidad, limite } = model.probMaxUsuariosSistema(max);
          response.metrics.probabilities.system.max = {
            probability: probabilidad,
            upTo: limite
          };
        }
        
        if (min !== undefined) {
          const { probabilidad, limite } = model.probMinUsuariosSistema(min);
          response.metrics.probabilities.system.min = {
            probability: probabilidad,
            upTo: limite
          };
        }
      }
      
      // Probabilidades en cola
      if (operations.queueProbabilities) {
        const { exact, max, min } = operations.queueProbabilities;
        
        if (exact) {
          response.metrics.probabilities.queue.exact = {};
          exact.forEach(r => {
            const n = model.k + r;
            response.metrics.probabilities.queue.exact[`Q${r}`] = model.Pn(n);
          });
          response.metrics.probabilities.queue.exactSum = model.probUsuariosCola(...exact);
        }
        
        if (max !== undefined) {
          const { probabilidad, limite } = model.probMaxUsuariosCola(max);
          response.metrics.probabilities.queue.max = {
            probability: probabilidad,
            upTo: limite - model.k // Convertir a usuarios en cola
          };
        }
        
        if (min !== undefined) {
          const { probabilidad, limite } = model.probMinUsuariosCola(min);
          response.metrics.probabilities.queue.min = {
            probability: probabilidad,
            upTo: (limite + 1) - model.k // Convertir a usuarios en cola
          };
        }
      }
      
      // Cálculo de costos
      if (operations.costs) {
        response.metrics.costs = {
          daily: {
            CTE: model.CTE_costoDiarioEsperaCola(operations.costs.CTE || 0),
            CTS: model.CTS_costoDiarioTiempoSistema(operations.costs.CTS || 0),
            CTSE: model.CTSE_costoDiarioServicio(operations.costs.CTSE || 0),
            CS: model.CS_costoDiarioServidor(operations.costs.CS || 0),
            total: model.costoTotalDiario(
              operations.costs.CTE || 0,
              operations.costs.CTS || 0,
              operations.costs.CTSE || 0,
              operations.costs.CS || 0
            )
          },
          unitCosts: operations.costs
        };
      }
    }

    res.json(response);
    
  } catch (error) {
    const statusCode = error.message.includes('inestable') ? 422 : 500;
    res.status(statusCode).json({
      success: false,
      error: "Error en cálculo",
      detalles: error.message
    });
  }
};