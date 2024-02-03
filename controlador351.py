from tkinter import Tk
from vista351 import Tablero
import observador351

class Controlador:     #Está es la clase principal
    
    def __init__(self, ventana):
        self.ventana_controlador = ventana
        self.objeto_vista = Tablero(self.ventana_controlador)
        self.el_observador=observador351.ConcreteObserverA(self.objeto_vista.objeto_base)


if __name__=="__main__":
    ventana = Tk()
    mi_app = Controlador(ventana)
    ventana.mainloop()
