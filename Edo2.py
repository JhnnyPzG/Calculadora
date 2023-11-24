import tkinter as tk
from tkinter import Label, Entry, Button, ttk, Text
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk  # Importar de PIL

class AplicacionEDO2:
    def __init__(self, master):
        self.master = master
        master.title("INTERFAZ PARA ECUACIONES DIFERENCIALES 2")

        # Etiquetas y campos de entrada
        Label(master, text="Valor inicial (a):", font='Arial 10').grid(row=0, column=0, pady=5, padx=10)
        self.a_entry = Entry(master, font='Arial 10')
        self.a_entry.grid(row=0, column=1, pady=5, padx=10)

        Label(master, text="Valor final (b):", font='Arial 10').grid(row=1, column=0, pady=5, padx=10)
        self.b_entry = Entry(master, font='Arial 10')
        self.b_entry.grid(row=1, column=1, pady=5, padx=10)

        Label(master, text="Tamaño del paso (h):", font='Arial 10').grid(row=2, column=0, pady=5, padx=10)
        self.h_entry = Entry(master, font='Arial 10')
        self.h_entry.grid(row=2, column=1, pady=5, padx=10)

        Label(master, text="Condición inicial (co o var):", font='Arial 10').grid(row=3, column=0, pady=5, padx=10)
        self.co_entry = Entry(master, font='Arial 10')
        self.co_entry.grid(row=3, column=1, pady=5, padx=10)

        # Lista desplegable para seleccionar el método
        Label(master, text="Método de resolución:", font='Arial 10').grid(row=5, column=0, pady=5, padx=10)
        methods = ["Euler", "Runge-Kutta"]
        self.method_var = tk.StringVar()
        self.method_var.set(methods[0])
        self.method_dropdown = ttk.Combobox(master, textvariable=self.method_var, values=methods, font='Arial 10')
        self.method_dropdown.grid(row=5, column=1, pady=5, padx=10)

        # Área de texto para mostrar soluciones numéricas
        self.results_text = Text(master, height=10, width=50, state=tk.DISABLED, font='Arial 10')
        self.results_text.grid(row=6, column=0, columnspan=2, pady=10, padx=10)

        # Botón para calcular y graficar resultados
        calculate_button = Button(master, text="Calcular y Graficar", command=self.plot_resultados)
        calculate_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10)

        # Espacio para la gráfica
        self.graph_label = Label(master)
        self.graph_label.grid(row=8, column=0, columnspan=2, pady=10, padx=10)

        # Crear una figura vacía al iniciar la aplicación
        fig, ax = plt.subplots()
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=2, rowspan=10)

        # Almacenar el widget de la gráfica actual para poder destruirlo la próxima vez
        self.canvas_widget = canvas_widget

        # Aplicar estilo al botón
        ttk.Style().configure("TButton", padding=(10, 5), font='Arial 10')

    def euler_sis(self, f, a, b, h, co):
        n = int((b - a) / h)
        t = np.linspace(a, b, n+1)
        S = [co]
        for i in range(n):
            S.append(S[i] + h * f(t[i], S[i]))      
        return t, np.array(S)

    def rk4_vec(self, f, a, b, h, var):
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

    def f(self, t, y):
        n = len(y)
        x = np.zeros(n)
        x[0] = y[1]
        x[1] = 2 * (1-y[0]**2)*y[1]-y[0]
        return x

    def plot_resultados(self):
        # Obtener valores de la interfaz gráfica
        a_valor = float(eval(self.a_entry.get()))
        b_valor = float(eval(self.b_entry.get()))
        h_valor = float(eval(self.h_entry.get()))
        co_valor = eval(self.co_entry.get())
        method = self.method_var.get()

        # Calcular soluciones utilizando el método seleccionado
        if method == "Euler":
            t, S = self.euler_sis(self.f, a_valor, b_valor, h_valor, co_valor)
        elif method == "Runge-Kutta":
            t, S = self.rk4_vec(self.f, a_valor, b_valor, h_valor, co_valor)
        else:
            raise ValueError("Método no reconocido")

        # Crear una nueva figura con subgráficas
        fig, axs = plt.subplots(1, 2, figsize=(12, 4), dpi=100, constrained_layout=True)

        # Subgráfica 1: x(t) vs t
        axs[0].grid()
        axs[0].plot(t, S[:, 0], 'g')
        axs[0].set_ylabel('x(t)')
        axs[0].set_xlabel('t')
        axs[0].set_title('x(t) vs t')

        # Subgráfica 2: x'(t) vs t
        axs[1].grid()
        axs[1].plot(t, S[:, 1], 'r')
        axs[1].set_ylabel("x'(t)")
        axs[1].set_xlabel("t")
        axs[1].set_title("x'(t) vs t")

        # Mostrar la nueva gráfica en la interfaz
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=2, rowspan=10)

        # Destruir el widget de la gráfica anterior si existe
        if hasattr(self, 'canvas_widget'):
            self.canvas_widget.destroy()

        # Almacenar el widget de la gráfica actual para poder destruirlo la próxima vez
        self.canvas_widget = canvas_widget

        # Mostrar soluciones numéricas en el área de texto
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Tiempo: {t}\n\nSoluciones:\n{S}")
        self.results_text.config(state=tk.DISABLED)

        # Actualizar la gráfica en el espacio designado
        self.update_graph(fig)

    def update_graph(self, fig):
        # Convertir la figura de Matplotlib a una imagen de PhotoImage
        photo = self.fig_to_photo(fig)

        # Mostrar la imagen en el espacio designado
        self.graph_label.config(image=photo)
        self.graph_label.image = photo

    def fig_to_photo(self, fig):
        # Convertir la figura de Matplotlib a una imagen de PhotoImage
        buf = fig.canvas.tostring_rgb()
        img = Image.frombytes('RGB', fig.canvas.get_width_height(), buf)
        photo = ImageTk.PhotoImage(image=img)

        return photo

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionEDO2(root)
    root.mainloop()
