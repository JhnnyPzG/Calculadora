import tkinter as tk
from tkinter import ttk
from Ceros import Ceros
from Interpolacion import main as main_interpolacion

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Principal")

        self.root.geometry("900x900")

        # Crear botones para acceder a las aplicaciones
        ttk.Button(root, text="Ceros", command=self.abrir_aplicacion_buscador_raiz).pack(pady=20)
        ttk.Button(root, text="Interpolación", command=self.abrir_aplicacion_interpolacion).pack(pady=20)

    def abrir_aplicacion_buscador_raiz(self):
        ventana_buscador_raiz = tk.Toplevel(self.root)
        aplicacion_buscador_raiz = Ceros(ventana_buscador_raiz)

    def abrir_aplicacion_interpolacion(self):
        main_interpolacion()

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuPrincipal(root)
    root.mainloop()
