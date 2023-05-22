"""
Created on Mon May 22 19:22:19 2023

Base de conocimiento de valoracion de Becas

@author: Alfonso Cabezas Fernández
"""

#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon

from bcValoracion import *
import ckCtrlValoracion as ctrl
import bcValoracionBeca as bccb
import bcValoracionPrestamos as bccv

class ValoracionDlg(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.persona = bccb.Persona()
        self.solicitud = bccb.Solicitud()
        self.personap = bccv.Persona()
        self.solicitudp = bccv.Solicitud()
        self.dominio = 'Becas'

        # Label
        labelTableWidgetDatosPersonales = QtWidgets.QLabel("Datos del Solicitante", self)
        labelTableWidgetDatosSolicitud = QtWidgets.QLabel("Datos de la solicitud", self)
        labelTableWidgetDatosAbstraidos = QtWidgets.QLabel("Datos Abstraidos", self)

        labelTextDecision = QtWidgets.QLabel("Decisión", self)
        labelTextExplicacion = QtWidgets.QLabel("Explicacion", self)

        # Widget
        header = ['ATRIBUTO', 'VALOR']

        self.rellenaDatosPersonales()

        self.rellenaDatosSolicitud()

        # Datos abstraidos
        self.tableWidgetDatosAbstraidos = QtWidgets.QTableWidget(len(self.persona.atributos) + len(self.solicitud.atributos), 2)
        self.tableWidgetDatosAbstraidos.setColumnWidth(0, 240)
        self.tableWidgetDatosAbstraidos.setColumnWidth(1, 300)
        self.tableWidgetDatosAbstraidos.setHorizontalHeaderLabels(header)

        # Decision
        self.plainTextEditDecision = QtWidgets.QPlainTextEdit()
        self.plainTextEditDecision = QtWidgets.QPlainTextEdit(self)
        font = QtGui.QFont()
        font.setPointSize(50)
        self.plainTextEditDecision.setFont(font)
        
        # Explicación
        self.plainTextEditExplicacion = QtWidgets.QPlainTextEdit()

        labelComboBoxDominio = QtWidgets.QLabel("Dominio", self)
        self.comboBoxDominio = QtWidgets.QComboBox()
        self.comboBoxDominio.addItem('Becas')
        self.comboBoxDominio.addItem('Prestamos')
        self.comboBoxDominio.activated[str].connect(self.dominioModificado)

        # Botones
        self.valorarButtom = QPushButton(QIcon("./Valorar.png"), "Valorar", self)
        self.valorarButtom.setShortcut("Ctrl+v")
        
        self.borrarButtom = QPushButton(QIcon("./Delete.png"), "Borrar", self)
        self.borrarButtom.setShortcut("Ctrl+v")
        
        self.salirButtom = QPushButton(QIcon("./exit24.png"), "Salir", self)
        self.salirButtom.setShortcut("Ctrl+s")
        
        self.buttomsLayout = QtWidgets.QHBoxLayout()
        self.buttomsLayout.addStretch()
        self.buttomsLayout.addWidget(self.valorarButtom)
        self.buttomsLayout.addWidget(self.borrarButtom)
        self.buttomsLayout.addWidget(self.salirButtom)
        self.buttomsLayout.addStretch()

        # Rejilla de distribución de los controles
        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(5)

        self.grid.addWidget(labelComboBoxDominio, 6, 0)
        self.grid.addWidget(self.comboBoxDominio, 7, 0)

        self.grid.addWidget(labelTableWidgetDatosPersonales, 0, 0)
        self.grid.addWidget(self.tableWidgetPersona, 1, 0)
        self.grid.addWidget(self.tableWidgetPersonap, 1, 0)
        self.tableWidgetPersonap.hide()
        self.grid.addWidget(labelTableWidgetDatosAbstraidos, 0, 1)

        self.grid.addWidget(labelTableWidgetDatosSolicitud, 2, 0)
        self.grid.addWidget(self.tableWidgetSolicitud, 3, 0)
        self.grid.addWidget(self.tableWidgetSolicitudp, 3, 0)
        self.tableWidgetSolicitudp.hide()

        self.grid.addWidget(labelTextDecision, 4, 0)
        self.grid.addWidget(self.plainTextEditDecision, 5, 0)

        self.grid.addWidget(labelTextExplicacion, 4, 1)
        self.grid.addWidget(self.plainTextEditExplicacion, 5, 1, 3, 1)

        # Diseño principal
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(self.grid)
        mainLayout.addLayout(self.buttomsLayout)
        self.setLayout(mainLayout)

        # Dimensiones de la ventana
        self.setGeometry(300, 300, 1200, 1200)
        self.setWindowTitle("TAREA DE VALORACIÓN")
        self.show()

        self.center()
        # Conexiones:
        # ==========
        self.valorarButtom.clicked.connect(self.valorar)
        self.salirButtom.clicked.connect(self.close)
        self.borrarButtom.clicked.connect(self.borrarInterfaz)



    def rellenaDatosPersonales(self):
        self.etiquetasHeader = ['ATRIBUTO', 'VALOR']
        
        self.tableWidgetPersona = QtWidgets.QTableWidget(len(self.persona.atributos), 2)
        self.tableWidgetPersona.setColumnWidth(0, 150)
        self.tableWidgetPersona.setColumnWidth(1, 150)
        self.tableWidgetPersona.setHorizontalHeaderLabels(self.etiquetasHeader)
        
        for i in range(0, len(self.persona.atributos)):
            label = QtWidgets.QTableWidgetItem(self.persona.atributos[i].nombre)
            label.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            self.tableWidgetPersona.setItem(i, 0, label)
            
            if self.persona.atributos[i].tipo == 'multiple' or self.persona.atributos[i].tipo == 'boleano':
                # Creamos el widget
                widget = QtWidgets.QComboBox()
                
                # Añadimos la información a mostrar correspondiente en función del atributo
                for posibleValor in self.persona.atributos[i].posiblesValores:
                    if posibleValor is not str:
                        widget.addItem(str(posibleValor))
                    else:
                        widget.addItem(posibleValor)
                    
                # Activamos la señal de cambio del widget
                self.tableWidgetPersona.setCellWidget(i, 1, widget)
            else:
                widget = QtWidgets.QTableWidgetItem('')
                self.tableWidgetPersona.setItem(i, 1, widget)
    
        self.tableWidgetPersonap = QtWidgets.QTableWidget(len(self.personap.atributos), 2)
        self.tableWidgetPersonap.setColumnWidth(0, 150)
        self.tableWidgetPersonap.setColumnWidth(1, 150)
        self.tableWidgetPersonap.setHorizontalHeaderLabels(self.etiquetasHeader)
        
        for i in range(0, len(self.personap.atributos)):
            label = QtWidgets.QTableWidgetItem(self.personap.atributos[i].nombre)
            label.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            self.tableWidgetPersonap.setItem(i, 0, label)
            
            if self.personap.atributos[i].tipo == 'multiple' or self.personap.atributos[i].tipo == 'boleano':
                # Creamos el widget
                widget = QtWidgets.QComboBox()
                
                # Añadimos la información a mostrar correspondiente en función del atributo
                for posibleValor in self.personap.atributos[i].posiblesValores:
                    if posibleValor is not str:
                        widget.addItem(str(posibleValor))
                    else:
                        widget.addItem(posibleValor)
                    
                # Activamos la señal de cambio del widget
                self.tableWidgetPersonap.setCellWidget(i, 1, widget)
            else:
                widget = QtWidgets.QTableWidgetItem('')
                self.tableWidgetPersonap.setItem(i, 1, widget)

        
    def rellenaDatosSolicitud(self):
        self.etiquetasHeader = ['ATRIBUTO', 'VALOR']
        
        self.tableWidgetSolicitud = QtWidgets.QTableWidget(len(self.solicitud.atributos), 2)
        self.tableWidgetSolicitud.setColumnWidth(0, 150)
        self.tableWidgetSolicitud.setColumnWidth(1, 150)
        self.tableWidgetSolicitud.setHorizontalHeaderLabels(self.etiquetasHeader)
        
        for i in range(0, len(self.solicitud.atributos)):
            label = QtWidgets.QTableWidgetItem(self.solicitud.atributos[i].nombre)
            label.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            self.tableWidgetSolicitud.setItem(i, 0, label)
            
            if self.solicitud.atributos[i].tipo == 'multiple' or self.solicitud.atributos[i].tipo == 'boleano':
                # Creamos el widget
                widget = QtWidgets.QComboBox()
                
                # Añadimos la información a mostrar correspondiente en función del atributo
                for posibleValor in self.solicitud.atributos[i].posiblesValores:
                    if posibleValor is not str:
                        widget.addItem(str(posibleValor))
                    else:
                        widget.addItem(posibleValor)
                    
                # Activamos la señal de cambio del widget
                self.tableWidgetSolicitud.setCellWidget(i, 1, widget)
            else:
                widget = QtWidgets.QTableWidgetItem('')
                self.tableWidgetSolicitud.setItem(i, 1, widget)
    
        self.tableWidgetSolicitudp = QtWidgets.QTableWidget(len(self.solicitudp.atributos), 2)
        self.tableWidgetSolicitudp.setColumnWidth(0, 150)
        self.tableWidgetSolicitudp.setColumnWidth(1, 150)
        self.tableWidgetSolicitudp.setHorizontalHeaderLabels(self.etiquetasHeader)
        
        for i in range(0, len(self.solicitudp.atributos)):
            label = QtWidgets.QTableWidgetItem(self.solicitudp.atributos[i].nombre)
            label.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            self.tableWidgetSolicitudp.setItem(i, 0, label)
            
            if self.solicitudp.atributos[i].tipo == 'multiple' or self.solicitudp.atributos[i].tipo == 'boleano':
                # Creamos el widget
                widget = QtWidgets.QComboBox()
                
                # Añadimos la información a mostrar correspondiente en función del atributo
                for posibleValor in self.solicitudp.atributos[i].posiblesValores:
                    if posibleValor is not str:
                        widget.addItem(str(posibleValor))
                    else:
                        widget.addItem(posibleValor)
                    
                # Activamos la señal de cambio del widget
                self.tableWidgetSolicitudp.setCellWidget(i, 1, widget)
            else:
                widget = QtWidgets.QTableWidgetItem('')
                self.tableWidgetSolicitudp.setItem(i, 1, widget)


    def rellenaAbstraidos(self):
        self.etiquetasHeader = ['ATRIBUTO', 'VALOR']
        if self.dominio == 'Becas':
            self.tableWidgetDatosAbstraidos = QtWidgets.QTableWidget(len(self.solicitud.atributos) + len(self.persona.atributos), 2)
            self.tableWidgetDatosAbstraidos.setColumnWidth(0, 150)
            self.tableWidgetDatosAbstraidos.setColumnWidth(1, 150)
            self.tableWidgetDatosAbstraidos.setHorizontalHeaderLabels(self.etiquetasHeader)
            for i in range(0, len(self.solicitud.atributos)):
                label = QtWidgets.QTableWidgetItem(self.solicitud.atributos[i].nombre)
                label.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                self.tableWidgetDatosAbstraidos.setItem(i, 0, label)
                
                label1 = QtWidgets.QTableWidgetItem(str(self.solicitud.atributos[i].valor))
                label1.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                self.tableWidgetDatosAbstraidos.setItem(i, 1, label1)
            for i in range(len(self.solicitud.atributos), len(self.persona.atributos) + len(self.solicitud.atributos)):
                label2 = QtWidgets.QTableWidgetItem(self.persona.atributos[i - len(self.solicitud.atributos)].nombre)
                label2.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                self.tableWidgetDatosAbstraidos.setItem(i, 0, label2)
                
                label3 = QtWidgets.QTableWidgetItem(str(self.persona.atributos[i - len(self.solicitud.atributos)].valor))
                label3.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                self.tableWidgetDatosAbstraidos.setItem(i, 1, label3)
            
        if self.dominio == 'Prestamos':
            self.tableWidgetDatosAbstraidos = QtWidgets.QTableWidget(len(self.solicitudp.atributos) + len(self.personap.atributos), 2)
            self.tableWidgetDatosAbstraidos.setColumnWidth(0, 150)
            self.tableWidgetDatosAbstraidos.setColumnWidth(1, 150)
            self.tableWidgetDatosAbstraidos.setHorizontalHeaderLabels(self.etiquetasHeader)
            for i in range(0, len(self.solicitudp.atributos)):
                label = QtWidgets.QTableWidgetItem(self.solicitudp.atributos[i].nombre)
                label.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                self.tableWidgetDatosAbstraidos.setItem(i, 0, label)
                
                label1 = QtWidgets.QTableWidgetItem(str(self.solicitudp.atributos[i].valor))
                label1.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                self.tableWidgetDatosAbstraidos.setItem(i, 1, label1)
            for i in range(len(self.solicitudp.atributos), len(self.personap.atributos) + len(self.solicitudp.atributos)):
                label2 = QtWidgets.QTableWidgetItem(self.personap.atributos[i - len(self.solicitudp.atributos)].nombre)
                label2.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                self.tableWidgetDatosAbstraidos.setItem(i, 0, label2)
                
                label3 = QtWidgets.QTableWidgetItem(str(self.personap.atributos[i - len(self.solicitudp.atributos)].valor))
                label3.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                self.tableWidgetDatosAbstraidos.setItem(i, 1, label3)
        
        self.grid.addWidget(self.tableWidgetDatosAbstraidos, 1, 1, 3, 1)

    
    def center(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topRight())

    def valorar(self):
        if self.obtenerInformacionObjeto():
            if self.dominio == 'Becas':
                resultado, descripcion = ctrl.eventoValorar(self.persona, self.solicitud)
            if self.dominio == 'Prestamos':
                resultado, descripcion = ctrl.eventoValorar(self.personap, self.solicitudp)
                
            self.plainTextEditDecision.clear()
            self.plainTextEditExplicacion.clear()
            self.tableWidgetDatosAbstraidos.clear()
            self.solicitud.descripcion = u''
            self.solicitudp.descripcion = u''
            if resultado == True:
                self.plainTextEditDecision.insertPlainText("Concedida")
                self.plainTextEditExplicacion.insertPlainText(descripcion)
            else:
                self.plainTextEditDecision.insertPlainText("Denegada")
                self.plainTextEditExplicacion.insertPlainText(descripcion)
            self.rellenaAbstraidos()

    def obtenerInformacionObjeto(self):
        informacionCorrecta = True
        if self.dominio == 'Becas':
            for i in range(self.tableWidgetPersona.rowCount()):
                if self.persona.atributos[i].tipo == 'str':
                    self.persona.atributos[i].valor = self.tableWidgetPersona.item(i, 1).text()
                elif self.persona.atributos[i].tipo == 'int':
                    try:
                        self.persona.atributos[i].valor = int(self.tableWidgetPersona.item(i, 1).text())
                        self.tableWidgetPersona.item(i, 1).setBackground(QtGui.QColor(255, 255, 255))
                    except:
                        self.tableWidgetPersona.item(i, 1).setBackground(QtGui.QColor(255, 0, 0))
                        informacionCorrecta = False
                elif self.persona.atributos[i].tipo == 'float':
                    try:
                        self.persona.atributos[i].valor = float(self.tableWidgetPersona.item(i, 1).text())
                        self.tableWidgetPersona.item(i, 1).setBackground(QtGui.QColor(255, 255, 255))
                    except:
                        self.tableWidgetPersona.item(i, 1).setBackground(QtGui.QColor(255, 0, 0))
                        informacionCorrecta = False
                elif self.persona.atributos[i].tipo == 'multiple':
                    self.persona.atributos[i].valor = self.tableWidgetPersona.cellWidget(i, 1).currentText()
                elif self.persona.atributos[i].tipo == 'boleano':
                    if self.tableWidgetPersona.cellWidget(i, 1).currentText() == 'True':
                        self.persona.atributos[i].valor = True
                    else:
                        self.persona.atributos[i].valor = False
    
            for i in range(self.tableWidgetSolicitud.rowCount()):
                if self.solicitud.atributos[i].tipo == 'str':
                    self.solicitud.atributos[i].valor = self.tableWidgetSolicitud.item(i, 1).text()
                elif self.solicitud.atributos[i].tipo == 'int':
                    try:
                        self.solicitud.atributos[i].valor = int(self.tableWidgetSolicitud.item(i, 1).text())
                        self.tableWidgetSolicitud.item(i, 1).setBackground(QtGui.QColor(255, 255, 255))
                    except:
                        self.tableWidgetSolicitud.item(i, 1).setBackground(QtGui.QColor(255, 0, 0))
                        informacionCorrecta = False
                elif self.solicitud.atributos[i].tipo == 'float':
                    try:
                        self.solicitud.atributos[i].valor = float(self.tableWidgetSolicitud.item(i, 1).text())
                        self.tableWidgetSolicitud.item(i, 1).setBackground(QtGui.QColor(255, 255, 255))
                    except:
                        self.tableWidgetSolicitud.item(i, 1).setBackground(QtGui.QColor(255, 0, 0))
                        informacionCorrecta = False
                elif self.solicitud.atributos[i].tipo == 'multiple':
                    self.solicitud.atributos[i].valor = self.tableWidgetSolicitud.cellWidget(i, 1).currentText()
                elif self.solicitud.atributos[i].tipo == 'boleano':
                    if self.tableWidgetSolicitud.cellWidget(i, 1).currentText() == 'True':
                        self.solicitud.atributos[i].valor = True
                    else:
                        self.solicitud.atributos[i].valor = False
        if self.dominio == 'Prestamos':
            for i in range(self.tableWidgetPersonap.rowCount()):
                if self.personap.atributos[i].tipo == 'str':
                    self.personap.atributos[i].valor = self.tableWidgetPersonap.item(i, 1).text()
                elif self.personap.atributos[i].tipo == 'int':
                    try:
                        self.personap.atributos[i].valor = int(self.tableWidgetPersonap.item(i, 1).text())
                        self.tableWidgetPersonap.item(i, 1).setBackground(QtGui.QColor(255, 255, 255))
                    except:
                        self.tableWidgetPersonap.item(i, 1).setBackground(QtGui.QColor(255, 0, 0))
                        informacionCorrecta = False
                elif self.personap.atributos[i].tipo == 'float':
                    try:
                        self.personap.atributos[i].valor = float(self.tableWidgetPersonap.item(i, 1).text())
                        self.tableWidgetPersonap.item(i, 1).setBackground(QtGui.QColor(255, 255, 255))
                    except:
                        self.tableWidgetPersonap.item(i, 1).setBackground(QtGui.QColor(255, 0, 0))
                        informacionCorrecta = False
                elif self.personap.atributos[i].tipo == 'multiple':
                    self.personap.atributos[i].valor = self.tableWidgetPersonap.cellWidget(i, 1).currentText()
                elif self.personap.atributos[i].tipo == 'boleano':
                    if self.tableWidgetPersonap.cellWidget(i, 1).currentText() == 'True':
                        self.personap.atributos[i].valor = True
                    else:
                        self.personap.atributos[i].valor = False
    
            for i in range(self.tableWidgetSolicitudp.rowCount()):
                if self.solicitudp.atributos[i].tipo == 'str':
                    self.solicitudp.atributos[i].valor = self.tableWidgetSolicitudp.item(i, 1).text()
                elif self.solicitudp.atributos[i].tipo == 'int':
                    try:
                        self.solicitudp.atributos[i].valor = int(self.tableWidgetSolicitudp.item(i, 1).text())
                        self.tableWidgetSolicitudp.item(i, 1).setBackground(QtGui.QColor(255, 255, 255))
                    except:
                        self.tableWidgetSolicitudp.item(i, 1).setBackground(QtGui.QColor(255, 0, 0))
                        informacionCorrecta = False
                elif self.solicitudp.atributos[i].tipo == 'float':
                    try:
                        self.solicitudp.atributos[i].valor = float(self.tableWidgetSolicitudp.item(i, 1).text())
                        self.tableWidgetSolicitudp.item(i, 1).setBackground(QtGui.QColor(255, 255, 255))
                    except:
                        self.tableWidgetSolicitudp.item(i, 1).setBackground(QtGui.QColor(255, 0, 0))
                        informacionCorrecta = False
                elif self.solicitudp.atributos[i].tipo == 'multiple':
                    self.solicitudp.atributos[i].valor = self.tableWidgetSolicitudp.cellWidget(i, 1).currentText()
                elif self.solicitudp.atributos[i].tipo == 'boleano':
                    if self.tableWidgetSolicitudp.cellWidget(i, 1).currentText() == 'True':
                        self.solicitudp.atributos[i].valor = True
                    else:
                        self.solicitudp.atributos[i].valor = False
    
        return informacionCorrecta

        
        
    
    def borrarInterfaz(self):
        self.plainTextEditDecision.clear()
        self.plainTextEditExplicacion.clear()
        self.tableWidgetDatosAbstraidos.clear()
    
    def dominioModificado(self, text):
        if self.dominio != text:
            self.dominio = text
            if self.dominio == 'Becas':
                self.tableWidgetPersonap.hide()
                self.tableWidgetSolicitudp.hide()
                self.tableWidgetPersona.show()
                self.tableWidgetSolicitud.show()
            else:
                self.tableWidgetPersona.hide()
                self.tableWidgetSolicitud.hide()
                self.tableWidgetSolicitudp.show()
                self.tableWidgetPersonap.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ValoracionDlg()
    sys.exit(app.exec_())
