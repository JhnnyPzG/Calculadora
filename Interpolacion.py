import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp

# Definir la variable simbólica
X = sp.symbols('X')

# Métodos proporcionados
def lagrange(xdata, ydata):
    N = len(xdata)
    P = 0
    for i in range(N):
        T = 1
        for j in range(N):
            if j != i:
                T = T * (X - xdata[j]) / (xdata[i] - xdata[j])
        P = P + T * ydata[i]
    return sp.lambdify(X, P)

def minimos_cuadrados(x, y):
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

def p_simple(xdata, ydata, degree):
    N = len(xdata)
    M = np.zeros([N, degree + 1])
    P = 0
    for i in range(N):
        for j in range(degree + 1):
            M[i, j] = xdata[i] ** j
    try:
        ai = np.linalg.solve(M, ydata)
        P = sum(ai[i] * X**i for i in range(degree + 1))
        return sp.lambdify(X, P)
    except np.linalg.LinAlgError:
        return None

# Función para graficar
def plot_graph(xdata, ydata, poly_func, eval_x=None, method_name="Método"):
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

# Función principal para la interfaz gráfica
def main():
    def calculate_result():
        try:
            xdata = list(map(float, x_entry.get().split(',')))
            ydata = list(map(float, y_entry.get().split(',')))
            degree = int(degree_var.get())

            selected_method = method_var.get()

            if selected_method == "lagrange":
                poly_func = lagrange(xdata, ydata)
                method_name = "Lagrange"
            elif selected_method == "minimos_cuadrados":
                a0, a1 = minimos_cuadrados(xdata, ydata)
                method_name = "Mínimos Cuadrados"
                result_label.config(text=f"a0: {a0}, a1: {a1}")
                minimos_cuadrados_plot(xdata, ydata, a0, a1)
                return
            elif selected_method == "p_simple":
                poly_func = p_simple(xdata, ydata, degree)
                if poly_func is None:
                    raise ValueError("No se puede calcular el método de Polinomio Simple con los datos proporcionados.")
                method_name = "Polinomio Simple"

            result_label.config(text=f"Polinomio: {poly_func(X)}")

            eval_x_value = eval_entry.get()
            if eval_x_value:
                eval_x = float(eval_x_value)
                eval_result = poly_func(eval_x)
                eval_result_label.config(text=f"Evaluación en X={eval_x}: {eval_result}")
            else:
                eval_result_label.config(text="")

            plt = plot_graph(xdata, ydata, poly_func, eval_x, method_name)
            canvas = FigureCanvasTkAgg(plt.gcf(), master=window)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.grid(row=0, column=5, rowspan=7, padx=10, pady=10)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def minimos_cuadrados_plot(xdata, ydata, a0, a1):
        plt = plot_graph(xdata, ydata, lambda x: a0 + a1 * x, method_name="Mínimos Cuadrados")
        canvas = FigureCanvasTkAgg(plt.gcf(), master=window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=5, rowspan=7, padx=10, pady=10)

    def clear_entries():
        x_entry.delete(0, tk.END)
        y_entry.delete(0, tk.END)
        degree_entry.delete(0, tk.END)
        eval_entry.delete(0, tk.END)
        result_label.config(text="")
        eval_result_label.config(text="")

        # Limpiar la gráfica
        plt = plot_graph([], [], lambda x: 0, method_name="Método")
        canvas = FigureCanvasTkAgg(plt.gcf(), master=window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=5, rowspan=7, padx=10, pady=10)

    # Configuración de la interfaz gráfica
    window = tk.Tk()
    window.title("INTERFAZ PARA INTERPOLACIÓN")

    x_label = ttk.Label(window, text="Ingrese los valores de X (separados por coma):")
    x_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

    x_entry = ttk.Entry(window)
    x_entry.grid(row=0, column=1, padx=10, pady=5)

    y_label = ttk.Label(window, text="Ingrese los valores de Y (separados por coma):")
    y_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

    y_entry = ttk.Entry(window)
    y_entry.grid(row=1, column=1, padx=10, pady=5)

    degree_label = ttk.Label(window, text="Ingrese el grado del polinomio:")
    degree_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

    degree_var = tk.StringVar()
    degree_entry = ttk.Entry(window, textvariable=degree_var)
    degree_entry.grid(row=2, column=1, padx=10, pady=5)

    eval_label = ttk.Label(window, text="Ingrese el valor de X a evaluar:")
    eval_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

    eval_entry = ttk.Entry(window)
    eval_entry.grid(row=3, column=1, padx=10, pady=5)

    method_label = ttk.Label(window, text="Seleccione el método:")
    method_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

    method_var = tk.StringVar()
    method_combobox = ttk.Combobox(window, textvariable=method_var, values=["lagrange", "minimos_cuadrados", "p_simple"])
    method_combobox.grid(row=4, column=1, padx=10, pady=5)
    method_combobox.set("lagrange")

    calculate_button = ttk.Button(window, text="Calcular", command=calculate_result)
    calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

    clear_button = ttk.Button(window, text="Borrar Datos", command=clear_entries)
    clear_button.grid(row=6, column=0, columnspan=2, pady=10)

    result_label = ttk.Label(window, text="")
    result_label.grid(row=7, column=0, columnspan=2, pady=10)

    eval_result_label = ttk.Label(window, text="")
    eval_result_label.grid(row=8, column=0, columnspan=2, pady=10)

    # Agregar gráfica inicial vacía
    empty_plt = plot_graph([], [], lambda x: 0, method_name="Método")
    empty_canvas = FigureCanvasTkAgg(empty_plt.gcf(), master=window)
    empty_canvas_widget = empty_canvas.get_tk_widget()
    empty_canvas_widget.grid(row=0, column=5, rowspan=7, padx=10, pady=10)

    window.mainloop()

if __name__ == "__main__":
    main()
