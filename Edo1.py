import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

def Euler(f, a, b, h, co):
    n = int((b - a) / h)
    t = np.linspace(a, b, n+1)
    yeu = [co]
    for i in range(n):
        yeu.append(yeu[i] + h * f(t[i], yeu[i]))
    return t, yeu

def Runge4(f, a, b, h, co):
    n = int((b - a) / h)
    t = np.linspace(a, b, n+1)
    yk = [co]
    for i in range(n):
        k1 = h * f(t[i], yk[i])
        k2 = h * f(t[i] + h/2, yk[i] + 1/2*k1)
        k3 = h * f(t[i] + h/2, yk[i] + 1/2*k2)
        k4 = h * f(t[i+1], yk[i] + k3)
        yk.append(yk[i] + 1/6 * (k1 + 2*k2 + 2*k3 + k4))
    return t, yk

def plot_graph(f, Y, a, b, h, co, Y_exact):
    method = method_var.get()

    if method == "Euler":
        t, yeu = Euler(f, a, b, h, co)
    elif method == "Runge-Kutta":
        t, yeu = Runge4(f, a, b, h, co)

    ax.clear()  # Limpiar el eje antes de graficar

    # Gráfica de la solución aproximada
    ax.plot(t, yeu, 'md', label=f'{method} Aproximada (f)')

    # Gráfica de la solución exacta
    ax.plot(t, Y(t), 'b', label=f'{method} Exacta (Y)')

    ax.set_xlabel('t')
    ax.set_ylabel('Y(t)')
    ax.legend()
    ax.grid(True)  # Agrega la cuadrícula
    ax.set_title('Gráfica de la Solución')
    canvas.draw()

    # Actualiza el Label con los valores devueltos
    result_label.config(text=f'Tiempo: {t}\nSolución Aproximada: {t, yeu}\nSolución Exacta: {t, Y(t)}')

# Función para borrar todos los datos ingresados
def clear_data():
    f_entry.delete(0, tk.END)
    Y_entry.delete(0, tk.END)
    a_entry.delete(0, tk.END)
    b_entry.delete(0, tk.END)
    h_entry.delete(0, tk.END)
    co_entry.delete(0, tk.END)
    result_label.config(text="")
    ax.clear()  # Limpiar el eje antes de graficar
    canvas.draw()

# Función para cambiar de método y actualizar la interfaz
def update_method(*args):
    ax.clear()  # Limpiar el eje antes de graficar
    canvas.draw()

# Crear la ventana principal
root = tk.Tk()
root.title("INTERFAZ PARA EDO 1")

# Variables de control
method_var = tk.StringVar()
method_var.set("Euler")  # Valor por defecto
method_var.trace_add('write', update_method)  # Asociar la función al cambio de método

# Crear los elementos de la interfaz
method_label = ttk.Label(root, text="Método:")
method_combobox = ttk.Combobox(root, textvariable=method_var, values=["Euler", "Runge-Kutta"])
f_label = ttk.Label(root, text="Función f(t, y):")
f_entry = ttk.Entry(root)
Y_label = ttk.Label(root, text="Función Y(t):")
Y_entry = ttk.Entry(root)
a_label = ttk.Label(root, text="a:")
a_entry = ttk.Entry(root)
b_label = ttk.Label(root, text="b:")
b_entry = ttk.Entry(root)
h_label = ttk.Label(root, text="h:")
h_entry = ttk.Entry(root)
co_label = ttk.Label(root, text="Condición Inicial:")
co_entry = ttk.Entry(root)
calculate_button = ttk.Button(root, text="Calcular", command=lambda: plot_graph(
    lambda t, y: eval(f_entry.get()),  # Convertir la entrada de la función a una función real
    lambda t: eval(Y_entry.get()),  # Convertir la entrada de la segunda función a una función real
    float(a_entry.get()), float(b_entry.get()), float(h_entry.get()), float(co_entry.get()), lambda t: 0  # Ajusta la función exacta según tus necesidades
))

# Crear el botón para borrar datos
clear_button = ttk.Button(root, text="Borrar Datos", command=clear_data)

# Label para mostrar los valores devueltos
result_label = ttk.Label(root, text="")
result_label.grid(row=8, column=0, columnspan=3, pady=10)

# Posicionar los elementos en la interfaz
method_label.grid(row=0, column=0, padx=5, pady=5, sticky="E")
method_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="W")
f_label.grid(row=1, column=0, padx=5, pady=5, sticky="E")
f_entry.grid(row=1, column=1, padx=5, pady=5, sticky="W")
Y_label.grid(row=2, column=0, padx=5, pady=5, sticky="E")
Y_entry.grid(row=2, column=1, padx=5, pady=5, sticky="W")
a_label.grid(row=3, column=0, padx=5, pady=5, sticky="E")
a_entry.grid(row=3, column=1, padx=5, pady=5, sticky="W")
b_label.grid(row=4, column=0, padx=5, pady=5, sticky="E")
b_entry.grid(row=4, column=1, padx=5, pady=5, sticky="W")
h_label.grid(row=5, column=0, padx=5, pady=5, sticky="E")
h_entry.grid(row=5, column=1, padx=5, pady=5, sticky="W")
co_label.grid(row=6, column=0, padx=5, pady=5, sticky="E")
co_entry.grid(row=6, column=1, padx=5, pady=5, sticky="W")
calculate_button.grid(row=7, columnspan=2, pady=10)
clear_button.grid(row=8, column=2, pady=10)

# Configurar la interfaz de matplotlib
fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=2, rowspan=8, padx=10, pady=10)

# Configurar el cierre de la aplicación
root.protocol("WM_DELETE_WINDOW", root.destroy)

# Iniciar el bucle principal
root.mainloop()
