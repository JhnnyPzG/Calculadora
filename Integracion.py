import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AplicacionIntegracion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("INTERFAZ PARA INTEGRACIÓN")
        self.geometry("800x450")

        self.label_func = ttk.Label(self, text="Ingrese la función (utilice 'np.' para funciones de NumPy):")
        self.label_func.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        self.entry_func = ttk.Entry(self, width=40)
        self.entry_func.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        self.label_a = ttk.Label(self, text="Valor de a:")
        self.label_a.grid(row=2, column=0, padx=10, pady=5)
        self.entry_a = ttk.Entry(self)
        self.entry_a.grid(row=2, column=1, padx=10, pady=5)

        self.label_b = ttk.Label(self, text="Valor de b:")
        self.label_b.grid(row=3, column=0, padx=10, pady=5)
        self.entry_b = ttk.Entry(self)
        self.entry_b.grid(row=3, column=1, padx=10, pady=5)

        self.label_n = ttk.Label(self, text="Valor de n:")
        self.label_n.grid(row=4, column=0, padx=10, pady=5)
        self.entry_n = ttk.Entry(self)
        self.entry_n.grid(row=4, column=1, padx=10, pady=5)

        self.method_var = tk.StringVar()
        self.method_var.set("Trapecio")

        self.method_label = ttk.Label(self, text="Seleccione el método:")
        self.method_label.grid(row=5, column=0, columnspan=2, pady=5)

        self.method_combobox = ttk.Combobox(self, values=["Trapecio", "Simpson 1/3", "Simpson 3/8"], textvariable=self.method_var)
        self.method_combobox.grid(row=6, column=0, columnspan=2, pady=5)

        self.result_label = ttk.Label(self, text="")
        self.result_label.grid(row=7, column=0, columnspan=2, pady=10)

        self.button_calculate = ttk.Button(self, text="Calcular", command=self.calculate_integral)
        self.button_calculate.grid(row=8, column=0, columnspan=2, pady=10)

        # Configurar el gráfico
        self.figure, self.ax = plt.subplots(figsize=(4, 4), dpi=100)
        self.ax.set_facecolor('#f0f0f0')  # Color de fondo
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=2, rowspan=9, padx=10, pady=10)

    def Trapecio(self, f, a, b, n):
        h = (b - a) / n
        S = 0
        for i in range(1, n):
            S += f(a + i * h)
        Int = (h / 2) * (f(a) + 2 * S + f(b))
        return Int

    def sims13(self, f, a, b, n):
        if (n % 2 == 0):
            sum_par = 0
            sum_imp = 0
            h = (b - a) / n
            for i in range(1, n):
                if (i % 2 == 0):
                    sum_par = f(a + i * h)
                else:
                    sum_imp = f(a + i * h)
            Int = (h / 3) * (f(a) + 4 * sum_imp + 2 * sum_par + f(b))
            return Int
        else:
            raise ValueError('No se puede calcular la integral por este método. ¡n debe ser un número par!')

    def sims38(self, f, a, b, n):
        if (n % 3 == 0):
            sum_mult3 = 0
            sum_n = 0
            h = (b - a) / n
            for i in range(1, n):
                if (i % 3 == 0):
                    sum_mult3 = f(a + i * h)
                else:
                    sum_n = f(a + i * h)
            Int = (3 * h / 8) * (f(a) + 3 * sum_n + 2 * sum_mult3 + f(b))
            return Int
        else:
            raise ValueError('No se puede calcular la integral por este método. ¡n debe ser un múltiplo de 3!')

    def get_values(self):
        try:
            func_str = self.entry_func.get()
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())
            n = int(self.entry_n.get())
            method = self.method_var.get()
            return func_str, a, b, n, method
        except ValueError:
            tk.messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")
            return None

    def calculate_integral(self):
        values = self.get_values()
        if values is not None:
            func_str, a, b, n, method = values
            try:
                f = lambda x: eval(func_str, {"np": np}, {"x": x})
                # Calcular integral
                if method == "Trapecio":
                    result = self.Trapecio(f, a, b, n)
                elif method == "Simpson 1/3":
                    result = self.sims13(f, a, b, n)
                elif method == "Simpson 3/8":
                    result = self.sims38(f, a, b, n)
                else:
                    raise ValueError("Método de integración no válido.")

                # Actualizar etiqueta de resultado
                self.result_label.config(text=f"El resultado de la integral por {method} es: {result}")

                # Graficar la función
                x_vals = np.linspace(a, b, 100)
                y_vals = f(x_vals)
                self.ax.clear()
                self.ax.plot(x_vals, y_vals, label="Función", color='blue', linewidth=2)
                self.ax.legend()
                self.ax.set_xlabel("x")
                self.ax.set_ylabel("f(x)")
                self.ax.set_title("Gráfico de la función")
                self.ax.set_facecolor('#f0f0f0')  # Color de fondo
                self.ax.grid(True, linestyle='--', alpha=0.7)

                # Actualizar el gráfico en la interfaz
                self.canvas.draw()

            except Exception as e:
                tk.messagebox.showerror("Error", f"Error al evaluar la función: {e}")

if __name__ == "__main__":
    app = AplicacionIntegracion()
    app.mainloop()
