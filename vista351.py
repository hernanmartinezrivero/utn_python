# Importación de librerias
from fileinput import close
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno, showinfo
from tkinter import filedialog
#import tkinter.filedialog as fdialog
from tkinter import Tk, Button

import sqlite3
from PIL import Image, ImageTk
from modelo351 import Rutinas
import os
import datetime
import traceback
import sys


#global foto_origen
foto_origen = ""

class Tablero(Frame):
    def __init__(self, ventana):
        super().__init__(ventana)
        self.objeto_base = Rutinas()
        self.ventana = ventana
        self.presentacion(self.ventana)
        self.ventana.geometry("1500x600")
        
       

    #funcion para cargar imagen
    def cargar_imagen(self):
        #global foto_origen
        self.foto_origen = StringVar()
        self.foto_origen.set(filedialog.askopenfilename())  # abre una ventana para buscar archivos
        ruta_imagen = self.foto_origen.get()  # obtiene la ruta de la imagen seleccionada
        self.imagen = Image.open(ruta_imagen)  # toma el archivo y lo asigna a una imagen  
        tam_original=self.imagen.size #tupla con los datos del tamaño original
        tam_nuevo=(120,120) #tupla con los datos del tamaño nuevo
        factor = min(float(tam_nuevo[0])/tam_original[0], float(tam_nuevo[1])/tam_original[1]) #calculo del factor de tamaño
        ancho = int(tam_original[0] * factor)
        alto = int(tam_original[1] * factor)
        #el Image.Resampling.LANCZOS es necesario porque mantiene las caracteristicas de la imagen al cambiar de tamaño
        imagen_trabajo= self.imagen.resize((ancho, alto), Image.Resampling.LANCZOS) # se redimensiona la imagen 
        #### Lo mas importante, este es el archivo de fotos a guardar en la base de datos#####
        self.imagen_trabajo = ImageTk.PhotoImage(imagen_trabajo) # genera una imagen compatible con tkinter
        ####
        # se genera la etiqueta para mostrar la imagen
        self.etiqueta_con_imagen=Label(self.ventana, image=self.imagen_trabajo).place(x=450,y=30) # .place(x=150,y=150)define donde ubica la imagen
        #nos retorna a ventana para poner ahi la imagen que termina siendo una etiqueta
        #ventana.mainloop() 
        return "Imagen lista para cargar"

# //////////////
# VISTA PROPIAMENTE DICHA
# //////////////
    
    def presentacion(self, ventana):
# Declaración de variables
        self.pro_val = StringVar()
        self.mol_val = StringVar()
        self.cod_val = StringVar()
        self.rec_val = StringVar()
        self.foto_origen = StringVar()

# //////////////////
# MENU SUPERIOR
# //////////////////

        self.menubar = Menu(self.ventana)
        self.menu_archivo = Menu(self.menubar)
        self.menubar.add_cascade(label="Archivo", menu=self.menu_archivo)
        self.ventana.title("Registro de fallas")
        self.menu_archivo.add_command(label="Exportar CSV", command=self.exportar_csv)
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Eliminar todo", command=lambda: self.eliminar(self.tree))
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Salir", command=self.quit)

        self.menu_info = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Ayuda", menu=self.menu_info)
        self.menu_info.add_command(label="Info Version", command=lambda: self.version())
        self.ventana.config(menu=self.menubar)

    # Creacion de etiquetas y entradas de datos
        self.provedor = Label(ventana, text="Proveedor").place(x=10, y=40)
        self.espacio_provedor = Entry(ventana, textvariable=self.pro_val).place(x=120, y=40)
        self.molde = Label(ventana, text="Molde").place(x=10, y=80)
        self.espacio_molde = Entry(ventana, textvariable=self.mol_val).place(x=120, y=80)
        self.codigo = Label(ventana, text="Codigo").place(x=10, y=120)
        self.espacio_codigo = Entry(ventana, textvariable=self.cod_val).place(x=120, y=120)
        self.reclamo = Label(ventana, text="Reclamo Cliente").place(x=10, y=160)
        self.espacio_reclamo = Entry(ventana, textvariable=self.rec_val, width=100).place(x=120, y=160)

###############################
# TREEVIEW
###############################

        self.tree = ttk.Treeview(self.ventana)
        self.tree.place(x=10, y=200)
        self.tree["columns"] = ("col1", "col2", "col3", "col4", "col5")
        self.tree.column("#0", width=90, minwidth=50, anchor=W)
        self.tree.column("col1", width=200, minwidth=80)
        self.tree.column("col2", width=200, minwidth=80)
        self.tree.column("col3", width=200, minwidth=80)
        self.tree.column("col4", width=200, minwidth=80)
        self.tree.column("col5", width=500, minwidth=80)
        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="Proveedor")
        self.tree.heading("col2", text="Molde")
        self.tree.heading("col3", text="Codigo")
        self.tree.heading("col4", text="Reclamo Cliente")
        self.tree.heading("col5", text="Foto")
        self.objeto_base.actualizar_treeview(self.tree) #aca esta el dolor de cabeza
        
# generacion de boton alta
        self.boton_alta = Button(
            self.ventana,
            text="Alta",
            command=lambda: self.vista_alta(
                self.pro_val, self.mol_val, self.cod_val, self.rec_val, self.foto_origen, self.tree),
            bg="blue",  width=12,
            fg="white",
            )

        self.boton_alta.place(x=800, y=30)

# boton borrar
        self.boton_borrar = Button(
            self.ventana,
            text="Baja",
            command=lambda: self.vista_borrar(self.tree), bg="blue", fg="white",  width=12
            )
        self.boton_borrar.place(x=800, y=70)

# boton modificar
        self.boton_modificar = Button(
            self.ventana,
            text="Modificar",  width=12,
            command=lambda: self.vista_modificar(
                self.pro_val, self.mol_val, self.cod_val, self.rec_val, self.foto_origen, self.tree),
            bg="blue",
            fg="white",
            )
        self.boton_modificar.place(x=800, y=110)

#el boton ejecuta la funcion subir imagen
        self.boton_foto = Button(
            self.ventana,
            text="Cargar Foto",
            command=lambda: self.vista_cargar_imagen(),
            width=12, bg="blue", fg="white"
            )
        self.boton_foto.place(x=300,y=40) 


###############################
# Definicion de comunicacion con botones
###############################


# comunicacion con datos de boton alta
    def vista_alta(self, a, b, c, d, e, tree):
        self.retorno = self.objeto_base.alta(a.get(), b.get(), c.get(), d.get(), e.get(), tree)
        #tomo los valores con el get, antes le pasaba directamente el objeto
        showinfo("Info", self.retorno) 

# comunicacion con boton borrar
    def vista_borrar(self, tree):
        self.retorno = self.objeto_base.borrar(tree)
        showinfo("Info",self.retorno)
        
# comunicacion con boton modificar
    def vista_modificar(self, a, b, c, d, e, tree):
        self.retorno = self.objeto_base.modificar(a.get(), b.get(), c.get(), d.get(), e.get(), tree) #tomo los valores con el get, antes le pasaba directamente el objeto
        showinfo("Info",self.retorno)

      
#Boton cargar imagen
    def vista_cargar_imagen(self):  
        self.retorno = self.cargar_imagen()
        showinfo("Precaucion",self.retorno)

    #funcion exportacion archivo registros    
    def exportar_csv(self):       
        self.retorno= self.objeto_base.modelo_exportar_csv()
        #con = self.objeto_base.conexion()
        #cursor = con.cursor()
        #sql = "SELECT * FROM cliente;"
        #cursor.execute(sql)
        #con.commit()
        #with open("base_reclamos.csv", "w", encoding="UTF-8", newline="") as csv_file:
        #    csv_writer = csv.writer(csv_file)
        #    csv_writer.writerow([i[0] for i in cursor.description])
        #    csv_writer.writerows(cursor)
        showinfo("Exportación",self.retorno)
    
    #funcion informacion de version de app
    def version(self): 
        showinfo("Información del Sofware",
                 "Version 3.5.1\n Equipo de trabajo para UTNBA\n Diplomatura Python 2023\n \n Trabajo final Nivel 3\n Amore, Lautaro\n Casali, Bruno\n Colloso, Matias\n Gevoa, Eduardo\n Martinez Rivero, Hernán\n "
                 ) 

 
    # función borrado de datos
    def eliminar(self, tree):
        self.tree = tree
        if askyesno("Borrar base de datos", "¿Deseas borrar todos los registros?"):
            self.retorno= self.objeto_base.modelo_eliminar()
            
            self.objeto_base.actualizar_treeview(tree)
        else:
            showinfo("Cuidado, es función elimina todos los registros")
    
    pass





# Creación de ventana
if __name__=="__main__":
    ventana = Tk()
    tablero = Tablero(ventana)
    ventana.mainloop()