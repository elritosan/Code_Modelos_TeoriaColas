// backend/models/Basicos/ClassPFCM.js
const BaseQueueModel = require('../BaseQueueModel');
const math = require('mathjs');

class ClassPFCM extends BaseQueueModel {
  constructor(lam, mu, M, k) {
    super(lam, mu, k);
    this.M = M; // Tamaño de la población
  }

  // Métodos de probabilidad
  P0ProbSistemaVacio() {
    let suma = 0;
    
    // Suma para n < k
    for (let n = 0; n < this.k; n++) {
      suma += math.factorial(this.M) / 
             (math.factorial(this.M - n) * math.factorial(n)) * 
             Math.pow(this.lam / this.mu, n);
    }
    
    // Suma para n >= k
    for (let n = this.k; n <= this.M; n++) {
      suma += math.factorial(this.M) / 
             (math.factorial(this.M - n) * math.factorial(this.k) * 
             Math.pow(this.k, n - this.k)) * 
             Math.pow(this.lam / this.mu, n);
    }
    
    return 1 / suma;
  }

  PEProbSistemaOcupado() {
    let prob = 0;
    for (let n = this.k; n <= this.M; n++) {
      prob += this.Pn(n);
    }
    return prob;
  }

  PNEProbSistemaDesocupado() {
    return 1 - this.PEProbSistemaOcupado();
  }

  Pn(n) {
    if (n < 0 || n > this.M) return 0;
    
    const P0 = this.P0ProbSistemaVacio();
    if (n < this.k) {
      return P0 * math.factorial(this.M) / 
             (math.factorial(this.M - n) * math.factorial(n)) * 
             Math.pow(this.lam / this.mu, n);
    } else {
      return P0 * math.factorial(this.M) / 
             (math.factorial(this.M - n) * math.factorial(this.k) * 
             Math.pow(this.k, n - this.k)) * 
             Math.pow(this.lam / this.mu, n);
    }
  }

  // Métodos de cantidad de clientes
  L() {
    let suma1 = 0; // Suma para n < k
    for (let n = 0; n < this.k; n++) {
      suma1 += n * this.Pn(n);
    }
    
    let suma2 = 0; // Suma para n >= k
    for (let n = this.k; n <= this.M; n++) {
      suma2 += (n - this.k) * this.Pn(n);
    }
    
    const suma3 = this.k * (1 - this.PNEProbSistemaDesocupado());
    
    return suma1 + suma2 + suma3;
  }

  Lq() {
    let sum = 0;
    for (let n = this.k; n <= this.M; n++) {
      sum += (n - this.k) * this.Pn(n);
    }
    return sum;
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

module.exports = ClassPFCM;