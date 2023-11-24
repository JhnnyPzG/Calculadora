import tkinter as tk
from tkinter import ttk
from Ceros import AplicacionBuscadorRaiz
from Interpolacion import AplicacionInterpolacion
from Integracion import AplicacionIntegracion
from Edo1 import AplicacionEDO1
from Edo2 import AplicacionEDO2

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("MENÚ PRINCIPAL")
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
        aplicacion_buscador_raiz = AplicacionBuscadorRaiz(ventana_buscador_raiz)

    def abrir_aplicacion_interpolacion(self):
        app_interpolacion = AplicacionInterpolacion()
        app_interpolacion.run()

    def abrir_aplicacion_integracion(self):
        aplicacion_integracion = AplicacionIntegracion()
        aplicacion_integracion.run()

    def abrir_aplicacion_edo1(self):
        ventana_edo1 = tk.Toplevel(self.root)
        aplicacion_edo1 = AplicacionEDO1(ventana_edo1)

    def abrir_aplicacion_edo2(self):
        ventana_edo2 = tk.Toplevel(self.root)
        aplicacion_edo2 = AplicacionEDO2(ventana_edo2)

if __name__ == "__main__":
    root = tk.Tk()

    # Configurar el estilo para el fondo azul
    style = ttk.Style(root)
    style.configure('yellow.TFrame', background='#4a90e2', foreground='white')

    app = MenuPrincipal(root)
    root.mainloop()   