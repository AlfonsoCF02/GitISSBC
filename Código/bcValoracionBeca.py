"""
Created on Mon May 22 19:22:19 2023

Base de conocimiento de valoracion de Becas

@author: Abraham Córdoba Pérez
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

        self.atTipo = Atributo('Tipo', 'multiple', None, None, ['MEC', 'Erasmus', 'Santander'])
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
        self.atNotaMedia = Atributo('MediaExpediente', 'float', None)
        self.atIndependiente = Atributo('Independiente', 'boleano', None, )
        # Se establece la lista de atributos que posee esta clase
        self.atributos = [self.atNotaMedia, self.atIndependiente, self.atRenta, self.atAsignaturasAprobadas, self.atAsignaturasCursadas]
        r1 = AbstraerPorcentaje('r1')
        self.reglas = [r1]


class Criterio(Regla):
    """
    Define el criterio que seguirá el sistema para aceptar o denegar una beca
    @param: Creditos >= 95 +0.7
    @param: Creditos >= 80 y < 95 +0.3
    @param: MediaExpediente >= 7 +0.4
    @param: Renta <= 25000 +0.7
    @param: Independiente == True +0.3
    @return: valor total de la solicitud.
    """

    def __init__(self, idRegla):
        Regla.__init__(self, idRegla)

    def execute(self, persona, solicitud):
        valor = 0.0
        for at in persona.atributos:
            if at.nombre == 'Renta' and at.valor <= 25000:
                descripcion = f"La propiedad {at.nombre} con valor {at.valor} añade 0.7 puntos a la valoración\n"
                solicitud.descripcion += descripcion
                valor += 0.7

            if at.nombre == 'Independiente' and at.valor == True:
                descripcion = f"La propiedad {at.nombre} con valor {at.valor} añade 0.3 puntos a la valoración\n"
                solicitud.descripcion += descripcion
                valor += 0.3
                
            if at.nombre == '%Creditos' and at.valor >= 95:
                descripcion = f"La propiedad {at.nombre} con valor {at.valor} añade 0.7 puntos a la valoración\n"
                solicitud.descripcion += descripcion
                valor += 0.7

            if at.nombre == '%Creditos' and 80 <= at.valor < 95:
                descripcion = f"La propiedad {at.nombre} con valor {at.valor} añade 0.3 puntos a la valoración\n"
                solicitud.descripcion += descripcion
                valor += 0.3

            if at.nombre == 'MediaExpediente' and at.valor >= 7:
                descripcion = f"La propiedad {at.nombre} con valor {at.valor} añade 0.4 puntos a la valoración\n"
                solicitud.descripcion += descripcion
                valor += 0.4

        solicitud.descripcion += f"El valor total de la solicitud obtenido es {valor}\n"
        return valor, solicitud



class AbstraerPorcentaje(Regla):
    """
    Regla básica para abstraer porcentaje de aprobados
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

        if not asignado:
            persona.atCreditosAprobados.valor = porcentaje
            persona.atributos.append(persona.atCreditosAprobados)

        return persona


class AbstraerLimite(Regla):
    """
    Regla básica para abstraer el límite mínimo para la concesión de la beca
    """

    def __init__(self, idRegla):
        Regla.__init__(self, idRegla)

    def execute(self, persona, solicitud):
        for i in solicitud.atributos:
            if i.nombre == 'Tipo':
                tipo_beca = i.valor
                asignado = False
                if tipo_beca == 'MEC':
                    descripcion = 'Para obtener la beca MEC, es necesario contar con una valoración mínima de 0.7 puntos\n'
                    valor_limite = 0.7
                elif tipo_beca == 'Erasmus':
                    descripcion = 'Para obtener la beca Erasmus, es necesario contar con una valoración mínima de 0.5 puntos\n'
                    valor_limite = 0.5
                elif tipo_beca == 'Santander':
                    descripcion = 'Para obtener la beca Santander, es necesario contar con una valoración mínima de 0.9 puntos\n'
                    valor_limite = 1.1

                for j in solicitud.atributos:
                    if j.nombre == 'ValorLimite':
                        j.valor = valor_limite
                        asignado = True

                if not asignado:
                    solicitud.valorLimite.valor = valor_limite
                    solicitud.atributos.append(solicitud.valorLimite)

                solicitud.descripcion += descripcion

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
