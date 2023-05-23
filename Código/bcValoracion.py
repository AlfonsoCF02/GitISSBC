# -*- coding: utf-8 -*-
"""
Created on Mon May 22 19:22:19 2023

@author: Alfonso Cabezas Fernández
"""


import sys
from PyQt5.QtWidgets import QApplication
import types


class Clase():
    """
    Clase en la jerarquia mas alta.
    """
    def __init__(self, nombre):
        """
        @param: Nombre de la clase.
        @param: Reglas de la clase.
        @param: Descripcion de la clase.
        """

        self.nombre = nombre  # La clase tiene un nombre
        self.reglas = []
        self.descripcion = u''


# CLASE GENERICA PARA REPRESENTACION DE REGLAS Y DEFINICION DE TIPOS DE REGLAS

class Regla():
    """
    Describe aspectos generales de una regla
    """
    def __init__(self, idRegla):
        self.idRegla = idRegla
        pass


# CLASE GENERICA PARA REPRESENTACION DE ATRIBUTOS

class Atributo():
    """
    Clase Atributo. Permite especificar las propiedades
    de los atributos que van a usarse en la base de conocimiento para
    describir un objeto.
    """
    def __init__(self, nombre, tipo, unidad, valor=None, posiblesValores=None):
        self.nombre = nombre
        self.tipo = tipo
        self.unidad = unidad

        # Obtenemos los posibles valores del atributo en caso de que sea de tipo multiple
        if (tipo == 'multiple') and (posiblesValores is not None) and (type(posiblesValores) is list):
            self.posiblesValores = posiblesValores

        # Comprobamos si el tipo de atributo es boleano para añadir los posibles valores de dicho tipo
        if tipo == 'boleano':
            self.posiblesValores = [True, False]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.exit(app.exec_())
