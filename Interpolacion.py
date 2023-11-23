import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp

class AplicacionInterpolacion:
    def __init__(self):
        self.X = sp.symbols('X')

        # Configuración de la interfaz gráfica
        self.window = tk.Tk()
        self.window.title("INTERFAZ PARA INTERPOLACIÓN")

        self.x_entry = None
        self.y_entry = None
        self.eval_entry = None
        self.method_var = None
        self.calculate_button = None
        self.clear_button = None
        self.result_label = None
        self.eval_result_label = None
        self.empty_canvas_widget = None

        self.create_widgets()

    def create_widgets(self):
        x_label = ttk.Label(self.window, text="Ingrese los valores de X (separados por coma):")
        x_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.x_entry = ttk.Entry(self.window)
        self.x_entry.grid(row=0, column=1, padx=10, pady=5)

        y_label = ttk.Label(self.window, text="Ingrese los valores de Y (separados por coma):")
        y_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.y_entry = ttk.Entry(self.window)
        self.y_entry.grid(row=1, column=1, padx=10, pady=5)

        eval_label = ttk.Label(self.window, text="Ingrese el valor de X a evaluar:")
        eval_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        self.eval_entry = ttk.Entry(self.window)
        self.eval_entry.grid(row=2, column=1, padx=10, pady=5)

        method_label = ttk.Label(self.window, text="Seleccione el método:")
        method_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        self.method_var = tk.StringVar()
        method_combobox = ttk.Combobox(self.window, textvariable=self.method_var, values=["lagrange", "minimos_cuadrados", "p_simple"])
        method_combobox.grid(row=3, column=1, padx=10, pady=5)
        method_combobox.set("lagrange")

        self.calculate_button = ttk.Button(self.window, text="Calcular", command=self.calculate_result)
        self.calculate_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.clear_button = ttk.Button(self.window, text="Borrar Datos", command=self.clear_entries)
        self.clear_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.result_label = ttk.Label(self.window, text="")
        self.result_label.grid(row=6, column=0, columnspan=2, pady=10)

        self.eval_result_label = ttk.Label(self.window, text="")
        self.eval_result_label.grid(row=7, column=0, columnspan=2, pady=10)

        # Agregar gráfica inicial vacía
        empty_plt = self.plot_graph([], [], lambda x: 0, method_name="Método")
        empty_canvas = FigureCanvasTkAgg(empty_plt.gcf(), master=self.window)
        self.empty_canvas_widget = empty_canvas.get_tk_widget()
        self.empty_canvas_widget.grid(row=0, column=5, rowspan=7, padx=10, pady=10)

    def lagrange(self, xdata, ydata):
        N = len(xdata)
        P = 0
        for i in range(N):
            T = 1
            for j in range(N):
                if j != i:
                    T = T * (self.X - xdata[j]) / (xdata[i] - xdata[j])
            P = P + T * ydata[i]
        return sp.lambdify(self.X, P)

    def minimos_cuadrados(self, x, y):
        x = np.array(x)
        y = np.array(y)
        m = len(x)
        sx = sum(x)
        sy = sum(y)
        sx2 = sx**2
        sxy = np.sum(x*y)
        scx = np.sum(x**2)
        a0 = (sy * scx - sx * sxy) / (m * scx - sx2)
        a1 = (m * sxy - sx * sy) / (m * scx - sx2)
        return a0, a1

    def p_simple(self, xdata, ydata):
        N = len(xdata)
        M = np.vander(xdata, N, increasing=True)
        try:
            ai = np.linalg.solve(M, ydata)
            P = sum(ai[i] * self.X**i for i in range(N))
            return sp.lambdify(self.X, P)
        except np.linalg.LinAlgError:
            return None

    def plot_graph(self, xdata, ydata, poly_func, eval_x=None, method_name="Método"):
        plt.clf()  # Limpiar la figura antes de agregar nuevos datos

        if not xdata:
            x_vals = np.linspace(0, 1, 1000)  # Aumentar la cantidad de puntos para suavizar la curva
        else:
            x_vals = np.linspace(min(xdata), max(xdata), 1000)

        y_vals = np.zeros_like(x_vals)
        for i, x_val in enumerate(x_vals):
            y_vals[i] = poly_func(x_val)

        plt.scatter(xdata, ydata, label='Datos', color='blue')

        if method_name != "Mínimos Cuadrados":
            plt.plot(x_vals, y_vals, label=f'Polinomio Interpolante ({method_name})', color='red')

        if eval_x is not None:
            eval_y = poly_func(eval_x)
            plt.scatter([eval_x], [eval_y], color='green', marker='o', label=f'Evaluación en X={eval_x}')

        plt.title(f'Interpolación Polinómica - {method_name}')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.grid(True)

        return plt

    def calculate_result(self):
        try:
            xdata = list(map(float, self.x_entry.get().split(',')))
            ydata = list(map(float, self.y_entry.get().split(',')))

            selected_method = self.method_var.get()

            if selected_method == "lagrange":
                poly_func = self.lagrange(xdata, ydata)
                method_name = "Lagrange"
            elif selected_method == "minimos_cuadrados":
                a0, a1 = self.minimos_cuadrados(xdata, ydata)
                method_name = "Mínimos Cuadrados"
                self.result_label.config(text=f"a0: {a0}, a1: {a1}")
                self.minimos_cuadrados_plot(xdata, ydata, a0, a1)
                return
            elif selected_method == "p_simple":
                poly_func = self.p_simple(xdata, ydata)
                if poly_func is None:
                    raise ValueError("No se puede calcular el método de Polinomio Simple con los datos proporcionados.")
                method_name = "Polinomio Simple"

            self.result_label.config(text=f"Polinomio: {poly_func(self.X)}")

            eval_x_value = self.eval_entry.get()
            if eval_x_value:
                eval_x = float(eval_x_value)
                eval_result = poly_func(eval_x)
                self.eval_result_label.config(text=f"Evaluación en X={eval_x}: {eval_result}")
            else:
                self.eval_result_label.config(text="")

            plt = self.plot_graph(xdata, ydata, poly_func, eval_x, method_name)
            canvas = FigureCanvasTkAgg(plt.gcf(), master=self.window)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.grid(row=0, column=5, rowspan=7, padx=10, pady=10)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def minimos_cuadrados_plot(self, xdata, ydata, a0, a1):
        plt = self.plot_graph(xdata, ydata, lambda x: a0 + a1 * x, method_name="Mínimos Cuadrados")
        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=5, rowspan=7, padx=10, pady=10)

    def clear_entries(self):
        self.x_entry.delete(0, tk.END)
        self.y_entry.delete(0, tk.END)
        self.eval_entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.eval_result_label.config(text="")

        # Limpiar la gráfica
        plt = self.plot_graph([], [], lambda x: 0, method_name="Método")
        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=5, rowspan=7, padx=10, pady=10)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = AplicacionInterpolacion()
    app.run()
