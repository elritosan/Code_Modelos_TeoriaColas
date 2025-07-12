// backend/models/Basicos/ClassPFCS.js
const BaseQueueModel = require('../BaseQueueModel');
const math = require('mathjs');

class ClassPFCS extends BaseQueueModel {
  constructor(lam, mu, M) {
    super(lam, mu, 1); // k = 1 para PFCS
    this.M = M; // Tamaño de la población
  }

  // Métodos de probabilidad
  P0ProbSistemaDesocupado() {
    let suma = 0;
    for (let n = 0; n <= this.M; n++) {
      suma += math.factorial(this.M) / math.factorial(this.M - n) * 
              Math.pow(this.lam / this.mu, n);
    }
    return 1 / suma;
  }

  PEProbSistemaOcupado() {
    return 1 - this.P0ProbSistemaDesocupado();
  }

  Pn(n) {
    if (n > this.M || n < 0) return 0;
    
    const P0 = this.P0ProbSistemaDesocupado();
    return P0 * (math.factorial(this.M) / math.factorial(this.M - n)) * 
           Math.pow(this.lam / this.mu, n);
  }

  // Métodos de cantidad de clientes
  L() {
    return this.M - (this.mu / this.lam) * (1 - this.P0ProbSistemaDesocupado());
  }

  Lq() {
    return this.M - ((this.lam + this.mu) / this.lam) * 
           (1 - this.P0ProbSistemaDesocupado());
  }

  Ln() {
    return this.Lq() / this.PEProbSistemaOcupado();
  }

  // Métodos de tiempo de espera
  W() {
    return this.Wq() + (1 / this.mu);
  }

  Wq() {
    return this.Lq() / ((this.M - this.L()) * this.lam);
  }

  Wn() {
    return this.Wq() / this.PEProbSistemaOcupado();
  }

  // Métodos de costo (heredados de BaseQueueModel)
}

module.exports = ClassPFCS;