import sys 
from PyQt5 import QtWidgets, uic

class Meniu(QtWidgets.QMainWindow):
	def __init__(self):
		super(Meniu, self).__init__()
		uic.loadUi('UI/Meniu.ui', self)

class meniu2(QtWidgets.QMainWindow):
	def __init__(self):
		super(meniu2, self).__init__()
		uic.loadUi('UI/meniu2.ui', self)

def render():
	app = QtWidgets.QApplication(sys.argv)

	meniu = Meniu()
	Meniu2 = meniu2()

	

	app.exec_()

