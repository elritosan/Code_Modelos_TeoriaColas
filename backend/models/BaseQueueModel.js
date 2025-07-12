// backend/models/BaseQueueModel.js

class BaseQueueModel {
  constructor(lam, mu, k = 1) {
    if (new.target === BaseQueueModel) {
      throw new Error("BaseQueueModel es una clase abstracta y no puede ser instanciada directamente");
    }

    this.lam = lam; // Tasa de llegada
    this.mu = mu;   // Tasa de servicio
    this.k = k;     // Número de servidores (por defecto 1)
    this.hrlab = 8;  // Horas laborables al día (valor por defecto)
  }

  setHrlab(hrlab) {
    this.hrlab = hrlab;
  }

  // Métodos abstractos que deben ser implementados por las clases hijas
  Pn(n) {
    throw new Error("Método abstracto Pn() debe ser implementado");
  }

  L() {
    throw new Error("Método abstracto L() debe ser implementado");
  }

  Lq() {
    throw new Error("Método abstracto Lq() debe ser implementado");
  }

  Ln() {
    throw new Error("Método abstracto Ln() debe ser implementado");
  }

  W() {
    throw new Error("Método abstracto W() debe ser implementado");
  }

  Wq() {
    throw new Error("Método abstracto Wq() debe ser implementado");
  }

  Wn() {
    throw new Error("Método abstracto Wn() debe ser implementado");
  }

  // Métodos concretos (implementación común)
  probUsuariosSistema(...rs) {
    return rs.reduce((sum, r) => sum + this.Pn(r), 0);
  }

  probMaxUsuariosSistema(r) {
    const limite = r;
    let sum = 0;
    for (let n = 0; n <= limite; n++) {
      sum += this.Pn(n);
    }
    return { probabilidad: sum, limite };
  }

  probMinUsuariosSistema(r) {
    const limite = r - 1;
    let sum = 0;
    for (let n = 0; n <= limite; n++) {
      sum += this.Pn(n);
    }
    return { probabilidad: 1 - sum, limite };
  }

  probUsuariosCola(...rs) {
    return rs.reduce((sum, r) => sum + this.Pn(this.k + r), 0);
  }

  probMaxUsuariosCola(r) {
    const limite = this.k + r;
    let sum = 0;
    for (let n = 0; n <= limite; n++) {
      sum += this.Pn(n);
    }
    return { probabilidad: sum, limite };
  }

  probMinUsuariosCola(r) {
    const limite = (this.k + r) - 1;
    let sum = 0;
    for (let n = 0; n <= limite; n++) {
      sum += this.Pn(n);
    }
    return { probabilidad: 1 - sum, limite };
  }

  // Métodos de costos
  CTE_costoDiarioEsperaCola(C_TE) {
    return this.lam * this.hrlab * this.Wq() * C_TE;
  }

  CTS_costoDiarioTiempoSistema(C_TS) {
    return this.lam * this.hrlab * this.W() * C_TS;
  }

  CTSE_costoDiarioServicio(C_TSE) {
    return this.lam * this.hrlab * (1 / this.mu) * C_TSE;
  }

  CS_costoDiarioServidor(C_S) {
    return this.k * C_S;
  }

  costoTotalDiario(C_TE, C_TS, C_TSE, C_S) {
    return (
      this.CTE_costoDiarioEsperaCola(C_TE) +
      this.CTS_costoDiarioTiempoSistema(C_TS) +
      this.CTSE_costoDiarioServicio(C_TSE) +
      this.CS_costoDiarioServidor(C_S)
    );
  }
}

module.exports = BaseQueueModel;