// backend/models/Basicos/ClassPICS.js
const BaseQueueModel = require('../BaseQueueModel');
const math = require('mathjs');

class ClassPICS extends BaseQueueModel {
  constructor(lam, mu) {
    super(lam, mu, 1); // k = 1 para PICS
    this.rho = lam / mu;
    
    if (this.rho >= 1) {
      throw new Error("Sistema inestable: λ/μ debe ser < 1");
    }
  }

  // Métodos de probabilidad
  rhoProbSistemaOcupado() {
    return this.rho;
  }

  P0ProbSistemaDesocupado() {
    return 1 - this.rho;
  }

  Pn(n) {
    return this.P0ProbSistemaDesocupado() * Math.pow(this.rho, n);
  }

  // Métodos de cantidad de clientes
  L() {
    return this.lam / (this.mu - this.lam);
  }

  Lq() {
    return Math.pow(this.lam, 2) / (this.mu * (this.mu - this.lam));
  }

  Ln() {
    return this.L();
  }

  // Métodos de tiempo de espera
  W() {
    return 1 / (this.mu - this.lam);
  }

  Wq() {
    return this.lam / (this.mu * (this.mu - this.lam));
  }

  Wn() {
    return this.W();
  }

  // Métodos de costo (heredados de BaseQueueModel)
  // Ya están implementados en la clase base
}

module.exports = ClassPICS;