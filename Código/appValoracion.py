# -*- coding: utf-8 -*-
"""
Created on Mon May 22 19:22:19 2023

@author: Abraham Córdoba Pérez
"""


import sys
from PyQt5.QtWidgets import QApplication
import ckVstValoracion


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ckVstValoracion.ValoracionDlg()
    form.show()
    sys.exit(app.exec_())
