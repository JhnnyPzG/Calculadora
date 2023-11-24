import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AplicacionBuscadorRaiz:
    def __init__(self, root):
        self.root = root
        self.root.title("INTERFAZ PARA CEROS")

        # Marco principal
        main_frame = ttk.Frame(root, padding=10)
        main_frame.grid(row=0, column=0)

        # Sección de entrada
        entry_section = ttk.LabelFrame(main_frame, text="Entrada", padding=(10, 5))
        entry_section.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(entry_section, text="Función (use 'x' como variable):").grid(row=0, column=0, pady=5, padx=15, sticky="w")
        self.entrada_funcion = ttk.Entry(entry_section, width=30)
        self.entrada_funcion.grid(row=1, column=0, pady=5, padx=15, sticky="ew")

        ttk.Label(entry_section, text="Intervalo [a, b]:").grid(row=0, column=1, pady=5, padx=15, sticky="w")
        self.entrada_valor_inicial = ttk.Entry(entry_section, width=30)
        self.entrada_valor_inicial.grid(row=1, column=1, pady=5, padx=15, sticky="ew")

        ttk.Label(entry_section, text="Tolerancia:").grid(row=0, column=2, pady=5, padx=15, sticky="w")
        self.entrada_tolerancia = ttk.Entry(entry_section, width=30)
        self.entrada_tolerancia.grid(row=1, column=2, pady=5, padx=15, sticky="ew")

        ttk.Label(entry_section, text="Método:").grid(row=0, column=3, pady=5, padx=15, sticky="w")
        self.var_metodo = tk.StringVar()
        metodos = ["Bisección", "Posición Falsa", "Newton", "Secante"]
        self.combobox_metodo = ttk.Combobox(entry_section, values=metodos, textvariable=self.var_metodo, width=27)
        self.combobox_metodo.grid(row=1, column=3, pady=5, padx=15, sticky="ew")
        self.combobox_metodo.set(metodos[0])

        # Botón para encontrar la raíz y graficar el método
        ttk.Button(main_frame, text="Encontrar Raíz", command=self.encontrar_raiz).grid(row=1, column=0, pady=10, sticky="ew")

        # Sección de resultados y gráficos
        results_section = ttk.LabelFrame(main_frame, text="Resultados y Gráficos", padding=(10, 5))
        results_section.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(results_section, text="Resultados:").grid(row=0, column=0, pady=5, sticky="w")
        self.tabla_raiz = ttk.Treeview(results_section, columns=("Valor",), show="headings", height=1)
        self.tabla_raiz.heading("Valor", text="Raíz")
        self.tabla_raiz.grid(row=1, column=0, pady=5, sticky="nsew")

        ttk.Label(results_section, text="Iteraciones:").grid(row=2, column=0, pady=5, sticky="w")
        self.tabla_iteraciones = ttk.Treeview(results_section, columns=("Iteración", "Valor"), show="headings", height=5)
        self.tabla_iteraciones.heading("Iteración", text="Iteración")
        self.tabla_iteraciones.heading("Valor", text="Valor")
        self.tabla_iteraciones.grid(row=3, column=0, pady=5, sticky="nsew")

        # Gráfico de la función
        self.figura, self.ax_funcion = plt.subplots(figsize=(5, 3), tight_layout=True)
        self.ax_funcion.set_title("Gráfico de la Función")
        self.ax_funcion.set_xlabel("x")
        self.ax_funcion.set_ylabel("f(x)")
        self.canvas_funcion = FigureCanvasTkAgg(self.figura, master=results_section)
        self.canvas_funcion.get_tk_widget().grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="nsew")

        # Configuración del grid para que se expanda con la ventana
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        results_section.columnconfigure(1, weight=1)
        results_section.rowconfigure((1, 3), weight=1)

    def encontrar_raiz(self):
        funcion_str = self.entrada_funcion.get()
        valor_inicial = self.entrada_valor_inicial.get()
        tolerancia = float(self.entrada_tolerancia.get())
        metodo_seleccionado = self.var_metodo.get()

        x = sp.symbols('x')
        try:
            funcion = sp.sympify(funcion_str)
        except sp.SympifyError:
            messagebox.showerror("Error", "Expresión de función no válida.")
            return

        intervalo = self.obtener_intervalo(valor_inicial)
        if intervalo is None:
            return

        if metodo_seleccionado == "Bisección":
            raiz, iteraciones = biseccion(lambda x_val: funcion.subs(x, x_val), *intervalo, tolerancia)
        elif metodo_seleccionado == "Posición Falsa":
            raiz, iteraciones = posicion_falsa(lambda x_val: funcion.subs(x, x_val), *intervalo, tolerancia)
        elif metodo_seleccionado == "Newton":
            try:
                valor_inicial = float(valor_inicial[0])
                raiz, iteraciones = newton(funcion, valor_inicial, tolerancia)
            except ValueError:
                messagebox.showerror("Error", "Valor inicial no válido.")
                return
        elif metodo_seleccionado == "Secante":
            raiz, iteraciones = secante(lambda x_val: funcion.subs(x, x_val), *intervalo, tolerancia)

        self.mostrar_resultados(raiz, iteraciones)
        self.graficar_funcion_y_metodo(funcion, intervalo, raiz, x, metodo_seleccionado)

    def mostrar_resultados(self, raiz, iteraciones):
        self.limpiar_tabla(self.tabla_raiz)
        self.limpiar_tabla(self.tabla_iteraciones)

        self.tabla_raiz.insert("", "end", values=(raiz,))

        for i, iteracion in enumerate(iteraciones, 1):
            self.tabla_iteraciones.insert("", "end", values=(i, iteracion[1]))

        num_iteraciones = len(iteraciones)
        mensaje = f"Raíz encontrada en {num_iteraciones} iteraciones."
        messagebox.showinfo("Resultado", mensaje)

    def graficar_funcion_y_metodo(self, funcion, intervalo, raiz, x, metodo):
        valores_intervalo = list(map(float, intervalo))
        if len(valores_intervalo) != 2:
            messagebox.showerror("Error", "Intervalo no válido para graficar.")
            return

        try:
            valores_x = np.linspace(float(valores_intervalo[0]), float(valores_intervalo[1]), 100)
        except ValueError:
            messagebox.showerror("Error", "Intervalo no válido para graficar.")
            return

        valores_y = [funcion.subs(x, val) for val in valores_x]

        self.ax_funcion.clear()
        self.ax_funcion.plot(valores_x, valores_y, label=str(funcion))

        if isinstance(raiz, (int, float)):
            self.ax_funcion.scatter([raiz], [funcion.subs(x, raiz)], color='red', label='Raíz')
        else:
            self.ax_funcion.set_title("Gráfico de la Función (Raíz no válida)")
            self.ax_funcion.legend()
            self.canvas_funcion.draw()
            return

        self.ax_funcion.set_title(f"Gráfico de la Función y Método: {metodo}")
        self.ax_funcion.set_xlabel("x")
        self.ax_funcion.set_ylabel("f(x)")
        self.ax_funcion.legend()

        self.canvas_funcion.draw()

    def obtener_intervalo(self, valor_inicial):
        try:
            return list(map(float, valor_inicial.split(',')))
        except ValueError:
            messagebox.showerror("Error", "Intervalo no válido.")
            return None

    def limpiar_tabla(self, tabla):
        for item in tabla.get_children():
            tabla.delete(item)

def biseccion(f, a, b, tol):
    if f(a) * f(b) > 0:
        messagebox.showerror("Error", "La función no cumple el teorema en el intervalo, busque otro intervalo")
        return None, None
    acum = 0
    datos = []
    while np.abs(b - a) > tol:
        c = (a + b) / 2
        datos.append([a, b, c, f(a), f(c), np.abs(b - a)])
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
        acum += 1
    return c, datos

def posicion_falsa(f, a, b, tol):
    if (f(a) * f(b) > 0):
        print('La funcion no cumple el teorema en el intervalo, busque otro itervalo')
    else:
        D = []
        c = a - ((f(a) * (a - b)) / (f(a) - f(b)))
        D.append([a, b, c, f(a), f(c), "+" if f(a) * f(c) > 0 else "-", np.abs(f(c))])
        while(np.abs(f(c)) > tol):
            c = a - ((f(a) * (a - b)) / (f(a) - f(b)))
            if (f(a) * f(c) < 0):
                b = c
            else:
                a = c
            D.append([a, b, c, f(a), f(c), "+" if f(a) * f(c) > 0 else "-", np.abs(f(c))])
        #print('La raiz de la función por falsa Posición es:', c, 'y su valor es:', f(c))
    return c, D


def newton(f, x0, tol):
    x = sp.symbols('x')
    df = sp.diff(f, x)
    tabla = []
    x_vals = [x0]
    i = 1

    while True:
        x1 = x_vals[-1] - f.subs(x, x_vals[-1]) / df.subs(x, x_vals[-1])
        x_vals.append(x1)
        tabla.append([i, x1])
        if sp.Abs(x1 - x_vals[-2]) <= tol:
            break
        i += 1

    return x_vals, tabla

def secante(f, x0, x1, tol):
    i = 1
    tabla = []
    x_vals = [x0, x1]

    while True:
        x2 = x_vals[-1] - f(x_vals[-1]) * (x_vals[-1] - x_vals[-2]) / (f(x_vals[-1]) - f(x_vals[-2]))
        x_vals.append(x2)
        tabla.append([i, x2])
        if np.abs(x2 - x_vals[-2]) <= tol:
            break
        i += 1

    return x_vals, tabla

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionBuscadorRaiz(root)
    root.mainloop()
