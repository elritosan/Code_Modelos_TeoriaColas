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

      
class ClassInfinitas(ClassBaseTeoriaColas):
    def __init__(self, lam, mu, k=1):
        super().__init__(lam, mu)
        self.k = k

class ClassPICS(ClassInfinitas):
    def __init__(self, lam, mu):
        super().__init__(lam, mu, k=1)
        self.rho = lam / mu
        if self.rho >= 1:
            raise ValueError("Sistema inestable: λ/μ debe ser < 1")

    def rho_prob_sistema_ocupado(self):
        return self.rho
    
    def P0_prob_sistema_desocupado(self):
        return 1 - self.rho

    def Pn(self, n):
        return self.P0_prob_sistema_desocupado() * (self.rho ** n)

    def L(self):
        return self.lam / (self.mu - self.lam)

    def Lq(self):
        return (self.lam ** 2) / (self.mu * (self.mu - self.lam))

    def Ln(self):
        return self.L()

    def W(self):
        return 1 / (self.mu - self.lam)

    def Wq(self):
        return self.lam / (self.mu * (self.mu - self.lam))

    def Wn(self):
        return self.W()

    def CS_costo_diario_servidor(self, C_S):
        return C_S