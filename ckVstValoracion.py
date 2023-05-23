"""
Created on Mon May 22 19:22:19 2023

Base de conocimiento de valoracion de Becas

@author: Alfonso Cabezas Fernández
"""

#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton,QHeaderView,QVBoxLayout
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
        self.labelTableWidgetDatosPersonales = QtWidgets.QLabel("Datos del Solicitante", self)
        self.labelTableWidgetDatosSolicitud = QtWidgets.QLabel("Datos de la solicitud", self)
        self.labelTableWidgetDatosAbstraidos = QtWidgets.QLabel("Datos Abstraidos", self)


        self.labelTextDecision = QtWidgets.QLabel("Decisión", self)
        self.labelTextExplicacion = QtWidgets.QLabel("Explicacion", self)

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

        self.labelComboBoxDominio = QtWidgets.QLabel("Dominio", self)
        self.comboBoxDominio = QtWidgets.QComboBox()
        self.comboBoxDominio.addItem('Becas')
        self.comboBoxDominio.addItem('Prestamos')
        self.comboBoxDominio.activated[str].connect(self.dominioModificado)

        # Botones
        self.valorarButtom = QPushButton(QIcon("./Valorar.png"), "Valorar", self)
        self.valorarButtom.setShortcut("Ctrl+v")
        
        self.borrarButtom = QPushButton(QIcon("./Delete.png"), "Borrar", self)
        self.borrarButtom.setShortcut("Ctrl+b")
        
        self.salirButtom = QPushButton(QIcon("./exit24.png"), "Salir", self)
        self.salirButtom.setShortcut("Ctrl+s")
    
    # Widgets Verticales Derecha
        v1 = QVBoxLayout()
        v1.addWidget(self.labelTableWidgetDatosAbstraidos)
        v1.addWidget(self.tableWidgetDatosAbstraidos)
        v1.addWidget(self.labelTextExplicacion)
        v1.addWidget(self.plainTextEditExplicacion)
        
    # Widgets Verticales izquierda
        v2 = QVBoxLayout()
        v2.addWidget(self.labelComboBoxDominio)
        v2.addWidget(self.comboBoxDominio)
        v2.addWidget(self.labelTableWidgetDatosPersonales)
        v2.addWidget(self.tableWidgetPersona)
        v2.addWidget(self.tableWidgetPersonap)
        self.tableWidgetPersonap.hide()
        v2.addWidget(self.labelTableWidgetDatosSolicitud)
        v2.addWidget(self.tableWidgetSolicitud)
        v2.addWidget(self.tableWidgetSolicitudp)
        self.tableWidgetSolicitudp.hide()
        v2.addWidget(self.labelTextDecision)
        v2.addWidget(self.plainTextEditDecision)

    # Botones
        bt = QtWidgets.QHBoxLayout()
        bt.addWidget(self.valorarButtom)
        bt.addWidget(self.borrarButtom)
        bt.addWidget(self.salirButtom)


    # Horizontales juntos
        hl = QtWidgets.QHBoxLayout()
        hl.addLayout(v2)
        hl.addLayout(v1)
        
    # Diseño principal
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(hl)
        mainLayout.addLayout(bt)
        self.setLayout(mainLayout)

    # Hacer que las columnas de la tablas deocupen todo el espacio disponible
        self.tableWidgetSolicitud.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetSolicitud.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidgetSolicitudp.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetSolicitudp.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidgetPersona.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetPersona.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidgetPersonap.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetPersonap.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        # Dimensiones de la ventana
        self.setGeometry(150, 150, 1700, 900)
        self.setWindowTitle("TAREA DE VALORACIÓN")
        self.showMaximized()

        # Conexiones:
        # ==========
        self.valorarButtom.clicked.connect(self.valorar)
        self.salirButtom.clicked.connect(self.close)
        self.borrarButtom.clicked.connect(self.borrarInterfaz)
        self.comboBoxDominio.activated[str].connect(self.dominioModificado)


    def rellenaDatosPersonales(self):
        self.etiquetasHeader = ['ATRIBUTO', 'VALOR']
    
        self.tableWidgetPersona = self.crearTablaWidget(self.persona.atributos)
        self.tableWidgetPersonap = self.crearTablaWidget(self.personap.atributos)
    
    def crearTablaWidget(self, atributos):
        tableWidget = QtWidgets.QTableWidget(len(atributos), 2)
        tableWidget.setColumnWidth(0, 150)
        tableWidget.setColumnWidth(1, 150)
        tableWidget.setHorizontalHeaderLabels(self.etiquetasHeader)
    
        for i, atributo in enumerate(atributos):
            label = QtWidgets.QTableWidgetItem(atributo.nombre)
            label.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            tableWidget.setItem(i, 0, label)
    
            if atributo.tipo == 'multiple' or atributo.tipo == 'boleano':
                widget = QtWidgets.QComboBox()
                for posibleValor in atributo.posiblesValores:
                    if isinstance(posibleValor, str):
                        widget.addItem(posibleValor)
                    else:
                        widget.addItem(str(posibleValor))
                tableWidget.setCellWidget(i, 1, widget)
            else:
                widget = QtWidgets.QTableWidgetItem('')
                tableWidget.setItem(i, 1, widget)
    
        return tableWidget

        
    def rellenaDatosSolicitud(self):
        self.etiquetasHeader = ['ATRIBUTO', 'VALOR']
    
        self.tableWidgetSolicitud = self.crearTablaWidgetDS(self.solicitud.atributos)
        self.tableWidgetSolicitudp = self.crearTablaWidgetDS(self.solicitudp.atributos)
    
    def crearTablaWidgetDS(self, atributos):
        tableWidget = QtWidgets.QTableWidget(len(atributos), 2)
        tableWidget.setColumnWidth(0, 150)
        tableWidget.setColumnWidth(1, 150)
        tableWidget.setHorizontalHeaderLabels(self.etiquetasHeader)
    
        for i, atributo in enumerate(atributos):
            label = QtWidgets.QTableWidgetItem(atributo.nombre)
            label.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            tableWidget.setItem(i, 0, label)
    
            if atributo.tipo == 'multiple' or atributo.tipo == 'boleano':
                widget = QtWidgets.QComboBox()
                for posibleValor in atributo.posiblesValores:
                    if isinstance(posibleValor, str):
                        widget.addItem(posibleValor)
                    else:
                        widget.addItem(str(posibleValor))
                tableWidget.setCellWidget(i, 1, widget)
            else:
                widget = QtWidgets.QTableWidgetItem('')
                tableWidget.setItem(i, 1, widget)
    
        return tableWidget


    def rellenaAbstraidos(self):
        self.tableWidgetDatosAbstraidos.clear()
        self.tableWidgetDatosAbstraidos.setColumnCount(2)
        self.tableWidgetDatosAbstraidos.setColumnWidth(0, 150)
        self.tableWidgetDatosAbstraidos.setColumnWidth(1, 150)
        self.tableWidgetDatosAbstraidos.setHorizontalHeaderLabels(self.etiquetasHeader)
        
        atributos = []
        
        if self.dominio == 'Becas':
            atributos = self.solicitud.atributos + self.persona.atributos
        elif self.dominio == 'Prestamos':
            atributos = self.solicitudp.atributos + self.personap.atributos
        
        self.tableWidgetDatosAbstraidos.setRowCount(len(atributos))
        
        for i, atributo in enumerate(atributos):
            label = QtWidgets.QTableWidgetItem(atributo.nombre)
            label.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            self.tableWidgetDatosAbstraidos.setItem(i, 0, label)
            
            valor = QtWidgets.QTableWidgetItem(str(atributo.valor))
            valor.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            self.tableWidgetDatosAbstraidos.setItem(i, 1, valor)
        
        
        # Hacer que las columnas de la tablas deocupen todo el espacio disponible
        self.tableWidgetDatosAbstraidos.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetDatosAbstraidos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


    
    def center(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topRight())

    def valorar(self):
        if self.obtenerInformacionObjeto():
            if self.dominio == 'Becas':
                resultado, descripcion = ctrl.eventoValorar(self.persona, self.solicitud)
                self.solicitud.descripcion = u''
            elif self.dominio == 'Prestamos':
                resultado, descripcion = ctrl.eventoValorar(self.personap, self.solicitudp)
                self.solicitudp.descripcion = u''
                
            self.plainTextEditDecision.clear()
            self.plainTextEditExplicacion.clear()
            self.tableWidgetDatosAbstraidos.clear()
            
            if resultado:
                self.plainTextEditDecision.insertPlainText("Concedida")
            else:
                self.plainTextEditDecision.insertPlainText("Denegada")
                
            self.plainTextEditExplicacion.insertPlainText(descripcion)
            self.rellenaAbstraidos()


    def obtenerInformacionObjeto(self):
        informacionCorrecta = True
        tableWidgets = [self.tableWidgetPersona, self.tableWidgetSolicitud]
        objetos = [self.persona, self.solicitud]
    
        if self.dominio == 'Prestamos':
            tableWidgets = [self.tableWidgetPersonap, self.tableWidgetSolicitudp]
            objetos = [self.personap, self.solicitudp]
    
        for widget, objeto in zip(tableWidgets, objetos):
            for i in range(widget.rowCount()):
                atributo = objeto.atributos[i]
                item = widget.item(i, 1)
                if atributo.tipo == 'str':
                    atributo.valor = item.text()
                elif atributo.tipo == 'int':
                    try:
                        atributo.valor = int(item.text())
                        item.setBackground(QtGui.QColor(255, 255, 255))
                    except:
                        item.setBackground(QtGui.QColor(255, 0, 0))
                        informacionCorrecta = False
                elif atributo.tipo == 'float':
                    try:
                        atributo.valor = float(item.text())
                        item.setBackground(QtGui.QColor(255, 255, 255))
                    except:
                        item.setBackground(QtGui.QColor(255, 0, 0))
                        informacionCorrecta = False
                elif atributo.tipo == 'multiple':
                    atributo.valor = widget.cellWidget(i, 1).currentText()
                elif atributo.tipo == 'boleano':
                    atributo.valor = (widget.cellWidget(i, 1).currentText() == 'True')
    
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
