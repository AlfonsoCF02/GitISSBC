# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 12:03:13 2015
Base de conocimiento de valoracion de Prestamos
@author: Alberto
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
	Requisitos aplicados para valorar la concesion de un prestamo
	@return: valor calculado para ver si es solvente o no.
	"""
  
	def __init__(self,idRegla):
        
		Regla.__init__(self,idRegla)
             
	def execute(self,persona,solicitud):
        
		valor=0.0
            
		if persona.atSolvencia.valor == 'Mucha':
			solicitud.descripcion+='El atributo '+persona.atSolvencia.nombre+' con valor '+persona.atSolvencia.valor+' proporciona 0.7 puntos de valoracion\n'
			valor=valor+0.7
        
		if persona.atSituacionLaboral.valor == 'Trabajo Fijo':
			solicitud.descripcion+='El atributo '+persona.atSituacionLaboral.nombre+' con valor '+persona.atSituacionLaboral.valor+' proporciona 0.4 puntos de valoracion\n'
			valor=valor+0.4
        
		if persona.atSituacionLaboral.valor == 'Trabajo Temporal':
			solicitud.descripcion+='El atributo '+persona.atSituacionLaboral.nombre+' con valor '+persona.atSituacionLaboral.valor+' proporciona 0.2 puntos de valoracion\n'
			valor=valor+0.2
            
		return valor, solicitud

  
    
class AbstraerSueldoMensual(Regla):
	"""
	Regla basica para abstraer el sueldo mensual del solicitante del prestamo
	@param: sueldoAnual
	@return: sueldo de la persona
	"""  

	def __init__(self,idRegla):
		Regla.__init__(self,idRegla)
  

	def execute(self,persona,solicitud):

		mensual=persona.atSueldoAnual.valor/12.0
		print(mensual)
		asignado=False        
		for i in persona.atributos:
			if i.nombre == 'Sueldo Mensual':
				i.valor=mensual
				asignado=True
		if asignado == False:
			persona.atSueldoMensual.valor=mensual
			persona.atributos.append(persona.atSueldoMensual)
                
		return persona
        
    
class AbstraerSolvencia(Regla):
	"""
	Regla basica para abstraer la solvencia del solicitante del prestamo

	"""    

	def __init__(self,idRegla):
		Regla.__init__(self,idRegla)
  

	def execute(self,persona,solicitud):

		pm=solicitud.atCantidad.valor/solicitud.atTiempoDevolucion.valor
		print(pm)
		asignado=False
		for i in persona.atributos:
			if i.nombre == 'Sueldo Mensual':
				if 4*pm <  i.valor:
					for j in persona.atributos:
						if j.nombre == 'Solvencia':
							j.valor='Mucha'
							asignado=True
					if asignado == False:
						persona.atSolvencia.valor='Mucha'
						persona.atributos.append(persona.atSolvencia)
				elif 2*pm <  i.valor:
					for j in persona.atributos:
						if j.nombre == 'Solvencia':
							j.valor='Media'
							asignado=True
					if asignado == False:
						persona.atSolvencia.valor='Media'
						persona.atributos.append(persona.atSolvencia)
				else:
					for j in persona.atributos:
						if j.nombre == 'Solvencia':
							j.valor='Poca'
							asignado=True
					if asignado == False:
						persona.atSolvencia.valor='Poca'
						persona.atributos.append(persona.atSolvencia)
                       
		return persona
   
class AbstraerLimite(Regla):
	"""
	Regla basica para abstraer el limite minimo para la concesion del prestamo
	"""   	

	def __init__(self,idRegla):
		Regla.__init__(self,idRegla)
        
	def execute(self,persona,solicitud):
        
		for i in solicitud.atributos:
			if i.nombre == 'Cantidad':
				if i.valor >= 12*persona.atSueldoMensual.valor:
					solicitud.descripcion+='Para una cantidad de '+str(i.valor)+' y un sueldo mensual de '+str(persona.atSueldoMensual.valor)+' se requiere un minimo de 0.9 puntos de valoracion para conceder el prestamo\n'
					asignado=False
					for j in solicitud.atributos:
						if j.nombre == 'ValorLimite':
							j.valor=0.9
							asignado = True
					if asignado == False:
						solicitud.valorLimite.valor=0.9
						solicitud.atributos.append(solicitud.valorLimite)
				elif i.valor >= 6*persona.atSueldoMensual.valor:
					solicitud.descripcion+='Para una cantidad de '+str(i.valor)+' y un sueldo mensual de '+str(persona.atSueldoMensual.valor)+' se requiere un minimo de 0.7 puntos de valoracion para conceder el prestamo\n'
					asignado=False
					for j in solicitud.atributos:
						if j.nombre == 'ValorLimite':
							j.valor=0.7
							asignado = True
					if asignado == False:
						solicitud.valorLimite.valor=0.7
						solicitud.atributos.append(solicitud.valorLimite)
				elif i.valor >= 3*persona.atSueldoMensual.valor:
					solicitud.descripcion+='Para una cantidad de '+str(i.valor)+' y un sueldo mensual de '+str(persona.atSueldoMensual.valor)+' se requiere un minimo de 0.5 puntos de valoracion para conceder el prestamo\n'
					asignado=False
					for j in solicitud.atributos:
						if j.nombre == 'ValorLimite':
							j.valor=0.6
							asignado = True
					if asignado == False:
						solicitud.valorLimite.valor=0.5
						solicitud.atributos.append(solicitud.valorLimite)
				elif i.valor < 3*persona.atSueldoMensual.valor:
					solicitud.descripcion+='Para una cantidad de '+str(i.valor)+' y un sueldo mensual de '+str(persona.atSueldoMensual.valor)+' se requiere un minimo de 0.5 puntos de valoracion para conceder el prestamo\n'
					asignado=False
					for j in solicitud.atributos:
						if j.nombre == 'ValorLimite':
							j.valor=0.5
							asignado = True
					if asignado == False:
						solicitud.valorLimite.valor=0.5
						solicitud.atributos.append(solicitud.valorLimite)
                   
        
		return solicitud
        
        
