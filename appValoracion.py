# -*- coding: utf-8 -*-
"""
Created on Sat May 09 20:16:02 2015

@author: Alberto
"""

import sys
from PyQt5.QtWidgets import QApplication
import ckVstValoracion


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ckVstValoracion.ValoracionDlg()
    form.show()
    sys.exit(app.exec_())
