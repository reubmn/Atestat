# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'meniu_secundar.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MeniuSecundar(object):
    def setupUi(self, MeniuSecundar):
        MeniuSecundar.setObjectName("MeniuSecundar")
        MeniuSecundar.resize(800, 600)
        self.scris = QtWidgets.QLabel(MeniuSecundar)
        self.scris.setGeometry(QtCore.QRect(200, 40, 461, 281))
        self.scris.setObjectName("scris")
        self.back = QtWidgets.QPushButton(MeniuSecundar)
        self.back.setGeometry(QtCore.QRect(50, 520, 131, 41))
        self.back.setStyleSheet("font: 24pt \"Sans Serif\";")
        self.back.setObjectName("back")

        self.retranslateUi(MeniuSecundar)
        QtCore.QMetaObject.connectSlotsByName(MeniuSecundar)

    def retranslateUi(self, MeniuSecundar):
        _translate = QtCore.QCoreApplication.translate
        MeniuSecundar.setWindowTitle(_translate("MeniuSecundar", "Form"))
        self.scris.setText(_translate("MeniuSecundar", "<html><head/><body><p><span style=\" font-size:36pt;\">Meniu Secundar</span></p></body></html>"))
        self.back.setText(_translate("MeniuSecundar", "Back"))
