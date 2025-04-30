# Modelos_TeoriaColas.py
import math

from abc import ABC, abstractmethod

class ClassBaseTeoriaColas(ABC):
    def __init__(self, lam, mu):
        self.lam = lam
        self.mu = mu
        
    @abstractmethod
    def Pn(self, n):
        pass

    # Probabilidades
    def prob_usuarios_sistema(self, *rs):
        return sum(self.Pn(r) for r in rs)

    def prob_max_usuarios_sistema(self, r):
        return sum(self.Pn(n) for n in range(r + 1))

    def prob_min_usuarios_sistema(self, r):
        return 1 - sum(self.Pn(n) for n in range(r))
    
    def prob_usuarios_cola(self, *rs):
        return sum(self.Pn(self.k + r) for r in rs)

    def prob_max_usuarios_cola(self, r):
        limite = self.k + r
        return sum(self.Pn(n) for n in range(0, limite + 1))

    def prob_min_usuarios_cola(self, r):
        limite = (self.k + r) - 1
        return 1 - sum(self.Pn(n) for n in range(0, limite + 1))
    
    # Número de Clientes
    @abstractmethod
    def L(self):
        pass

    @abstractmethod
    def Lq(self):
        pass

    @abstractmethod
    def Ln(self):
        pass

    # Tiempos de Espera
    @abstractmethod
    def W(self):
        pass

    @abstractmethod
    def Wq(self):
        pass

    @abstractmethod
    def Wn(self):
        pass

    def CTE_costo_diario_espera_cola(self, C_TE):
        return self.lam * 8 * self.Wq() * C_TE

    def CTS_costo_diario_tiempo_sistema(self, C_TS):
        return self.lam * 8 * self.W() * C_TS

    def CTSE_costo_diario_servicio(self, C_TSE):
        return self.lam * 8 * (1 / self.mu) * C_TSE

    @abstractmethod
    def CS_costo_diario_servidor(self, C_S):
        pass

    def costo_total_diario(self, C_TE, C_TS, C_TSE, C_S):
        return (self.CTE_costo_diario_espera_cola(C_TE) +
                self.CTS_costo_diario_tiempo_sistema(C_TS) +
                self.CTSE_costo_diario_servicio(C_TSE) +
                self.CS_costo_diario_servidor(C_S))