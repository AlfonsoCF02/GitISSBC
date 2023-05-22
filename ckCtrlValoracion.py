# -*- coding: utf-8 -*-
"""
Created on Sat May 09 20:14:02 2015

@author: Alberto
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
