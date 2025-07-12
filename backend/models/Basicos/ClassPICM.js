// backend/models/Basicos/ClassPICM.js
const BaseQueueModel = require('../BaseQueueModel');
const math = require('mathjs');

class ClassPICM extends BaseQueueModel {
  constructor(lam, mu, k) {
    super(lam, mu, k);
    this.rho = lam / (k * mu);
    
    if (this.rho >= 1) {
      throw new Error("Sistema inestable: λ/(kμ) debe ser < 1");
    }
  }

  // Métodos de probabilidad
  P0ProbSistemaVacio() {
    let sum1 = 0;
    for (let n = 0; n < this.k; n++) {
      sum1 += (1 / math.factorial(n)) * Math.pow(this.lam / this.mu, n);
    }
    
    const term = (1 / math.factorial(this.k)) * 
                 Math.pow(this.lam / this.mu, this.k) * 
                 (this.k * this.mu) / (this.k * this.mu - this.lam);
    
    return 1 / (sum1 + term);
  }

  PkProbSistemaOcupado() {
    const P0 = this.P0ProbSistemaVacio();
    return (1 / math.factorial(this.k)) * 
           Math.pow(this.lam / this.mu, this.k) * 
           (this.k * this.mu) / (this.k * this.mu - this.lam) * 
           P0;
  }

  PNEProbSistemaDesocupado() {
    return 1 - this.PkProbSistemaOcupado();
  }

  Pn(n) {
    const P0 = this.P0ProbSistemaVacio();
    if (n < this.k) {
      return P0 * (1 / math.factorial(n)) * Math.pow(this.lam / this.mu, n);
    } else {
      return P0 * (1 / (math.factorial(this.k) * Math.pow(this.k, n - this.k))) * 
             Math.pow(this.lam / this.mu, n);
    }
  }

  // Métodos de cantidad de clientes
  L() {
    return this.Lq() + (this.lam / this.mu);
  }

  Lq() {
    const numerator = this.lam * this.mu * Math.pow(this.lam / this.mu, this.k) * 
                     this.P0ProbSistemaVacio();
    const denominator = math.factorial(this.k - 1) * 
                       Math.pow(this.k * this.mu - this.lam, 2);
    return numerator / denominator;
  }

  Ln() {
    return this.Lq() / this.PkProbSistemaOcupado();
  }

  // Métodos de tiempo de espera
  W() {
    return this.Wq() + (1 / this.mu);
  }

  Wq() {
    const numerator = this.mu * Math.pow(this.lam / this.mu, this.k) * 
                     this.P0ProbSistemaVacio();
    const denominator = math.factorial(this.k - 1) * 
                       Math.pow(this.k * this.mu - this.lam, 2);
    return numerator / denominator;
  }

  Wn() {
    return this.Wq() / this.PkProbSistemaOcupado();
  }

  // Métodos adicionales
  probTodosServidoresOcupados() {
    return this.PkProbSistemaOcupado();
  }

  // Métodos de costo (heredados de BaseQueueModel)
}

module.exports = ClassPICM;