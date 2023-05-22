# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 12:03:13 2015
Base de conocimiento de valoracion de Becas
@author: Alberto
"""
import sys
from PyQt5.QtWidgets import QApplication
from bcValoracion import *


class Solicitud(Clase):
    """
    Describe los atributos por los que se caracterizará a una solicitud de beca
    @param: atTipo
    @param: valorLimite
    @param: atributos
    @param: criterio
    """
    def __init__(self, nombre=None):

        Clase.__init__(self, nombre=nombre)

        self.atTipo = Atributo('Tipo', 'multiple', None, None, ['General', 'Movilidad', 'Especial'])
        self.valorLimite = Atributo('ValorLimite', 'float', None)
        self.atributos = [self.atTipo]
        self.criterio = Criterio("criterio")
        r2 = AbstraerLimite('r2')
        self.reglas = [r2]


class Persona(Clase):
    """
    Describe los atributos por los que se caracterizará a una persona solicitante de una Beca.
    @param: Renta
    @param: Asignaturas Cursadas
    @param: Asignaturas Aprobadas
    @param: Creditos Aprobados
    @param: Nota media
    @param: Independiente
    """
    def __init__(self, nombre=None):

        Clase.__init__(self, nombre=nombre)

        self.atRenta = Atributo('Renta', 'float', None)
        self.atAsignaturasCursadas = Atributo('Cursadas', 'int', None)
        self.atAsignaturasAprobadas = Atributo('Aprobadas', 'int', None)
        self.atCreditosAprobados = Atributo('%Creditos', 'float', None)
        self.atNotaMedia = Atributo('Nota', 'float', None)
        self.atIndependiente = Atributo('Independencia', 'boleano', None, )
        # Se establece la lista de atributos que posee esta clase
        self.atributos = [self.atRenta, self.atAsignaturasAprobadas, self.atAsignaturasCursadas, self.atNotaMedia,
                          self.atIndependiente]
        r1 = AbstraerPorcentaje('r1')
        self.reglas = [r1]


class Criterio(Regla):
    """
    Define el criterio que seguira el sistema para aceptar o denegar una beca
    @param: Creditos >= 80 +0.2
    @param: Creditos >=65 and < 80 +0.2
    @param: Nota>=6.5 +0.2
    @param: Renta<=20000 +0.2
    @param: Independencia == true +0.2
    @return: valor total de la solicitud.
    """
    def __init__(self, idRegla):

        Regla.__init__(self, idRegla)

    def execute(self, persona, solicitud):
        valor = 0.0
        for at in persona.atributos:
            if at.nombre == '%Creditos' and at.valor >= 80:
                solicitud.descripcion += 'El atributo' + at.nombre + ' ' + 'con valor ' + str(at.valor) + ' aporta 0.7 puntos de valoracion\n'
                valor = valor + 0.7

            if at.nombre == '%Creditos' and at.valor >= 65 and at.valor < 80:
                solicitud.descripcion += 'El atributo' + at.nombre + ' ' + 'con valor ' + str(at.valor) + ' aporta 0.3 puntos de valoracion\n'
                valor = valor + 0.3

            if at.nombre == 'Nota' and at.valor >= 6.5:
                solicitud.descripcion += 'El atributo' + at.nombre + ' ' + 'con valor ' + str(at.valor) + ' aporta 0.4 puntos de valoracion\n'
                valor = valor + 0.4

            if at.nombre == 'Renta' and at.valor <= 20000:
                solicitud.descripcion += 'El atributo' + at.nombre + ' ' + 'con valor ' + str(at.valor) + ' aporta 0.7 puntos de valoracion\n'
                valor = valor + 0.7

            if at.nombre == 'Independencia' and at.valor == True:
                solicitud.descripcion += 'El atributo' + at.nombre + ' ' + 'con valor ' + str(at.valor) + ' aporta 0.3 puntos de valoracion\n'
                valor = valor + 0.3

        solicitud.descripcion += 'El valor total de la solicitud obtenido es ' + str(valor) + '\n'
        return valor, solicitud


class AbstraerPorcentaje(Regla):
    """
    Regla basica para abstraer porcentaje de aprobados
    """
    def __init__(self, idRegla):
        Regla.__init__(self, idRegla)

    def execute(self, persona, solicitud):

        porcentaje = float(persona.atAsignaturasAprobadas.valor) / float(persona.atAsignaturasCursadas.valor) * 100
        asignado = False
        for i in persona.atributos:
            if i.nombre == '%Creditos':
                i.valor = porcentaje
                asignado = True
        if asignado == False:
            persona.atCreditosAprobados.valor = porcentaje
            persona.atributos.append(persona.atCreditosAprobados)

        return persona


class AbstraerLimite(Regla):
    """
    Regla basica para abstraer el limite minimo para la concesion de la beca
    """
    def __init__(self, idRegla):
        Regla.__init__(self, idRegla)

    def execute(self, persona, solicitud):

        for i in solicitud.atributos:
            if i.nombre == 'Tipo':
                if i.valor == 'General':
                    asignado = False
                    solicitud.descripcion += 'A la beca de tipo general requiere un minimo de 1.0 puntos de valoracion para ser concedida\n'
                    for j in solicitud.atributos:
                        if j.nombre == 'ValorLimite':
                            j.valor = 0.7
                            asignado = True
                    if asignado == False:
                        solicitud.valorLimite.valor = 1.0
                        solicitud.atributos.append(solicitud.valorLimite)
                if i.valor == 'Movilidad':
                    asignado = False
                    solicitud.descripcion += 'A la beca de tipo movilidad requiere un minimo de 0.5 puntos de valoracion para ser concedida\n'
                    for j in solicitud.atributos:
                        if j.nombre == 'ValorLimite':
                            j.valor = 0.5
                            asignado = True
                    if asignado == False:
                        solicitud.valorLimite.valor = 0.5
                        solicitud.atributos.append(solicitud.valorLimite)
                if i.valor == 'Especial':
                    asignado = False
                    solicitud.descripcion += 'A la beca de tipo especial requiere un minimo de 0.9 puntos de valoracion para ser concedida \n'
                    for j in solicitud.atributos:
                        if j.nombre == 'ValorLimite':
                            j.valor = 0.9
                            asignado = True
                    if asignado == False:
                        solicitud.valorLimite.valor = 0.9
                        solicitud.atributos.append(solicitud.valorLimite)

        return solicitud


if __name__ == "__main__":
    app = QApplication(sys.argv)
    solicitud = Solicitud()
    persona = Persona()
    criterio = Criterio("criterio")
    valor, solicitud = criterio.execute(persona, solicitud)
    print("Valor total de la solicitud:", valor)
    print("Descripción de la solicitud:", solicitud.descripcion)
    sys.exit(app.exec_())
