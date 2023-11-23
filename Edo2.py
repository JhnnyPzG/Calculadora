import tkinter as tk
from tkinter import Label, Entry, Button, ttk, Text, Scrollbar
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def main_EDO2():
    def euler_sis(f, a, b, h, co):
        n = int((b - a) / h)
        t = np.linspace(a, b, n+1)
        S = [co]
        for i in range(n):
            S.append(S[i] + h * f(t[i], S[i]))      
        return t, np.array(S)

    def rk4_vec(f, a, b, h, var):
        n = int((b - a) / h)
        t = np.linspace(a, b, n+1)
        w = [var]
        for i in range(0, n):
            k1 = h * f(t[i], w[i])
            k2 = h * f(t[i] + h/2, w[i] + k1/2)
            k3 = h * f(t[i] + h/2, w[i] + k2/2)
            k4 = h * f(t[i+1], w[i] + k3)
            w.append(w[i] + (1/6) * (k1 + 2*k2 + 2*k3 + k4))
        w = np.array(w)
        return t, w

    def plot_results():
        # Obtener valores de la interfaz gráfica
        a_val = float(eval(a_entry.get()))
        b_val = float(eval(b_entry.get()))
        h_val = float(eval(h_entry.get()))
        co_val = eval(co_entry.get())
        var_val = eval(var_entry.get())
        method = method_var.get()

        # Calcular soluciones utilizando el método seleccionado
        if method == "Euler":
            t, sol = euler_sis(f, a_val, b_val, h_val, co_val)
        elif method == "Runge-Kutta":
            t, sol = rk4_vec(f, a_val, b_val, h_val, var_val)
        else:
            raise ValueError("Método no reconocido")

        # Crear una nueva figura
        fig, ax = plt.subplots()
        ax.plot(t, sol)
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Solución')
        ax.set_title(f'Resultados usando {method}')

        # Mostrar la nueva gráfica en la interfaz
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=2, rowspan=10)

        # Destruir el widget de la gráfica anterior si existe
        if hasattr(plot_results, 'canvas_widget'):
            plot_results.canvas_widget.destroy()

        # Almacenar el widget de la gráfica actual para poder destruirlo la próxima vez
        plot_results.canvas_widget = canvas_widget

        # Mostrar soluciones numéricas en el área de texto
        results_text.config(state=tk.NORMAL)
        results_text.delete(1.0, tk.END)
        results_text.insert(tk.END, f"Tiempo: {t}\n\nSoluciones:\n{sol}")
        results_text.config(state=tk.DISABLED)

    # Función de sistema de ecuaciones diferenciales de ejemplo
    def f(t, y):
        return y  # Puedes cambiar esta función según tus necesidades

    # Crear la interfaz gráfica
    window = tk.Tk()
    window.title("INTERFAZ PARA ECUACIONES DIFERENCIALES 2")

    # Etiquetas y campos de entrada
    Label(window, text="Valor inicial (a):").grid(row=0, column=0)
    a_entry = Entry(window)
    a_entry.grid(row=0, column=1)

    Label(window, text="Valor final (b):").grid(row=1, column=0)
    b_entry = Entry(window)
    b_entry.grid(row=1, column=1)

    Label(window, text="Tamaño del paso (h):").grid(row=2, column=0)
    h_entry = Entry(window)
    h_entry.grid(row=2, column=1)

    Label(window, text="Condición inicial (co):").grid(row=3, column=0)
    co_entry = Entry(window)
    co_entry.grid(row=3, column=1)

    Label(window, text="Condición inicial para RK4 (var):").grid(row=4, column=0)
    var_entry = Entry(window)
    var_entry.grid(row=4, column=1)

    # Lista desplegable para seleccionar el método
    Label(window, text="Método de resolución:").grid(row=5, column=0)
    methods = ["Euler", "Runge-Kutta"]
    method_var = tk.StringVar()
    method_var.set(methods[0])
    method_dropdown = ttk.Combobox(window, textvariable=method_var, values=methods)
    method_dropdown.grid(row=5, column=1)

    # Área de texto para mostrar soluciones numéricas
    results_text = Text(window, height=10, width=50, state=tk.DISABLED)
    results_text.grid(row=6, column=0, columnspan=2, pady=10)

    # Botón para calcular y graficar resultados
    Button(window, text="Calcular y Graficar", command=plot_results).grid(row=7, column=0, columnspan=2)

    window.mainloop()

# Ejecutar la aplicación
if __name__ == "__main__":
    main_EDO2()
