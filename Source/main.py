from PyQt5 import QtWidgets
import interface
import sys

app = QtWidgets.QApplication(sys.argv)

window = interface.MainWindow()

window.setFixedWidth(800)
window.setFixedHeight(800) 

window.show()

app.exec()
