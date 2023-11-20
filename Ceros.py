import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AplicacionBuscadorRaiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Ceros")

        # Entrada de la función
        ttk.Label(root, text="Ingrese la función (use 'x' como variable):").grid(row=0, column=0, padx=10, pady=10)
        self.function_entry = ttk.Entry(root, width=50)
        self.function_entry.grid(row=0, column=1, padx=10, pady=10)

        # Entrada del valor inicial o intervalo [a, b]
        ttk.Label(root, text="Ingrese el valor inicial o intervalo [a, b]:").grid(row=1, column=0, padx=10, pady=10)
        self.initial_value_entry = ttk.Entry(root)
        self.initial_value_entry.grid(row=1, column=1, padx=10, pady=10)

        # Entrada de la tolerancia
        ttk.Label(root, text="Ingrese la tolerancia:").grid(row=2, column=0, padx=10, pady=10)
        self.tolerance_entry = ttk.Entry(root)
        self.tolerance_entry.grid(row=2, column=1, padx=10, pady=10)

        # Selección del método
        ttk.Label(root, text="Seleccione el método para encontrar la raíz:").grid(row=3, column=0, padx=10, pady=10)
        self.method_var = tk.StringVar()
        methods = ["Bisección", "Posición Falsa", "Newton", "Secante"]
        self.method_combobox = ttk.Combobox(root, values=methods, textvariable=self.method_var)
        self.method_combobox.grid(row=3, column=1, padx=10, pady=10)
        self.method_combobox.set(methods[0])

        # Botón para encontrar la raíz
        ttk.Button(root, text="Encontrar Raíz", command=self.encontrar_raiz).grid(row=4, column=0, columnspan=2, pady=20)

        # Resultados y gráficos
        self.result_label = ttk.Label(root, text="Resultados:")
        self.result_label.grid(row=5, column=0, columnspan=2, pady=10)

        self.root_table = ttk.Treeview(root, columns=("Valor",), show="headings")
        self.root_table.heading("Valor", text="Raíz")
        self.root_table.grid(row=6, column=0, columnspan=2, pady=10)

        self.iteration_table = ttk.Treeview(root, columns=("Iteración", "Valor"), show="headings")
        self.iteration_table.heading("Iteración", text="Iteración")
        self.iteration_table.heading("Valor", text="Valor")
        self.iteration_table.grid(row=7, column=0, columnspan=2, pady=10)

        # Gráfico de la función
        self.figure, self.ax_function = plt.subplots(figsize=(6, 4), tight_layout=True)
        self.ax_function.set_title("Gráfico de la Función")
        self.ax_function.set_xlabel("x")
        self.ax_function.set_ylabel("f(x)")
        self.canvas_function = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas_function.get_tk_widget().grid(row=0, column=2, rowspan=8, padx=10, pady=10)

    def encontrar_raiz(self):
        # Obtener datos ingresados por el usuario
        funcion_str = self.function_entry.get()
        input_value = self.initial_value_entry.get()
        tolerancia = float(self.tolerance_entry.get())
        metodo_seleccionado = self.method_var.get()

        # Definir la función simbólicamente
        x = sp.symbols('x')
        try:
            f = sp.sympify(funcion_str)
        except sp.SympifyError:
            messagebox.showerror("Error", "Expresión de función no válida.")
            return

        # Elegir el método y llamar a la función correspondiente
        if metodo_seleccionado == "Bisección":
            try:
                a, b = map(float, input_value.split(','))
                raiz, iteraciones = Biseccion(lambda x_val: f.subs(x, x_val), a, b, tolerancia)
            except ValueError:
                messagebox.showerror("Error", "Intervalo no válido.")
                return
        elif metodo_seleccionado == "Posición Falsa":
            try:
                a, b = map(float, input_value.split(','))
                raiz, iteraciones = falsa_pos(lambda x_val: f.subs(x, x_val), a, b, tolerancia)
            except ValueError:
                messagebox.showerror("Error", "Intervalo no válido.")
                return
        elif metodo_seleccionado == "Newton":
            try:
                valor_inicial = float(input_value)
                raiz, iteraciones = Newton(f, valor_inicial, tolerancia)
            except ValueError:
                messagebox.showerror("Error", "Valor inicial no válido.")
                return
        elif metodo_seleccionado == "Secante":
            try:
                a, b = map(float, input_value.split(','))
                raiz, iteraciones = Secante(lambda x_val: f.subs(x, x_val), a, b, tolerancia)
            except ValueError:
                messagebox.showerror("Error", "Intervalo no válido.")
                return

        # Mostrar los resultados y graficar la convergencia
        self.mostrar_resultados(raiz, iteraciones)
        self.plot_function_and_root(f, input_value, eval(str(raiz)), x)




    def mostrar_resultados(self, raiz, iteraciones):
        # Limpiar resultados anteriores
        for item in self.root_table.get_children():
            self.root_table.delete(item)
        for item in self.iteration_table.get_children():
            self.iteration_table.delete(item)

        # Mostrar el valor de la raíz
        self.root_table.insert("", "end", values=(raiz,))

        # Mostrar los valores de las iteraciones
        for i, iteracion in enumerate(iteraciones, 1):
            self.iteration_table.insert("", "end", values=(i, iteracion[1]))

        # Mostrar mensaje con el número de iteraciones
        num_iteraciones = len(iteraciones)
        mensaje = f"Raíz encontrada en {num_iteraciones} iteraciones."
        messagebox.showinfo("Resultado", mensaje)

    def plot_function_and_root(self, funcion, intervalo, raiz, x):
        # Crear un array de valores x para la gráfica de la función
        x_vals = np.linspace(float(intervalo.split(',')[0]), float(intervalo.split(',')[1]), 100)

        # Evaluar la función simbólica directamente en lugar de usar lambdify
        y_vals = [funcion.subs(x, val) for val in x_vals]

        # Limpiar el gráfico anterior y graficar la función
        self.ax_function.clear()
        self.ax_function.plot(x_vals, y_vals, label=str(funcion))
        
        # Verificar si la raíz es un número antes de evaluarla en la función
        if isinstance(raiz, (int, float)):
            self.ax_function.scatter([raiz], [funcion.subs(x, raiz)], color='red', label='Raíz')
        else:
            messagebox.showerror("Error", "La raíz no es un número válido.")
            return
        
        self.ax_function.set_title("Gráfico de la Función")
        self.ax_function.set_xlabel("x")
        self.ax_function.set_ylabel("f(x)")
        self.ax_function.legend()

        # Actualizar el gráfico en el widget Tkinter
        self.canvas_function.draw()

def Biseccion(f, a, b, tol):
    if (f(a) * f(b) > 0):
        print('La función no cumple el teorema en el intervalo, busque otro intervalo')
        return None, None
    acum = 0
    data = []
    while(np.abs(b - a) > tol):
        c = (a + b) / 2
        data.append([a, b, c, f(a), f(c), np.abs(b - a)])
        if (f(a) * f(c) < 0):
            b = c
        else:
            a = c
        acum += 1
    return c, data

def falsa_pos(f, a, b, tol):
    if (f(a) * f(b) > 0):
        print('La función no cumple el teorema en el intervalo, busque otro intervalo')
        return None, None
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
    print('La raíz de la función por falsa Posición es:', c, 'y su valor es:', f(c))
    return c, D

def Newton(f, x0, tol):
    x = sp.symbols('x')
    df = sp.diff(f, x)
    tabla = []
    NewT = x - f/df
    NewT = sp.lambdify(x, NewT)
    x1 = x0 - f.subs(x, x0)/df.subs(x, x0)
    i = 1
    tabla.append([i, x1])
    while sp.Abs(x1 - x0) > tol:
        x0 = x1
        x1 = x0 - f.subs(x, x0)/df.subs(x, x0)
        i = i + 1
        tabla.append([i, x1])

    print("La raíz es: ", x1, "La cantidad de iteraciones es: ", i)
    return tabla

def Secante(f,x0,x1,tol):
    i=1
    tabla=[]
    x2 = x1 - f(x1) * (x1-x0) / (f(x1) - f(x0))
    tabla.append([i,x2])
    while(np.abs(x2-x1)>tol):
        x0= x1
        x1= x2
        x2= x1 - f(x1) * (x1-x0) / (f(x1) - f(x0))
        i=i+1
        tabla.append([i, x2])
            
    print('Iteraciones:',i, ' X:', x2)
    return tabla


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionBuscadorRaiz(root)
    root.mainloop()
