# Importación de librerias
from fileinput import close
import sqlite3
import re
from tkinter.messagebox import askyesno
import csv
import os
import sys
import datetime
import traceback
#PASO 2 - importacion de Observador 
from observador351 import Sujeto


#/////////////////////
# DECORADORES
# ///////////////////

BASE_DIRacc = os.path.dirname(os.path.abspath(__file__))
ruta = os.path.join(BASE_DIRacc, "acciones.txt")

#############################################
# Un audit log es un registro de las acciones que ocurren sobre una aplicación con unos datos 
# y registra cuando ocurre una operación, qué operación ha realizado y 
# se puede incluir la información modificada (en su estado inicial y el modificado).
#############################################

def decorador_alta(_alta):
    def envoltura_alta(self, a, b, c, d, e, tree):
        print("Alta de Registro", _alta(self, a, b, c, d, e, tree))
        info = f' {str(ruta)}\n <<ALTA>> Fecha: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n \n'
        with open(ruta, "a") as log:
            log.write(info)
    return envoltura_alta

def decorador_baja(_baja):
    def envoltura_baja(self, tree):
        print("Baja de Registro", _baja(self, tree))
        info = f' {str(ruta)}\n <<BAJA>> Fecha: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n \n'
        with open(ruta, "a") as log:
            log.write(info)
    
    return envoltura_baja

def decorador_modificar(_modificar):
    def envoltura_modificar(self, a, b, c, d, e, tree):
        print("Modificación de Registro", _modificar(self, a, b, c, d, e, tree))
        info = f' {str(ruta)}\n <<MODIFICAR>> Fecha: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n \n'
        with open(ruta, "a") as log:
            log.write(info)
    
    return envoltura_modificar
            
# ///////////////////
# MODELO
# ///////////////////


# Creación de base de datos
class Rutinas(Sujeto):
    def __init__(self):
        self.conexion()
        self.cursor = self.con.cursor()
        self.crear_tabla()
        
    
    def conexion(self): 
        self.con = sqlite3.connect("proveedor.db")
        return self.con

    def crear_tabla(self):
        try:
            con = self.conexion()
            self.cursor = con.cursor()
            sql = """CREATE TABLE IF NOT EXISTS cliente(id INTEGER PRIMARY KEY AUTOINCREMENT,\
                provedor VARCHAR(80) NOT NULL, molde VARCHAR(80), codigo VARCHAR(80),\
                reclamo VARCHAR(80), foto VARCHAR(80))"""
            self.cursor.execute(sql)
            self.con.commit()
        except sqlite3.OperationalError as error: 
            raise ValueError("error al crear tabla")
    
############################################
# Funcion alta con aplicacion de excepciones
#############################################

# PASO 3 - heredo

    @decorador_alta
    def alta(self, a, b, c, d, e, tree):
        try:    
            cadena = a
            patron = "^[A-Za-záéíóú]*$" #regex
            if re.match(patron, cadena):
                print(a, b, c, d, e)
                data = (a, b, c, d, e)
                x = all(data)
                print(x) 
                if x == False:
                    raise ValueError("Faltan datos de cargar")
                
                sql = "INSERT INTO cliente(provedor, molde, codigo, reclamo, foto) VALUES(?, ?, ?, ?, ?)"
                self.cursor.execute(sql, data)
                self.con.commit()
                self.actualizar_treeview(tree)
                print("Ingreso Ok")
                self.notificar(self, a, b, c, d)
                return "Ingreso Ok"
                
            else:
                raise ValueError(a)
            
        except ValueError as a:
            return("ATENCION! escribio", str(a))    
        


    # Funcion borrar
    @decorador_baja
    def borrar(self, tree):
        valor = tree.selection()
        item = tree.item(valor)
        mi_id = item["text"]
        data = (mi_id,)
        sql = "DELETE FROM cliente WHERE id = ?;"
        self.cursor.execute(sql, data)
        self.con.commit()
        tree.delete(valor)
        return "Info Borrada"

    def actualizar_treeview(self, tree):
        records = tree.get_children()
        for element in records:
            tree.delete(element)
        sql = "SELECT * FROM cliente ORDER BY id ASC"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        for fila in resultado:
            print(fila)
            tree.insert(
                "", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5])
            )
        pass
############################################
# Funcion modificacion con aplicacion de excepciones
#############################################
    @decorador_modificar
    def modificar(self, a, b, c, d, e, tree):
        try:
            valor1 = tree.selection()
            print(valor1)
            registros = tree.item(valor1)
            mi_id = registros["text"]
            print(mi_id)
            print(a, b, c, d, e)
            data = (a, b, c, d, e, mi_id)
            x = all(data)
            if x == False:
                raise ValueError("Faltan datos de cargar")
            
            sql = "UPDATE cliente SET provedor=?, molde=?, codigo=?,reclamo=?,foto=? WHERE id=?"
            self.cursor.execute(sql, data)
            self.con.commit()
            self.actualizar_treeview(tree)
            return "Cambio OK"
        
        except ValueError as a:
            return("Ojo ", str(a))
        
    def modelo_exportar_csv(self):
        con = self.conexion()
        cursor = con.cursor()
        sql = "SELECT * FROM cliente;"
        cursor.execute(sql)
        con.commit()
        with open("base_reclamos.csv", "w", encoding="UTF-8", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])
            csv_writer.writerows(cursor)
        return "Registros exportados"
    
    # función borrado de datos
    def modelo_eliminar(self):
            self.con=self.conexion()
            cursor = self.con.cursor()
            sql = "DELETE FROM cliente;"
            cursor.execute(sql)
            self.con.commit()
            return
                