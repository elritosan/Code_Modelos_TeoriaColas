import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
from pathlib import Path

class AppIntegrador:
    def __init__(self, root):
        self.root = root
        self.root.title("Integrador de Modelos de Teoría de Colas")
        self.root.geometry("500x450")
        
        # Ruta base del proyecto
        self.base_path = Path(__file__).parent.parent
        
        # Diccionario de aplicaciones
        self.apps = {
            "PICS": {
                "name": "PICS (M/M/1)",
                "path": self.base_path / "CalculadoraPICS" / "AppPICS.py",
                "color": "#4CAF50"
            },
            "PICM": {
                "name": "PICM (M/M/k)",
                "path": self.base_path / "CalculadoraPICM" / "AppPICM.py",
                "color": "#2196F3"
            },
            "PFCS": {
                "name": "PFCS (M/M/1/M)",
                "path": self.base_path / "CalculadoraPFCS" / "AppPFCS.py",
                "color": "#FF9800"
            },
            "PFCM": {
                "name": "PFCM (M/M/k/M)",
                "path": self.base_path / "CalculadoraPFCM" / "AppPFCM.py",
                "color": "#9C27B0"
            }
        }
        
        self.create_interface()

    def create_interface(self):
        """Crea la interfaz del integrador"""
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        tk.Label(main_frame, 
                text="Seleccione el Modelo de Cola a Ejecutar",
                font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Frame para los botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        # Botón para lanzar todas las aplicaciones
        tk.Button(btn_frame, 
                 text="Iniciar TODAS las aplicaciones",
                 command=self.launch_all_apps,
                 bg="#333", fg="white",
                 height=2, font=('Arial', 10, 'bold')).pack(pady=10, fill=tk.X)
        
        # Botones individuales
        for model, data in self.apps.items():
            tk.Button(main_frame, 
                     text=f"Iniciar {data['name']}",
                     command=lambda m=model: self.launch_app(m),
                     bg=data['color'], fg="white",
                     height=2, width=25).pack(pady=5)
        
        # Botón para salir
        tk.Button(main_frame, 
                 text="Salir",
                 command=self.root.destroy,
                 bg="#f44336", fg="white",
                 height=2).pack(pady=(20, 0), fill=tk.X)

    def launch_app(self, model):
        """Lanza la aplicación correspondiente al modelo seleccionado"""
        try:
            app_data = self.apps.get(model)
            if not app_data or not app_data['path'].exists():
                raise FileNotFoundError(f"No se encontró la aplicación para {model}")
            
            # Comando para ejecutar la aplicación
            cmd = [sys.executable, str(app_data['path'])]
            
            # Ejecutar en una nueva ventana
            if os.name == 'nt':  # Windows
                subprocess.Popen(['start', 'cmd', '/k'] + cmd, shell=True)
            elif os.name == 'posix':  # Linux/Mac
                subprocess.Popen(['x-terminal-emulator', '-e'] + cmd)
            else:
                subprocess.Popen(cmd)
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar {model}:\n{str(e)}")

    def launch_all_apps(self):
        """Lanza todas las aplicaciones simultáneamente"""
        for model in self.apps.keys():
            self.launch_app(model)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppIntegrador(root)
    root.mainloop()