# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'meniu_principal.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MeniuPrincipal(object):
    def setupUi(self, MeniuPrincipal):
        MeniuPrincipal.setObjectName("MeniuPrincipal")
        MeniuPrincipal.resize(800, 600)
        self.titlu = QtWidgets.QLabel(MeniuPrincipal)
        self.titlu.setGeometry(QtCore.QRect(50, 110, 771, 111))
        self.titlu.setObjectName("titlu")
        self.buton = QtWidgets.QPushButton(MeniuPrincipal)
        self.buton.setGeometry(QtCore.QRect(300, 310, 181, 91))
        self.buton.setStyleSheet("font: 36pt \"Sans Serif\";")
        self.buton.setObjectName("buton")

        self.retranslateUi(MeniuPrincipal)
        QtCore.QMetaObject.connectSlotsByName(MeniuPrincipal)

    def retranslateUi(self, MeniuPrincipal):
        _translate = QtCore.QCoreApplication.translate
        MeniuPrincipal.setWindowTitle(_translate("MeniuPrincipal", "Form"))
        self.titlu.setText(_translate("MeniuPrincipal", "<html><head/><body><p><span style=\" font-size:72pt;\">Meniu Princpial</span></p><p><br/></p></body></html>"))
        self.buton.setText(_translate("MeniuPrincipal", "Buton"))
