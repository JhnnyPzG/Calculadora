import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

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

def plot_graph(f, Y, a, b, h, co, Y_exact):
    method = method_var.get()

    if method == "Euler":
        t, yeu = euler_sis(f, a, b, h, co)
    elif method == "Runge-Kutta":
        t, yeu = rk4_vec(f, a, b, h, co)

    ax.clear()
    ax.plot(t, yeu[:, 0], 'md', label=f'{method} Aproximada (f)')
    ax.plot(t, Y(t), 'b', label=f'{method} Exacta (Y)')

    ax.set_xlabel('t')
    ax.set_ylabel('Y(t)')
    ax.legend()
    ax.grid(True)
    ax.set_title('Gráfica de la Solución')
    canvas.draw()

    result_label.config(text=f'Tiempo: {t}\nSolución Aproximada: {t, yeu}\nSolución Exacta: {t, Y(t)}')

def clear_data():
    f_entry.delete(0, tk.END)
    Y_entry.delete(0, tk.END)
    a_entry.delete(0, tk.END)
    b_entry.delete(0, tk.END)
    h_entry.delete(0, tk.END)
    co_entry.delete(0, tk.END)
    result_label.config(text="")
    ax.clear()
    canvas.draw()

def update_method(*args):
    ax.clear()
    canvas.draw()

def ODE_solver_GUI_2():
    root = tk.Tk()
    root.title("INTERFAZ PARA EDO 2")

    global method_var
    method_var = tk.StringVar()
    method_var.set("Euler")
    method_var.trace_add('write', update_method)

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
        lambda t, y: eval(f_entry.get()),
        lambda t: eval(Y_entry.get()),
        float(a_entry.get()), float(b_entry.get()), float(h_entry.get()), float(co_entry.get()), lambda t: 0
    ))

    clear_button = ttk.Button(root, text="Borrar Datos", command=clear_data)

    result_label = ttk.Label(root, text="")
    result_label.grid(row=8, column=0, columnspan=3, pady=10)

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

    fig, ax = plt.subplots(figsize=(8, 6))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=2, rowspan=8, padx=10, pady=10)

    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()

