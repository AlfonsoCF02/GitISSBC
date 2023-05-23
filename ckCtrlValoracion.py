"""
Created on Mon May 22 19:22:19 2023

Base de conocimiento de valoracion de Becas

@author: Alfonso Manuel de la Torre Osuna
"""

import sys
from PyQt5 import QtWidgets
import ckModValoracion as ma
    
##
#	
#
def eventoValorar(persona, solicitud):
    """
    Método encargado de ejecutar el Método de decidir caso para la valoración
    de la persona indicada junto con la solicitud

    @param persona: Persona solicitante
    @param solicitud: Solicitud realizada 
    """
    
    mp = ma.DecidirCaso(persona, solicitud)
    return mp.execute()
