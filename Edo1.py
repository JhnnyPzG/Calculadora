import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class AplicacionEDO1:
    def __init__(self, root):
        self.root = root
        self.root.title("INTERFAZ PARA ECUACIONES DIFERENCIALES 1")

        # Variables de seguimiento
        self.method_var = tk.StringVar()
        self.method_var.set("Euler")
        self.method_var.trace_add('write', self.update_method)

        # Configuración del estilo de la interfaz
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 10))  # Fuente más pequeña
        self.style.configure('TButton', font=('Arial', 10))  # Fuente más pequeña
        self.style.configure('TEntry', font=('Arial', 10))  # Fuente más pequeña

        self.create_widgets()

    def create_widgets(self):
        # Crear y organizar los widgets
        self.method_label = ttk.Label(self.root, text="Método:")
        self.method_combobox = ttk.Combobox(self.root, textvariable=self.method_var, values=["Euler", "Runge-Kutta"])
        self.f_label = ttk.Label(self.root, text="Función f(t, y):")
        self.f_entry = ttk.Entry(self.root, width=20)  # Reducción del ancho del Entry
        self.Y_label = ttk.Label(self.root, text="Función Y(t):")
        self.Y_entry = ttk.Entry(self.root, width=20)  # Reducción del ancho del Entry
        self.a_label = ttk.Label(self.root, text="a:")
        self.a_entry = ttk.Entry(self.root, width=10)
        self.b_label = ttk.Label(self.root, text="b:")
        self.b_entry = ttk.Entry(self.root, width=10)
        self.h_label = ttk.Label(self.root, text="h:")
        self.h_entry = ttk.Entry(self.root, width=10)
        self.co_label = ttk.Label(self.root, text="Condición Inicial:")
        self.co_entry = ttk.Entry(self.root, width=10)
        self.calculate_button = ttk.Button(self.root, text="Calcular", command=self.calculate)
        self.clear_button = ttk.Button(self.root, text="Borrar Datos", command=self.clear_data)

        self.result_label = ttk.Label(self.root, text="", font=('Arial', 10))  
        self.result_label.grid(row=8, column=0, columnspan=3, pady=5) 

        # Configurar el diseño de la cuadrícula
        self.method_label.grid(row=0, column=0, padx=5, pady=5, sticky="E")  
        self.method_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="W")  
        self.f_label.grid(row=1, column=0, padx=5, pady=5, sticky="E")  
        self.f_entry.grid(row=1, column=1, padx=5, pady=5, sticky="W")  
        self.Y_label.grid(row=2, column=0, padx=5, pady=5, sticky="E")  
        self.Y_entry.grid(row=2, column=1, padx=5, pady=5, sticky="W")  
        self.a_label.grid(row=3, column=0, padx=5, pady=5, sticky="E")  
        self.a_entry.grid(row=3, column=1, padx=5, pady=5, sticky="W")  
        self.b_label.grid(row=4, column=0, padx=5, pady=5, sticky="E")  
        self.b_entry.grid(row=4, column=1, padx=5, pady=5, sticky="W")  
        self.h_label.grid(row=5, column=0, padx=5, pady=5, sticky="E")  
        self.h_entry.grid(row=5, column=1, padx=5, pady=5, sticky="W")  
        self.co_label.grid(row=6, column=0, padx=5, pady=5, sticky="E")  
        self.co_entry.grid(row=6, column=1, padx=5, pady=5, sticky="W")  
        self.calculate_button.grid(row=7, columnspan=2, pady=10)
        self.clear_button.grid(row=8, column=2, pady=5)  

        # Configuración adicional para el lienzo de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(6, 4)) 
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=2, rowspan=9, padx=5, pady=5, sticky="nsew") 

        # Configuración de la expansión del grid
        self.root.columnconfigure((0, 1), weight=1)
        self.root.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        # Configuración de la separación de columnas
        self.root.columnconfigure(2, minsize=150)  # Reducción del ancho de la columna 2

        # Configuración adicional
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.root.geometry("900x500")  # Reducción del tamaño de la ventana
        self.root.mainloop()

    def update_method(self, *args):
        self.ax.clear()
        self.canvas.draw()

    def calculate(self):
        self.plot_graph(
            lambda t, y: eval(self.f_entry.get()),
            lambda t: eval(self.Y_entry.get()),
            float(self.a_entry.get()), float(self.b_entry.get()), float(self.h_entry.get()), float(self.co_entry.get()), lambda t: 0
        )

    def Euler(self, f, a, b, h, co):
        n = int((b - a) / h)
        t = np.linspace(a, b, n + 1)
        yeu = [co]
        for i in range(n):
            yeu.append(yeu[i] + h * f(t[i], yeu[i]))
        return t, yeu

    def Runge4(self, f, a, b, h, co):
        n = int((b - a) / h)
        t = np.linspace(a, b, n + 1)
        yk = [co]
        for i in range(n):
            k1 = h * f(t[i], yk[i])
            k2 = h * f(t[i] + h / 2, yk[i] + 1 / 2 * k1)
            k3 = h * f(t[i] + h / 2, yk[i] + 1 / 2 * k2)
            k4 = h * f(t[i + 1], yk[i] + k3)
            yk.append(yk[i] + 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4))
        return t, yk

    def plot_graph(self, f, Y, a, b, h, co, Y_exact):
        method = self.method_var.get()

        if method == "Euler":
            t, yeu = self.Euler(f, a, b, h, co)
        elif method == "Runge-Kutta":
            t, yeu = self.Runge4(f, a, b, h, co)

        self.ax.clear()
        self.ax.plot(t, yeu, 'md', label=f'{method} Aproximada (f)')
        self.ax.plot(t, Y(t), 'b', label=f'{method} Exacta (Y)')
        self.ax.set_xlabel('t')
        self.ax.set_ylabel('Y(t)')
        self.ax.legend()
        self.ax.grid(True)
        self.ax.set_title('Gráfica de la Solución')
        self.canvas.draw()

        self.result_label.config(
            text=f'Tiempo: {t}\nSolución Aproximada: {t, yeu}\nSolución Exacta: {t, Y(t)}')

    def clear_data(self):
        self.f_entry.delete(0, tk.END)
        self.Y_entry.delete(0, tk.END)
        self.a_entry.delete(0, tk.END)
        self.b_entry.delete(0, tk.END)
        self.h_entry.delete(0, tk.END)
        self.co_entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.ax.clear()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionEDO1(root)
    root.mainloop()
