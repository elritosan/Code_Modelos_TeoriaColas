import tkinter as tk
from tkinter import ttk, messagebox
from Models.Modelos_TeoriaColas import ClassPICS, ClassPICM, ClassPFCS, ClassPFCM

class QueueTheoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modelos de Teoría de Colas")
        self.root.geometry("1000x800")
        
        self.create_main_interface()
        
    def create_main_interface(self):
        """Interfaz principal para seleccionar el modelo"""
        self.clear_window()
        
        lbl_title = tk.Label(self.root, text="Seleccione el Modelo de Cola", font=('Arial', 14))
        lbl_title.pack(pady=20)
        
        # Botones para cada modelo
        models = [
            ("PICS (M/M/1)", "PICS"),
            ("PICM (M/M/k)", "PICM"),
            ("PFCS (M/M/1/M)", "PFCS"),
            ("PFCM (M/M/k/M)", "PFCM")
        ]
        
        for text, model in models:
            btn = tk.Button(self.root, text=text, 
                          command=lambda m=model: self.show_model_interface(m), 
                          width=20, height=2)
            btn.pack(pady=10)
        
    def show_model_interface(self, model_type):
        """Muestra la interfaz específica para cada modelo"""
        self.clear_window()
        self.model_type = model_type
        self.model = None
        
        # Botón de regreso
        btn_back = tk.Button(self.root, text="← Volver", command=self.create_main_interface)
        btn_back.pack(anchor='nw', padx=10, pady=10)
        
        # Frame para parámetros de entrada
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=20)
        
        # Título del modelo
        model_names = {
            "PICS": "PICS (M/M/1) - Un servidor, población infinita",
            "PICM": "PICM (M/M/k) - Múltiples servidores, población infinita",
            "PFCS": "PFCS (M/M/1/M) - Un servidor, población finita",
            "PFCM": "PFCM (M/M/k/M) - Múltiples servidores, población finita"
        }
        lbl_model = tk.Label(self.root, text=model_names[model_type], font=('Arial', 12))
        lbl_model.pack(pady=10)
        
        # Campos de entrada según el modelo
        self.entries = {}
        
        lbl_lam = tk.Label(input_frame, text="Tasa de llegada (λ):")
        lbl_lam.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entries['lam'] = tk.Entry(input_frame)
        self.entries['lam'].grid(row=0, column=1, padx=5, pady=5)
        
        lbl_mu = tk.Label(input_frame, text="Tasa de servicio (μ):")
        lbl_mu.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entries['mu'] = tk.Entry(input_frame)
        self.entries['mu'].grid(row=1, column=1, padx=5, pady=5)
        
        if model_type in ["PICM", "PFCM"]:
            lbl_k = tk.Label(input_frame, text="Número de servidores (k):")
            lbl_k.grid(row=2, column=0, padx=5, pady=5, sticky='e')
            self.entries['k'] = tk.Entry(input_frame)
            self.entries['k'].grid(row=2, column=1, padx=5, pady=5)
            
        if model_type in ["PFCS", "PFCM"]:
            lbl_m = tk.Label(input_frame, text="Tamaño población (M):")
            lbl_m.grid(row=3, column=0, padx=5, pady=5, sticky='e')
            self.entries['M'] = tk.Entry(input_frame)
            self.entries['M'].grid(row=3, column=1, padx=5, pady=5)
        
        # Botón de cálculo
        btn_calculate = tk.Button(self.root, text="Calcular", command=self.calculate_model)
        btn_calculate.pack(pady=20)
        
        # Frame para resultados
        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
    def calculate_model(self):
        """Calcula los resultados según el modelo seleccionado"""
        try:
            # Obtener parámetros de entrada
            params = {
                'lam': float(self.entries['lam'].get()),
                'mu': float(self.entries['mu'].get())
            }
            
            if self.model_type in ["PICM", "PFCM"]:
                params['k'] = int(self.entries['k'].get())
                
            if self.model_type in ["PFCS", "PFCM"]:
                params['M'] = int(self.entries['M'].get())
            
            # Crear instancia del modelo
            if self.model_type == "PICS":
                self.model = ClassPICS(params['lam'], params['mu'])
            elif self.model_type == "PICM":
                self.model = ClassPICM(params['lam'], params['mu'], params['k'])
            elif self.model_type == "PFCS":
                self.model = ClassPFCS(params['lam'], params['mu'], params['M'])
            elif self.model_type == "PFCM":
                self.model = ClassPFCM(params['lam'], params['mu'], params['M'], params['k'])
            
            # Mostrar resultados
            self.show_results()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Entrada inválida: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
    
    def show_results(self):
        """Muestra los resultados del cálculo"""
        self.clear_frame(self.result_frame)
        
        # Crear notebook (pestañas)
        notebook = ttk.Notebook(self.result_frame)
        notebook.pack(fill='both', expand=True)
        
        # Pestaña de probabilidades con submenús
        prob_frame = tk.Frame(notebook)
        notebook.add(prob_frame, text="Probabilidades")
        self.create_probability_tab(notebook, prob_frame)
        
        # Pestaña de métricas
        metrics_frame = tk.Frame(notebook)
        notebook.add(metrics_frame, text="Métricas")
        self.create_metrics_tab(metrics_frame)
        
        # Pestaña de costos (si aplica)
        if self.model_type in ["PICS", "PICM", "PFCS", "PFCM"]:
            cost_frame = tk.Frame(notebook)
            notebook.add(cost_frame, text="Costos")
            self.create_cost_tab(cost_frame)
    
    def create_probability_tab(self, notebook, parent):
        """Crea la pestaña de probabilidades con submenús"""
        # Frame principal con scrollbar
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Menú de opciones de probabilidad
        prob_menu = tk.Menu(scrollable_frame)
        
        # 1. Probabilidades del sistema (básicas)
        sys_frame = tk.Frame(scrollable_frame)
        sys_frame.pack(fill='x', padx=5, pady=5)
        
        btn_sys_basics = tk.Button(sys_frame, text="Probabilidades Básicas del Sistema", 
                                  command=lambda: self.show_prob_section("basics"))
        btn_sys_basics.pack(fill='x', pady=2)
        
        # 2. Cálculos de probabilidades en el sistema
        btn_sys_calc = tk.Button(sys_frame, text="Cálculos en el Sistema", 
                                command=lambda: self.show_prob_section("system_calc"))
        btn_sys_calc.pack(fill='x', pady=2)
        
        # 3. Cálculos de probabilidades en cola
        btn_queue_calc = tk.Button(sys_frame, text="Cálculos en Cola", 
                                  command=lambda: self.show_prob_section("queue_calc"))
        btn_queue_calc.pack(fill='x', pady=2)
        
        # Frame para mostrar las secciones de probabilidad
        self.prob_section_frame = tk.Frame(scrollable_frame)
        self.prob_section_frame.pack(fill='both', expand=True, pady=10)
        
        # Mostrar la sección básica por defecto
        self.show_prob_section("basics")
    
    def show_prob_section(self, section):
        """Muestra la sección de probabilidad seleccionada"""
        self.clear_frame(self.prob_section_frame)
        
        if section == "basics":
            self.show_basic_probabilities()
        elif section == "system_calc":
            self.show_system_calculations()
        elif section == "queue_calc":
            self.show_queue_calculations()
    
    def show_basic_probabilities(self):
        """Muestra las probabilidades básicas del sistema"""
        frame = tk.LabelFrame(self.prob_section_frame, text="Probabilidades Básicas del Sistema", padx=5, pady=5)
        frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        if self.model_type == "PICS":
            self.add_result_row(frame, "Probabilidad sistema ocupado (ρ):", self.model.rho_prob_sistema_ocupado())
            self.add_result_row(frame, "Probabilidad sistema desocupado (P0):", self.model.P0_prob_sistema_desocupado())
        elif self.model_type == "PICM":
            self.add_result_row(frame, "Probabilidad sistema vacío (P0):", self.model.P0_prob_sistema_vacio())
            self.add_result_row(frame, "Probabilidad sistema ocupado (Pk):", self.model.Pk_prob_sistema_ocupado())
            self.add_result_row(frame, "Probabilidad sistema desocupado (PNE):", self.model.PNE_prob_sistema_desocupado())
        elif self.model_type == "PFCS":
            self.add_result_row(frame, "Probabilidad sistema ocupado (PE):", self.model.PE_prob_sistema_ocupado())
            self.add_result_row(frame, "Probabilidad sistema desocupado (P0):", self.model.P0_prob_sistema_desocupado())
        elif self.model_type == "PFCM":
            self.add_result_row(frame, "Probabilidad sistema vacío (P0):", self.model.P0_prob_sistema_vacio())
            self.add_result_row(frame, "Probabilidad sistema ocupado (PE):", self.model.PE_prob_sistema_ocupado())
            self.add_result_row(frame, "Probabilidad sistema desocupado (PNE):", self.model.PNE_prob_sistema_desocupado())
    
    def show_system_calculations(self):
        """Muestra los cálculos de probabilidad en el sistema"""
        frame = tk.LabelFrame(self.prob_section_frame, text="Cálculos de Probabilidad en el Sistema", padx=5, pady=5)
        frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Probabilidad de exactamente n usuarios en el sistema
        frame_pn = tk.Frame(frame)
        frame_pn.pack(fill='x', pady=5)
        lbl_pn = tk.Label(frame_pn, text="Probabilidad de exactamente estos usuarios (separados por comas):")
        lbl_pn.pack(side='left', padx=5)
        self.entry_pn = tk.Entry(frame_pn, width=15)
        self.entry_pn.pack(side='left', padx=5)
        btn_pn = tk.Button(frame_pn, text="Calcular", command=self.calc_pn_system)
        btn_pn.pack(side='left', padx=5)
        self.lbl_pn_result = tk.Label(frame_pn, text="", justify='left')
        self.lbl_pn_result.pack(side='left', padx=5)
        
        # Probabilidad de máximo n usuarios en el sistema
        frame_pmax = tk.Frame(frame)
        frame_pmax.pack(fill='x', pady=5)
        lbl_pmax = tk.Label(frame_pmax, text="Probabilidad de máximo este número de usuarios:")
        lbl_pmax.pack(side='left', padx=5)
        self.entry_pmax = tk.Entry(frame_pmax, width=15)
        self.entry_pmax.pack(side='left', padx=5)
        btn_pmax = tk.Button(frame_pmax, text="Calcular", command=self.calc_pmax_system)
        btn_pmax.pack(side='left', padx=5)
        self.lbl_pmax_result = tk.Label(frame_pmax, text="", justify='left')
        self.lbl_pmax_result.pack(side='left', padx=5)
        
        # Probabilidad de al menos n usuarios en el sistema
        frame_pmin = tk.Frame(frame)
        frame_pmin.pack(fill='x', pady=5)
        lbl_pmin = tk.Label(frame_pmin, text="Probabilidad de al menos este número de usuarios:")
        lbl_pmin.pack(side='left', padx=5)
        self.entry_pmin = tk.Entry(frame_pmin, width=15)
        self.entry_pmin.pack(side='left', padx=5)
        btn_pmin = tk.Button(frame_pmin, text="Calcular", command=self.calc_pmin_system)
        btn_pmin.pack(side='left', padx=5)
        self.lbl_pmin_result = tk.Label(frame_pmin, text="", justify='left')
        self.lbl_pmin_result.pack(side='left', padx=5)
    
    def show_queue_calculations(self):
        """Muestra los cálculos de probabilidad en cola"""
        frame = tk.LabelFrame(self.prob_section_frame, text="Cálculos de Probabilidad en Cola", padx=5, pady=5)
        frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Probabilidad de exactamente n usuarios en cola
        frame_qn = tk.Frame(frame)
        frame_qn.pack(fill='x', pady=5)
        lbl_qn = tk.Label(frame_qn, text="Probabilidad de exactamente estos usuarios en cola (separados por comas):")
        lbl_qn.pack(side='left', padx=5)
        self.entry_qn = tk.Entry(frame_qn, width=15)
        self.entry_qn.pack(side='left', padx=5)
        btn_qn = tk.Button(frame_qn, text="Calcular", command=self.calc_qn_queue)
        btn_qn.pack(side='left', padx=5)
        self.lbl_qn_result = tk.Label(frame_qn, text="", justify='left')
        self.lbl_qn_result.pack(side='left', padx=5)
        
        # Probabilidad de máximo n usuarios en cola
        frame_qmax = tk.Frame(frame)
        frame_qmax.pack(fill='x', pady=5)
        lbl_qmax = tk.Label(frame_qmax, text="Probabilidad de máximo este número de usuarios en cola:")
        lbl_qmax.pack(side='left', padx=5)
        self.entry_qmax = tk.Entry(frame_qmax, width=15)
        self.entry_qmax.pack(side='left', padx=5)
        btn_qmax = tk.Button(frame_qmax, text="Calcular", command=self.calc_qmax_queue)
        btn_qmax.pack(side='left', padx=5)
        self.lbl_qmax_result = tk.Label(frame_qmax, text="", justify='left')
        self.lbl_qmax_result.pack(side='left', padx=5)
        
        # Probabilidad de al menos n usuarios en cola
        frame_qmin = tk.Frame(frame)
        frame_qmin.pack(fill='x', pady=5)
        lbl_qmin = tk.Label(frame_qmin, text="Probabilidad de al menos este número de usuarios en cola:")
        lbl_qmin.pack(side='left', padx=5)
        self.entry_qmin = tk.Entry(frame_qmin, width=15)
        self.entry_qmin.pack(side='left', padx=5)
        btn_qmin = tk.Button(frame_qmin, text="Calcular", command=self.calc_qmin_queue)
        btn_qmin.pack(side='left', padx=5)
        self.lbl_qmin_result = tk.Label(frame_qmin, text="", justify='left')
        self.lbl_qmin_result.pack(side='left', padx=5)
    
    def calc_pn_system(self):
        """Calcula P(n) usuarios en el sistema con valores únicos"""
        try:
            input_str = self.entry_pn.get().strip()
            if not input_str:
                self.lbl_pn_result.config(text="Ingrese valores")
                return
                
            # Obtener valores únicos
            values = list({int(x.strip()) for x in input_str.split(',') if x.strip()})
            values.sort()
            
            if not values:
                self.lbl_pn_result.config(text="Ingrese valores válidos")
                return
            
            prob = self.model.prob_usuarios_sistema(*values)
            
            # Construir detalles
            details = []
            total = 0
            for n in values:
                pn = self.model.Pn(n)
                details.append(f"P(n={n}) = {pn:.6f}")
                total += pn
            
            result_text = f"Resultado: {prob:.6f}\n" + "\n".join(details)
            self.lbl_pn_result.config(text=result_text)
            
        except ValueError:
            self.lbl_pn_result.config(text="Error: Ingrese números válidos")
        except Exception as e:
            self.lbl_pn_result.config(text=f"Error: {str(e)}")
    
    def calc_pmax_system(self):
        """Calcula P(≤n) usuarios en el sistema"""
        try:
            input_str = self.entry_pmax.get().strip()
            if not input_str:
                self.lbl_pmax_result.config(text="Ingrese valor")
                return
                
            value = int(input_str)
            prob = self.model.prob_max_usuarios_sistema(value)
            
            # Construir detalles
            details = []
            for n in range(value + 1):
                pn = self.model.Pn(n)
                details.append(f"P(n={n}) = {pn:.6f}")
            
            result_text = f"Resultado: {prob:.6f}\n" + "\n".join(details)
            self.lbl_pmax_result.config(text=result_text)
            
        except ValueError:
            self.lbl_pmax_result.config(text="Error: Ingrese un número válido")
        except Exception as e:
            self.lbl_pmax_result.config(text=f"Error: {str(e)}")
    
    def calc_pmin_system(self):
        """Calcula P(≥n) usuarios en el sistema"""
        try:
            input_str = self.entry_pmin.get().strip()
            if not input_str:
                self.lbl_pmin_result.config(text="Ingrese valor")
                return
                
            value = int(input_str)
            prob = self.model.prob_min_usuarios_sistema(value)
            self.lbl_pmin_result.config(text=f"Resultado: {prob:.6f}")
        except Exception as e:
            self.lbl_pmin_result.config(text=f"Error: {str(e)}")
    
    def calc_qn_queue(self):
        """Calcula P(n) usuarios en cola con valores únicos"""
        try:
            input_str = self.entry_qn.get().strip()
            if not input_str:
                self.lbl_qn_result.config(text="Ingrese valores")
                return
                
            # Obtener valores únicos
            values = list({int(x.strip()) for x in input_str.split(',') if x.strip()})
            values.sort()
            
            if not values:
                self.lbl_qn_result.config(text="Ingrese valores válidos")
                return
            
            prob = self.model.prob_usuarios_cola(*values)
            
            # Construir detalles
            details = []
            total = 0
            for n in values:
                pn = self.model.Pn(self.model.k + n)
                details.append(f"P(n={self.model.k + n}) = {pn:.6f}")
                total += pn
            
            result_text = f"Resultado: {prob:.6f}\n" + "\n".join(details)
            self.lbl_qn_result.config(text=result_text)
            
        except ValueError:
            self.lbl_qn_result.config(text="Error: Ingrese números válidos")
        except Exception as e:
            self.lbl_qn_result.config(text=f"Error: {str(e)}")
    
    def calc_qmax_queue(self):
        """Calcula P(≤n) usuarios en cola"""
        try:
            input_str = self.entry_qmax.get().strip()
            if not input_str:
                self.lbl_qmax_result.config(text="Ingrese valor")
                return
                
            value = int(input_str)
            prob = self.model.prob_max_usuarios_cola(value)
            
            # Construir detalles
            details = []
            for n in range(self.model.k, self.model.k + value + 1):
                pn = self.model.Pn(n)
                details.append(f"P(n={n}) = {pn:.6f}")
            
            result_text = f"Resultado: {prob:.6f}\n" + "\n".join(details)
            self.lbl_qmax_result.config(text=result_text)
            
        except ValueError:
            self.lbl_qmax_result.config(text="Error: Ingrese un número válido")
        except Exception as e:
            self.lbl_qmax_result.config(text=f"Error: {str(e)}")
    
    def calc_qmin_queue(self):
        """Calcula P(≥n) usuarios en cola"""
        try:
            input_str = self.entry_qmin.get().strip()
            if not input_str:
                self.lbl_qmin_result.config(text="Ingrese valor")
                return
                
            value = int(input_str)
            prob = self.model.prob_min_usuarios_cola(value)
            self.lbl_qmin_result.config(text=f"Resultado: {prob:.6f}")
        except Exception as e:
            self.lbl_qmin_result.config(text=f"Error: {str(e)}")
    
    def create_metrics_tab(self, parent):
        """Crea la pestaña de métricas"""
        # Número de clientes
        lbl_clients = tk.Label(parent, text="Número Esperado de Clientes", font=('Arial', 10, 'bold'))
        lbl_clients.pack(pady=5, anchor='w')
        
        self.add_result_row(parent, "En el sistema (L):", self.model.L())
        self.add_result_row(parent, "En la cola (Lq):", self.model.Lq())
        if hasattr(self.model, 'Ln'):
            self.add_result_row(parent, "En cola no vacía (Ln):", self.model.Ln())
        
        # Tiempos de espera
        lbl_times = tk.Label(parent, text="Tiempos Esperados de Espera", font=('Arial', 10, 'bold'))
        lbl_times.pack(pady=5, anchor='w')
        
        self.add_result_row(parent, "En el sistema (W):", self.model.W())
        self.add_result_row(parent, "En la cola (Wq):", self.model.Wq())
        if hasattr(self.model, 'Wn'):
            self.add_result_row(parent, "En cola no vacía (Wn):", self.model.Wn())
    
    def create_cost_tab(self, parent):
        """Crea la pestaña de costos (para modelos infinitos)"""
        # Frame para ingresar costos y horas laborables
        cost_input_frame = tk.Frame(parent)
        cost_input_frame.pack(pady=10)
        
        # Agregar campo para horas laborables
        lbl_hrlab = tk.Label(cost_input_frame, text="Horas laborables al día (hrlab):")
        lbl_hrlab.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_hrlab = tk.Entry(cost_input_frame)
        self.entry_hrlab.grid(row=0, column=1, padx=5, pady=5)
        self.entry_hrlab.insert(0, "8")  # Valor por defecto: 8 horas
        
        lbl_cte = tk.Label(cost_input_frame, text="Costo espera en cola (CTE):")
        lbl_cte.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_cte = tk.Entry(cost_input_frame)
        self.entry_cte.grid(row=1, column=1, padx=5, pady=5)
        
        lbl_cts = tk.Label(cost_input_frame, text="Costo tiempo sistema (CTS):")
        lbl_cts.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.entry_cts = tk.Entry(cost_input_frame)
        self.entry_cts.grid(row=2, column=1, padx=5, pady=5)
        
        lbl_ctse = tk.Label(cost_input_frame, text="Costo tiempo servicio (CTSE):")
        lbl_ctse.grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.entry_ctse = tk.Entry(cost_input_frame)
        self.entry_ctse.grid(row=3, column=1, padx=5, pady=5)
        
        lbl_cs = tk.Label(cost_input_frame, text="Costo servidor (CS):")
        lbl_cs.grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.entry_cs = tk.Entry(cost_input_frame)
        self.entry_cs.grid(row=4, column=1, padx=5, pady=5)
        
        btn_calc_cost = tk.Button(parent, text="Calcular Costos", command=self.show_cost_results)
        btn_calc_cost.pack(pady=10)
        
        # Frame para resultados de costos
        self.cost_result_frame = tk.Frame(parent)
        self.cost_result_frame.pack(fill='both', expand=True, padx=10, pady=5)

    def show_cost_results(self):
        """Muestra los resultados de costos"""
        self.clear_frame(self.cost_result_frame)
        
        try:
            # Obtener y establecer horas laborables
            hrlab = float(self.entry_hrlab.get()) if self.entry_hrlab.get() else 8
            self.model.set_hrlab(hrlab)
            
            # Obtener los demás parámetros de costo
            cte = float(self.entry_cte.get()) if self.entry_cte.get() else 0
            cts = float(self.entry_cts.get()) if self.entry_cts.get() else 0
            ctse = float(self.entry_ctse.get()) if self.entry_ctse.get() else 0
            cs = float(self.entry_cs.get()) if self.entry_cs.get() else 0
            
            # Mostrar las horas laborables usadas
            self.add_result_row(self.cost_result_frame, "Horas laborables al día:", f"{hrlab} horas")
            
            # Mostrar los resultados de costos con formato de moneda
            self.add_result_row(self.cost_result_frame, "Costo diario espera en cola (CTE):", 
                            f"${self.model.CTE_costo_diario_espera_cola(cte):.2f}")
            self.add_result_row(self.cost_result_frame, "Costo diario tiempo en sistema (CTS):", 
                            f"${self.model.CTS_costo_diario_tiempo_sistema(cts):.2f}")
            self.add_result_row(self.cost_result_frame, "Costo diario tiempo en servicio (CTSE):", 
                            f"${self.model.CTSE_costo_diario_servicio(ctse):.2f}")
            self.add_result_row(self.cost_result_frame, "Costo diario servidor (CS):", 
                            f"${self.model.CS_costo_diario_servidor(cs):.2f}")
            self.add_result_row(self.cost_result_frame, "COSTO TOTAL DIARIO:", 
                            f"${self.model.costo_total_diario(cte, cts, ctse, cs):.2f}", bold=True)
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al calcular costos: {str(e)}")
            
    def add_result_row(self, parent, label, value, bold=False):
        """Añade una fila de resultado a la interfaz"""
        frame = tk.Frame(parent)
        frame.pack(fill='x', padx=5, pady=2)
        
        lbl = tk.Label(frame, text=label, anchor='w')
        if bold:
            lbl.config(font=('Arial', 9, 'bold'))
        lbl.pack(side='left', padx=5)
        
        if isinstance(value, (int, float)):
            value_str = f"{value:.6f}"
        else:
            value_str = str(value)
            
        val = tk.Label(frame, text=value_str, anchor='e')
        if bold:
            val.config(font=('Arial', 9, 'bold'))
        val.pack(side='right', padx=5)
    
    def clear_window(self):
        """Limpia la ventana principal"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def clear_frame(self, frame):
        """Limpia un frame específico"""
        for widget in frame.winfo_children():
            widget.destroy()

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = QueueTheoryApp(root)
    root.mainloop()