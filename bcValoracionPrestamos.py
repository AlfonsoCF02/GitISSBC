"""
Created on Mon May 22 19:22:19 2023

Base de conocimiento de valoracion de Prestamos

@author: Alfonso Cabezas Fernández
"""

from bcValoracion import *


class Solicitud(Clase):
	"""
	Clase para la representacion de la solicitud de un prestamo
	@param: Motivo: Compra casa, cambio coche, estudios
	@param: Cantidad: cantidad solcitada
	@param: TiempoDevolucion: tiempo de devolucion del prestamo
	@param: Valor Limite: valor maximo del prestamo.
	"""
		
    
	def __init__(self,nombre=None):
		Clase.__init__(self,nombre=nombre)
        
		self.atMotivo=Atributo('Motivo','multiple',None, None,['Compra de Casa','Cambio Coche','Estudios'])
		self.atCantidad=Atributo('Cantidad','int',None)
		self.atTiempoDevolucion=Atributo('Tiempo Devolucion','int',None)
		self.valorLimite=Atributo('ValorLimite','float',None)        
		self.atributos=[self.atMotivo,self.atCantidad,self.atTiempoDevolucion]
		self.criterio=Criterio("criterio")
		r=AbstraerLimite('r')
		self.reglas=[r]

        


class Persona(Clase):
	"""
	Describe los atributos por los que se caracterizará a una persona solicitante de un prestamo

	@param: Nombre
	@param: Apellidos
	@param: Sueldo Mensual
	@param: Sueldo Anual
	@param: Situacion laboral: parado, trabajo temporal, trabajo fijo.
	@param: Riesgo: alto, medio, bajo
	@param: Solvencia: mucha, poca, media.
	"""
  
	def __init__(self,nombre=None):

		Clase.__init__(self,nombre=nombre)

		self.atNombre=Atributo('Nombre','str',None)
		self.atApellidos=Atributo('Apellidos','str',None)
		self.atSueldoMensual=Atributo('Sueldo Mensual','float', None)
		self.atSueldoAnual=Atributo('Sueldo Anual','float',None)
		self.atSituacionLaboral=Atributo('Situacion Laboral','multiple',None,None,['Parado','Trabajo Temporal','Trabajo Fijo'])
		self.atRiesgo=Atributo('Riesgo','multiple',None,None,['Alto','Medio','Bajo'])
		self.atSolvencia=Atributo('Solvencia','multiple',None,None,['Mucha','Poca','Media'])
		#Se establece la lista de atributos que posee esta clase
		self.atributos=[self.atNombre,self.atApellidos,self.atSueldoAnual,self.atSituacionLaboral]
		r2= AbstraerSolvencia('r2')
		r1= AbstraerSueldoMensual('r1')        
		self.reglas=[r1,r2]


class Criterio(Regla):
    """
    Requisitos aplicados para valorar la concesión de un préstamo
    @return: valor calculado para determinar si es solvente o no.
    """

    def __init__(self, idRegla):
        Regla.__init__(self, idRegla)

    def execute(self, persona, solicitud):
        valor = 0.0

        solvencia = persona.atSolvencia.valor
        if solvencia == 'Mucha':
            solicitud.descripcion += 'La propiedad ' + persona.atSolvencia.nombre + ' con valor ' + solvencia + ' añade 0.7 puntos a la valoración\n'
            valor += 0.7

        situacion_laboral = persona.atSituacionLaboral.valor
        if situacion_laboral == 'Trabajo Fijo':
            solicitud.descripcion += 'La propiedad ' + persona.atSituacionLaboral.nombre + ' con valor ' + situacion_laboral + ' añade 0.4 puntos a la valoración\n'
            valor += 0.4
        elif situacion_laboral == 'Trabajo Temporal':
            solicitud.descripcion += 'La propiedad ' + persona.atSituacionLaboral.nombre + ' con valor ' + situacion_laboral + ' añade 0.2 puntos a la valoración\n'
            valor += 0.2

        return valor, solicitud


  
    
class AbstraerSueldoMensual(Regla):
    """
    Regla básica para abstraer el sueldo mensual del solicitante del préstamo
    @param: sueldoAnual
    @return: sueldo mensual de la persona
    """

    def __init__(self, idRegla):
        Regla.__init__(self, idRegla)

    def execute(self, persona, solicitud):
        mensual = persona.atSueldoAnual.valor / 12.0
        print(mensual)
        asignado = False
        for i in persona.atributos:
            if i.nombre == 'Sueldo Mensual':
                i.valor = mensual
                asignado = True
        if not asignado:
            persona.atSueldoMensual.valor = mensual
            persona.atributos.append(persona.atSueldoMensual)

        return persona
        
    
class AbstraerSolvencia(Regla):
    """
    Regla básica para abstraer la solvencia del solicitante del préstamo
    """

    def __init__(self, idRegla):
        Regla.__init__(self, idRegla)

    def execute(self, persona, solicitud):
        pm = solicitud.atCantidad.valor / solicitud.atTiempoDevolucion.valor

        asignado = False
        solvencia_valor = ''

        for i in persona.atributos:
            if i.nombre == 'Sueldo Mensual':
                sueldo_mensual = i.valor

                if 4 * pm < sueldo_mensual:
                    solvencia_valor = 'Mucha'
                elif 2 * pm < sueldo_mensual:
                    solvencia_valor = 'Media'
                else:
                    solvencia_valor = 'Poca'

                asignar_solvencia(persona, solvencia_valor)

        return persona


def asignar_solvencia(persona, solvencia_valor):
    asignado = False

    for j in persona.atributos:
        if j.nombre == 'Solvencia':
            j.valor = solvencia_valor
            asignado = True
            break

    if not asignado:
        persona.atSolvencia.valor = solvencia_valor
        persona.atributos.append(persona.atSolvencia)

   
class AbstraerLimite(Regla):
    """
    Regla básica para abstraer el límite mínimo para la concesión del préstamo
    """

    def __init__(self, idRegla):
        Regla.__init__(self, idRegla)

    def execute(self, persona, solicitud):
        cantidad = solicitud.atCantidad.valor
        sueldo_mensual = persona.atSueldoMensual.valor

        if cantidad >= 14 * sueldo_mensual:
            self.asignar_valor_limite(solicitud, 0.9)
        elif cantidad >= 8 * sueldo_mensual:
            self.asignar_valor_limite(solicitud, 0.7)
        elif cantidad >= 5 * sueldo_mensual:
            self.asignar_valor_limite(solicitud, 0.6)
        else:
            self.asignar_valor_limite(solicitud, 0.5)

        return solicitud

    def asignar_valor_limite(self, solicitud, valor):
        asignado = False

        for atributo in solicitud.atributos:
            if atributo.nombre == 'ValorLimite':
                atributo.valor = valor
                asignado = True
                break

        if not asignado:
            solicitud.valorLimite.valor = valor
            solicitud.atributos.append(solicitud.valorLimite)

        
