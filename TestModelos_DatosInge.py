from Models.Modelos_TeoriaColas import ClassPICS, ClassPICM, ClassPFCS, ClassPFCM

print("Modelo PICS")
lam_pics = 10;
mu_pics = 15;
oPICS = ClassPICS(lam_pics, mu_pics);

r1_pics_pn1 = 1;
r1_pics_pn2 = 2;
r1_pics_pmax = 2;
r1_pics_pmin = 2;

print("\nProbabilidades de usuarios en el sistema:")

print(f"Probabilidad de encontrar sistema Ocupado:  {oPICS.rho_prob_sistema_ocupado()}");
print(f"Probabilidad de encontrar sistema desocupado:  {oPICS.P0_prob_sistema_desocupado()}");
print(f"Probabilidad de encontrar ({r1_pics_pn1}) usuario en el sistema:  {oPICS.prob_usuarios_sistema(r1_pics_pn1)}");
print(f"Probabilidad de encontrar ({r1_pics_pn1}) o ({r1_pics_pn2}) usuarios en el sistema:  {oPICS.prob_usuarios_sistema(r1_pics_pn1, r1_pics_pn2)}");
print(f"Probabilidad de encontrar máximo ({r1_pics_pmax}) usuarios en el sistema: {oPICS.prob_max_usuarios_sistema(r1_pics_pmax)}");
print(f"Probabilidad de encontrar al menos ({r1_pics_pmin}) usuarios en el sistema: {oPICS.prob_min_usuarios_sistema(r1_pics_pmin)}");

r2_pics_pn1 = 2;
r2_pics_pn2 = 3;
r2_pics_pmax = 2;
r2_pics_pmin = 1;

print("\nProbabilidades de usuarios en cola:")

print(f"Probabilidad de encontrar ({r2_pics_pn1}) usuario en cola:  {oPICS.prob_usuarios_cola(r2_pics_pn1)}");
print(f"Probabilidad de encontrar ({r2_pics_pn1}) o ({r2_pics_pn2}) usuarios en cola:  {oPICS.prob_usuarios_cola(r2_pics_pn1, r2_pics_pn2)}");
print(f"Probabilidad de encontrar máximo ({r2_pics_pmax}) usuarios en cola: {oPICS.prob_max_usuarios_cola(r2_pics_pmax)}");
print(f"Probabilidad de encontrar al menos ({r2_pics_pmin}) usuarios en cola: {oPICS.prob_min_usuarios_cola(r2_pics_pmin)}");

print("\nNumero de Clientes:")

print(f"Número esperado de clientes en el sistema: {oPICS.L()}")
print(f"Número esperado de clientes en la cola: {oPICS.Lq()}")
print(f"Número esperado de clientes en la cola no vacía: {oPICS.Ln()}")

print("\nTiempos de Espera:")

print(f"Tiempo esperado en el sistema: {oPICS.W()}")
print(f"Tiempo esperado en cola: {oPICS.Wq()}")
print(f"Tiempo esperado en cola para colas no vacías: {oPICS.Wn()}")

print("\nModelo PICS")
oPICS_Costo = ClassPICS(5, 10);

print("\nCostos Diarios:")

print(f"Costo diario de espera en cola: {oPICS_Costo.CTE_costo_diario_espera_cola(10)}")
print(f"Costo diario de tiempo en el sistema: {oPICS_Costo.CTS_costo_diario_tiempo_sistema(3.5)}")
print(f"Costo diario de tiempo en servicio: {oPICS_Costo.CTSE_costo_diario_servicio(10)}")
print(f"Costo diario de servidor: {oPICS_Costo.CS_costo_diario_servidor(10)}")

print("\n###############################################################################\n")

print("Modelo PICM")
lam_picm = 10;
mu_picm = 7.5;
k_picm = 2;
oPICM = ClassPICM(lam_picm, mu_picm, k_picm);

r1_picm_pn1 = 1;
r1_picm_pn2 = 2;
r1_picm_pmax = 2;
r1_picm_pmin = 2;

print("\nProbabilidades de usuarios en el sistema:")

print(f"Probabilidad de encontrar sistema Vacio:  {oPICM.P0_prob_sistema_vacio()}");
print(f"Probabilidad de encontrar sistema Ocupado:  {oPICM.Pk_prob_sistema_ocupado()}");
print(f"Probabilidad de encontrar sistema desocupado:  {oPICM.PNE_prob_sistema_desocupado()}");
print(f"Probabilidad de encontrar ({r1_picm_pn1}) usuario en el sistema:  {oPICM.prob_usuarios_sistema(r1_picm_pn1)}");
print(f"Probabilidad de encontrar ({r1_picm_pn1}) o ({r1_picm_pn2}) usuarios en el sistema:  {oPICM.prob_usuarios_sistema(r1_picm_pn1, r1_picm_pn2)}");
print(f"Probabilidad de encontrar máximo ({r1_picm_pmax}) usuarios en el sistema: {oPICM.prob_max_usuarios_sistema(r1_picm_pmax)}");
print(f"Probabilidad de encontrar al menos ({r1_picm_pmin}) usuarios en el sistema: {oPICM.prob_min_usuarios_sistema(r1_picm_pmin)}");

r2_picm_pn1 = 2;
r2_picm_pn2 = 3;
r2_picm_pmax = 2;
r2_picm_pmin = 1;

print("\nProbabilidades de usuarios en cola:")

print(f"Probabilidad de encontrar ({r2_picm_pn1}) usuario en cola:  {oPICM.prob_usuarios_cola(r2_picm_pn1)}");
print(f"Probabilidad de encontrar ({r2_picm_pn1}) o ({r2_picm_pn2}) usuarios en cola:  {oPICM.prob_usuarios_cola(r2_picm_pn1, r2_picm_pn2)}");
print(f"Probabilidad de encontrar máximo ({r2_picm_pmax}) usuarios en cola: {oPICM.prob_max_usuarios_cola(r2_picm_pmax)}");
print(f"Probabilidad de encontrar al menos ({r2_picm_pmin}) usuarios en cola: {oPICM.prob_min_usuarios_cola(r2_picm_pmin)}");

print("\nNumero de Clientes:")

print(f"Número esperado de clientes en el sistema: {oPICM.L()}")
print(f"Número esperado de clientes en la cola: {oPICM.Lq()}")
print(f"Número esperado de clientes en la cola no vacía: {oPICM.Ln()}")

print("\nTiempos de Espera:")

print(f"Tiempo esperado en el sistema: {oPICM.W()}")
print(f"Tiempo esperado en cola: {oPICM.Wq()}")
print(f"Tiempo esperado en cola para colas no vacías: {oPICM.Wn()}")

print("\nModelo PICM")
oPICM_Costo = ClassPICM(5, 10, 1);

print("\nCostos Diarios:")

print(f"Costo diario de espera en cola: {oPICM_Costo.CTE_costo_diario_espera_cola(10)}")
print(f"Costo diario de tiempo en el sistema: {oPICM_Costo.CTS_costo_diario_tiempo_sistema(3.5)}")
print(f"Costo diario de tiempo en servicio: {oPICM_Costo.CTSE_costo_diario_servicio(10)}")
print(f"Costo diario de servidor: {oPICM_Costo.CS_costo_diario_servidor(5)}")

print("\n###############################################################################\n")

print("Modelo PFCS")
lam_pfcs = 0.1;
mu_pfcs = 0.5;
m_pfcs = 4;
oPFCS = ClassPFCS(lam_pfcs, mu_pfcs, m_pfcs);

r1_pfcs_pn1 = 1;
r1_pfcs_pn2 = 2;
r1_pfcs_pmax = 2;
r1_pfcs_pmin = 2;

print("\nProbabilidades de usuarios en el sistema:")

print(f"Probabilidad de encontrar sistema Ocupado:  {oPFCS.PE_prob_sistema_ocupado()}");
print(f"Probabilidad de encontrar sistema desocupado:  {oPFCS.P0_prob_sistema_desocupado()}");
print(f"Probabilidad de encontrar ({r1_pfcs_pn1}) usuario en el sistema:  {oPFCS.prob_usuarios_sistema(r1_pfcs_pn1)}");
print(f"Probabilidad de encontrar ({r1_pfcs_pn1}) o ({r1_pfcs_pn2}) usuarios en el sistema:  {oPFCS.prob_usuarios_sistema(r1_pfcs_pn1, r1_pfcs_pn2)}");
print(f"Probabilidad de encontrar máximo ({r1_pfcs_pmax}) usuarios en el sistema: {oPFCS.prob_max_usuarios_sistema(r1_pfcs_pmax)}");
print(f"Probabilidad de encontrar al menos ({r1_pfcs_pmin}) usuarios en el sistema: {oPFCS.prob_min_usuarios_sistema(r1_pfcs_pmin)}");

r2_pfcs_pn1 = 2;
r2_pfcs_pn2 = 3;
r2_pfcs_pmax = 2;
r2_pfcs_pmin = 1;

print("\nProbabilidades de usuarios en cola:")

print(f"Probabilidad de encontrar ({r2_pfcs_pn1}) usuario en cola:  {oPFCS.prob_usuarios_cola(r2_pfcs_pn1)}");
print(f"Probabilidad de encontrar ({r2_pfcs_pn1}) o ({r2_pfcs_pn2}) usuarios en cola:  {oPFCS.prob_usuarios_cola(r2_pfcs_pn1, r2_pfcs_pn2)}");
print(f"Probabilidad de encontrar máximo ({r2_pfcs_pmax}) usuarios en cola: {oPFCS.prob_max_usuarios_cola(r2_pfcs_pmax)}");
print(f"Probabilidad de encontrar al menos ({r2_pfcs_pmin}) usuarios en cola: {oPFCS.prob_min_usuarios_cola(r2_pfcs_pmin)}");

print("\nNumero de Clientes:")

print(f"Número esperado de clientes en el sistema: {oPFCS.L()}");
print(f"Número esperado de clientes en la cola: {oPFCS.Lq()}");
print(f"Número esperado de clientes en la cola no vacía: {oPFCS.Ln()}");

print("\nTiempos de Espera:")

print(f"Tiempo esperado en el sistema: {oPFCS.W()}");
print(f"Tiempo esperado en cola: {oPFCS.Wq()}");
print(f"Tiempo esperado en cola para colas no vacías: {oPFCS.Wn()}");

print("\nModelo PFCS")
oPFCS_Costo = ClassPFCS(0.1, 0.5, 4);

print("\nCostos Diarios:")

print(f"Costo diario de espera en cola: {oPFCS_Costo.CTE_costo_diario_espera_cola(12)}");
print(f"Costo diario de tiempo en el sistema: {oPFCS_Costo.CTS_costo_diario_tiempo_sistema(20)}");
print(f"Costo diario de tiempo en servicio: {oPFCS_Costo.CTSE_costo_diario_servicio(8)}");
print(f"Costo diario de servidor: {oPFCS_Costo.CS_costo_diario_servidor(6)}");

print("\n###############################################################################\n")

print("Modelo PFCM")

lam_pfcm = 0.1;
mu_pfcm = 0.5;
m_pfcm = 4;
k_pfcm = 2;
oPFCM = ClassPFCM(lam_pfcm, mu_pfcm, m_pfcm, k_pfcm);

r1_pfcm_pn1 = 1;
r1_pfcm_pn2 = 2;
r1_pfcm_pmax = 2;
r1_pfcm_pmin = 2;

print("\nProbabilidades de usuarios en el sistema:")

print(f"Probabilidad de encontrar sistema Vacio:  {oPFCM.P0_prob_sistema_vacio()}");
print(f"Probabilidad de encontrar sistema Ocupado:  {oPFCM.PE_prob_sistema_ocupado()}");
print(f"Probabilidad de encontrar sistema desocupado:  {oPFCM.PNE_prob_sistema_desocupado()}");
print(f"Probabilidad de encontrar ({r1_pfcm_pn1}) usuario en el sistema:  {oPFCM.prob_usuarios_sistema(r1_pfcm_pn1)}");
print(f"Probabilidad de encontrar ({r1_pfcm_pn1}) o ({r1_pfcm_pn2}) usuarios en el sistema:  {oPFCM.prob_usuarios_sistema(r1_pfcm_pn1, r1_pfcm_pn2)}");
print(f"Probabilidad de encontrar máximo ({r1_pfcm_pmax}) usuarios en el sistema: {oPFCM.prob_max_usuarios_sistema(r1_pfcm_pmax)}");
print(f"Probabilidad de encontrar al menos ({r1_pfcm_pmin}) usuarios en el sistema: {oPFCM.prob_min_usuarios_sistema(r1_pfcm_pmin)}");

r2_pfcm_pn1 = 2;
r2_pfcm_pn2 = 3;
r2_pfcm_pmax = 2;
r2_pfcm_pmin = 1;

print("\nProbabilidades de usuarios en cola:")

print(f"Probabilidad de encontrar ({r2_pfcm_pn1}) usuario en cola:  {oPFCM.prob_usuarios_cola(r2_pfcm_pn1)}");
print(f"Probabilidad de encontrar ({r2_pfcm_pn1}) o ({r2_pfcm_pn2}) usuarios en cola:  {oPFCM.prob_usuarios_cola(r2_pfcm_pn1, r2_pfcm_pn2)}");
print(f"Probabilidad de encontrar máximo ({r2_pfcm_pmax}) usuarios en cola: {oPFCM.prob_max_usuarios_cola(r2_pfcm_pmax)}");
print(f"Probabilidad de encontrar al menos ({r2_pfcm_pmin}) usuarios en cola: {oPFCM.prob_min_usuarios_cola(r2_pfcm_pmin)}");

print("\nNumero de Clientes:")

print(f"Número esperado de clientes en el sistema: {oPFCM.L()}");
print(f"Número esperado de clientes en la cola: {oPFCM.Lq()}");
print(f"Número esperado de clientes en la cola no vacía: {oPFCM.Ln()}");

print("\nTiempos de Espera:")

print(f"Tiempo esperado en el sistema: {oPFCM.W()}");
print(f"Tiempo esperado en cola: {oPFCM.Wq()}");
print(f"Tiempo esperado en cola para colas no vacías: {oPFCM.Wn()}");

print("\nModelo PFCM")
oPFCM_Costo = ClassPFCM(0.1, 0.5, 4, 2);

print("\nCostos Diarios:")

print(f"Costo diario de espera en cola: {oPFCM_Costo.CTE_costo_diario_espera_cola(15)}");
print(f"Costo diario de tiempo en el sistema: {oPFCM_Costo.CTS_costo_diario_tiempo_sistema(25)}");
print(f"Costo diario de tiempo en servicio: {oPFCM_Costo.CTSE_costo_diario_servicio(10)}");
print(f"Costo diario de servidor: {oPFCM_Costo.CS_costo_diario_servidor(7)}");