import tkinter as tk
from tkinter import ttk
from Ceros import Ceros
from Interpolacion import main as main_interpolacion

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
            ("Ecuaciones diferenciales 1", self.abrir_aplicacion_interpolacion),
            ("Ecuaciones diferenciales 2", self.abrir_aplicacion_interpolacion)
        ]

        for text, command in buttons:
            ttk.Button(button_container, text=text, command=command).pack(fill='x', pady=5)

    def abrir_aplicacion_buscador_raiz(self):
        ventana_buscador_raiz = tk.Toplevel(self.root)
        ventana_buscador_raiz.title("Ventana Ceros")  # Puedes personalizar el título
        ventana_buscador_raiz.geometry("300x300")  # Puedes ajustar el tamaño según tus necesidades
        ventana_buscador_raiz.configure(borderwidth=5)  # Ajusta el grosor del borde según tus preferencias

        aplicacion_buscador_raiz = Ceros(ventana_buscador_raiz)

    def abrir_aplicacion_interpolacion(self):
        main_interpolacion()

    def abrir_aplicacion_integracion(self):
        ventana_integracion = tk.Toplevel(self.root)
        ventana_integracion.title("Ventana de Integración")  
        ventana_integracion.geometry("800x400")  

        aplicacion_buscador_integracion = (ventana_integracion)
    

if __name__ == "__main__":
    root = tk.Tk()

    # Configurar el estilo para el fondo azul
    style = ttk.Style(root)
    style.configure('yellow.TFrame', background='#4a90e2', foreground='white')  # Ajusta el color según tu preferencia

    app = MenuPrincipal(root)
    root.mainloop()
