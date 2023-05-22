# -*- coding: utf-8 -*-
"""
Created on Mon May 9 11:20:44 2023

@author: Alfonso Cabezas Fernández
"""

import sys
from PyQt4 import QtGui
import ckVstValoracion

app = QtGui.QApplication(sys.argv)
form = ckVstValoracion.ValoracionDlg()
sys.exit(app.exec_())