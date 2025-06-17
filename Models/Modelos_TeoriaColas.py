# Modelos_TeoriaColas.py
import math

from abc import ABC, abstractmethod

class ClassBaseTeoriaColas(ABC):
    def __init__(self, lam, mu, k=1):
        self.lam = lam
        self.mu = mu
        self.k = k
        # self.hrlab  # Horas laborables al día
    
    def set_hrlab(self, hrlab):
        self.hrlab = hrlab
        
    @abstractmethod
    def Pn(self, n):
        pass

    # Probabilidades
    def prob_usuarios_sistema(self, *rs):
        return sum(self.Pn(r) for r in rs)

    def prob_max_usuarios_sistema(self, r):
        limite = r
        return sum(self.Pn(n) for n in range(0, limite + 1)), limite

    def prob_min_usuarios_sistema(self, r):
        limite = r - 1
        return 1 - sum(self.Pn(n) for n in range(0, limite + 1)), limite
    
    def prob_usuarios_cola(self, *rs):
        return sum(self.Pn(self.k + r) for r in rs)

    def prob_max_usuarios_cola(self, r):
        limite = self.k + r
        return sum(self.Pn(n) for n in range(0, limite + 1)), limite

    def prob_min_usuarios_cola(self, r):
        limite = (self.k + r) - 1
        return 1 - sum(self.Pn(n) for n in range(0, limite + 1)), limite
    
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

    @abstractmethod
    def CTE_costo_diario_espera_cola(self, C_TE):
        pass

    @abstractmethod
    def CTS_costo_diario_tiempo_sistema(self, C_TS):
        pass

    @abstractmethod
    def CTSE_costo_diario_servicio(self, C_TSE):
        pass

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
        super().__init__(lam, mu, k)
        
    def CTE_costo_diario_espera_cola(self, C_TE):
        return self.lam * self.hrlab * self.Wq() * C_TE

    def CTS_costo_diario_tiempo_sistema(self, C_TS):
        return self.lam * self.hrlab * self.W() * C_TS

    def CTSE_costo_diario_servicio(self, C_TSE):
        return self.lam * self.hrlab * (1 / self.mu) * C_TSE

    def CS_costo_diario_servidor(self, C_S):
        return self.k * C_S

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
class ClassPICM(ClassInfinitas): 
    def __init__(self, lam, mu, k):
        super().__init__(lam, mu, k)
        self.rho = lam / (k * mu)
        if self.rho >= 1:
            raise ValueError("Sistema inestable: λ/(kμ) debe ser < 1")

    def P0_prob_sistema_vacio(self):
        sum1 = sum((1 / math.factorial(n)) * (self.lam / self.mu) ** n for n in range(self.k))
        sum2 = (1 / math.factorial(self.k)) * (self.lam / self.mu) ** self.k * (self.k * self.mu) / (self.k * self.mu - self.lam)
        return 1 / (sum1 + sum2)

    def Pk_prob_sistema_ocupado(self):
        P0 = self.P0_prob_sistema_vacio()
        return (1 / math.factorial(self.k)) * (self.lam / self.mu) ** self.k * (self.k * self.mu) / (self.k * self.mu - self.lam) * P0

    def PNE_prob_sistema_desocupado(self):
        return 1 - self.Pk_prob_sistema_ocupado()
    
    def Pn(self, n):
        P0 = self.P0_prob_sistema_vacio()
        if n < self.k:
            return P0 * (1 / math.factorial(n)) * (self.lam / self.mu) ** n
        else:
            return P0 * (1 / (math.factorial(self.k) * self.k ** (n - self.k))) * (self.lam / self.mu) ** n

    def L(self):
        return self.Lq() + (self.lam / self.mu)
    
    def Lq(self):
        return (self.lam * self.mu * ((self.lam / self.mu) ** self.k) * self.P0_prob_sistema_vacio()) / ((math.factorial(self.k - 1)) * ((self.k * self.mu - self.lam) ** 2))

    def Ln(self):
        return self.Lq() / self.Pk_prob_sistema_ocupado()

    def W(self):
        return self.Wq() + (1 / self.mu)
    
    def Wq(self):
        return (self.mu * ((self.lam / self.mu) ** self.k) * self.P0_prob_sistema_vacio()) / ((math.factorial(self.k - 1)) * ((self.k * self.mu - self.lam) ** 2))

    def Wn(self):
        return self.Wq() / self.Pk_prob_sistema_ocupado()
    

class ClassFinitas(ClassBaseTeoriaColas):
    def __init__(self, lam, mu, M, k=1):
        super().__init__(lam, mu, k)
        self.M = M
        
    @abstractmethod
    def PE_prob_sistema_ocupado(self, n):
        pass

    def Ln(self):
        return self.Lq() / self.PE_prob_sistema_ocupado()
    
    def W(self):
        return self.Wq() + (1 / self.mu)

    def Wq(self):
        return self.Lq() / ((self.M - self.L()) * self.lam)

    def Wn(self):
        return self.Wq() / self.PE_prob_sistema_ocupado()
    
    def CTE_costo_diario_espera_cola(self, C_TE):
        return self.lam * self.hrlab * self.Wq() * C_TE

    def CTS_costo_diario_tiempo_sistema(self, C_TS):
        return self.lam * self.hrlab * self.W() * C_TS

    def CTSE_costo_diario_servicio(self, C_TSE):
        return self.lam * self.hrlab * (1 / self.mu) * C_TSE

    def CS_costo_diario_servidor(self, C_S):
        return self.k * C_S

class ClassPFCS(ClassFinitas):
    def __init__(self, lam, mu, M, k=1):
        super().__init__(lam, mu, M, k)
    
    def P0_prob_sistema_desocupado(self):
        suma = sum(math.factorial(self.M) / math.factorial(self.M - n) * (self.lam / self.mu) ** n for n in range(self.M + 1))
        return 1 / suma
    
    def PE_prob_sistema_ocupado(self):
        return 1 - self.P0_prob_sistema_desocupado()
    
    def Pn(self, n):
        if n > self.M or n < 0:
            return 0
        P0 = self.P0_prob_sistema_desocupado()
        return P0 * (math.factorial(self.M) / math.factorial(self.M - n)) * (self.lam / self.mu) ** n
    
    def L(self):
        return self.M - (self.mu / self.lam) * (1 - self.P0_prob_sistema_desocupado())

    def Lq(self):
        return self.M - ((self.lam + self.mu) / self.lam) * (1 - self.P0_prob_sistema_desocupado())
class ClassPFCM(ClassFinitas):
    def __init__(self, lam, mu, M, k):
        super().__init__(lam, mu, M, k)
        
    def P0_prob_sistema_vacio(self):
        suma = 0
        for n in range(0, self.k):
            termino = math.factorial(self.M) / (math.factorial(self.M - n) * math.factorial(n)) * (self.lam / self.mu) ** n
            suma += termino
        for n in range(self.k, self.M + 1):
            termino = math.factorial(self.M) / (math.factorial(self.M - n) * math.factorial(self.k) * self.k ** (n - self.k)) * (self.lam / self.mu) ** n
            suma += termino
        return 1 / suma
    
    def PE_prob_sistema_ocupado(self):
        return sum(self.Pn(n) for n in range(self.k, self.M + 1))

    def Pn(self, n):
        if n < 0 or n > self.M:
            return 0
        P0 = self.P0_prob_sistema_vacio()
        if n < self.k:
            return P0 * math.factorial(self.M) / (math.factorial(self.M - n) * math.factorial(n)) * (self.lam / self.mu) ** n
        else:
            return P0 * math.factorial(self.M) / (math.factorial(self.M - n) * math.factorial(self.k) * self.k ** (n - self.k)) * (self.lam / self.mu) ** n

    def PNE_prob_sistema_desocupado(self):
        return 1 - self.PE_prob_sistema_ocupado()

    def L(self):
        suma1 = sum(n * self.Pn(n) for n in range(0, self.k))
        suma2 = sum((n - self.k) * self.Pn(n) for n in range(self.k, self.M + 1))
        suma3 = self.k * (1 - sum(self.Pn(n) for n in range(0, self.k)))
        return suma1 + suma2 + suma3

    def Lq(self):
        return sum((n - self.k) * self.Pn(n) for n in range(self.k, self.M + 1))