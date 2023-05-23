"""
Created on Mon May 22 19:22:19 2023

Base de conocimiento de valoracion de Becas

@author: Alfonso de la Torre
"""

#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import sys
from PyQt5 import QtWidgets
import bcValoracionBeca as bccb


class DecidirCaso():

    def __init__(self, persona, solicitud):
        self.persona = persona
        self.solicitud = solicitud
        self.criterio = None
        self.decision = None
        self.valor = None
        self.personaAbstraida = None
        self.solicitudAbstraida = None
        self.valorLimite = None

    def execute(self):
        abstraer = Abstraer(self.persona, self.solicitud)
        self.personaAbstraida, self.solicitudAbstraida = abstraer.execute()
        seleccionar = Seleccionar(self.solicitudAbstraida)
        self.criterio, self.valorLimite = seleccionar.execute()
        evaluar = Evaluar(self.criterio, self.personaAbstraida, self.solicitudAbstraida)
        self.valor, self.solicitudAbstraida = evaluar.execute()
        equiparar = Equiparar(self.valorLimite, self.valor, self.solicitudAbstraida)
        self.decision, self.solicitudAbstraida = equiparar.execute()
        return self.decision, self.solicitudAbstraida.descripcion


class Inferencia():
    """
    Clase padre de todas las inferencias del modelo de aplicación
    """
    def __init__(self):
        pass

    def execute(self):
        pass


class Abstraer(Inferencia):
    """
    Clase representativa de la abstracción encargada de abstraer nuevos datos a partir de los inicialmente introducidos
    """
    def __init__(self, persona, solicitud):
        Inferencia.__init__(self)
        self.p = persona
        self.s = solicitud

    def execute(self):
        for r in self.p.reglas:
            self.p = r.execute(self.p, self.s)

        for r1 in self.s.reglas:
            self.s = r1.execute(self.p, self.s)

        return self.p, self.s


class Seleccionar(Inferencia):
    """
    Inferencia encargada de seleccionar el criterio y determinar valor límite para la solicitud
    """
    def __init__(self, solicitud):
        Inferencia.__init__(self)
        self.s = solicitud

    def execute(self):
        c = self.s.criterio

        for i in self.s.atributos:
            if i.nombre == 'ValorLimite':
                v = i.valor

        return c, v


class Evaluar(Inferencia):
    """
    Inferencia encargada de seleccionar obtener el valor asignado a la persona en función del criterio anteriormente seleccionado
    """
    def __init__(self, criterio, persona, solicitud):
        Inferencia.__init__(self)
        self.c = criterio
        self.p = persona
        self.s = solicitud

    def execute(self):
        d, so = self.c.execute(self.p, self.s)
        return d, so


class Equiparar(Inferencia):
    """
    Inferencia encargada de equiparar el valor límite con el valor obtenido por la persona en la inferencia evaluar
    """
    def __init__(self, valorLimite, valor, solicitud):
        Inferencia.__init__(self)
        self.vl = valorLimite
        self.v = valor
        self.s = solicitud

    def execute(self):
        if self.vl <= self.v:
            self.s.descripcion += 'El valor ' + str(self.v) + ' es mayor que ' + str(self.vl) + ' por tanto se acepta\n'
            return True, self.s
        else:
            self.s.descripcion += 'El valor ' + str(self.v) + ' es menor que ' + str(self.vl) + ' por tanto se deniega\n'
            return False, self.s


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    persona = bccb.Persona()
    solicitud = bccb.Solicitud()
    resultado = DecidirCaso(persona, solicitud)
    sys.exit(app.exec_())
