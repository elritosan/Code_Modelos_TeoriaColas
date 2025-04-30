from Models.Modelos_TeoriaColas import ClassPICS, ClassPICM

print("Modelo PICS")
oPICS = ClassPICS(10, 15);

r1_pics_pn1 = 1;
r1_pics_pn2 = 2;
r1_pics_pmax = 2;
r1_pics_pmin = 2;

print("\nProbabilidades de usuarios en el sistema:")

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
oPICM = ClassPICM(10, 7.5, 2);

r1_picm_pn1 = 1;
r1_picm_pn2 = 2;
r1_picm_pmax = 2;
r1_picm_pmin = 2;

print("\nProbabilidades de usuarios en el sistema:")

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