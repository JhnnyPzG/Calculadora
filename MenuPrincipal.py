import tkinter as tk
from tkinter import ttk
from Ceros import Ceros
from Interpolacion import main as main_interpolacion
from Integracion import GUI
from Edo1 import solve_and_plot_ode
from Edo2 import ODE_solver_GUI_2

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Principal")
        self.root.configure(bg='sky blue')
        self.root.geometry("400x400")
        self.root.configure(borderwidth=5)  # Ajusta el grosor del borde de la ventana principal

        # Crear un contenedor para los botones con fondo azul
        button_container = ttk.Frame(root, padding="20", style='sky Blue.TFrame')
        button_container.pack(pady=20, fill='both', expand=True)

        # Añadir un título
        ttk.Label(button_container, text="Selecciona el Método", font=('Helvetica', 16, 'bold'), background='#05b7f2', foreground='white').pack(pady=10, fill='both')

        # Crear botones para acceder a las aplicaciones
        buttons = [
            ("Ceros", self.abrir_aplicacion_buscador_raiz),
            ("Interpolación", self.abrir_aplicacion_interpolacion),
            ("Integración", self.abrir_aplicacion_integracion),
            ("Ecuaciones diferenciales 1", self.abrir_aplicacion_edo1),
            ("Ecuaciones diferenciales 2", self.abrir_aplicacion_edo2)
        ]

        for text, command in buttons:
            # Agregar cursor "hand2" a los botones
            ttk.Button(button_container, text=text, command=command, cursor="heart").pack(fill='x', pady=5) #agg cursor heart

    def abrir_aplicacion_buscador_raiz(self):
        ventana_buscador_raiz = tk.Toplevel(self.root)
        aplicacion_buscador_raiz = Ceros(ventana_buscador_raiz)

    def abrir_aplicacion_interpolacion(self):
        main_interpolacion()

    def abrir_aplicacion_integracion(self):
        GUI()

    def abrir_aplicacion_edo1(self):
        solve_and_plot_ode()

    def abrir_aplicacion_edo2(self):
        ODE_solver_GUI_2()

if __name__ == "__main__":
    root = tk.Tk()

    # Configurar el estilo para el fondo azul
    style = ttk.Style(root)
    style.configure('yellow.TFrame', background='#4a90e2', foreground='white')  # Ajusta el color según tu preferencia

    app = MenuPrincipal(root)
    root.mainloop()
