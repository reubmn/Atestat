import sys 
from PyQt5 import QtWidgets, uic
from UI import meniu_principal, meniu_secundar

class MainMenu(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
	
		# Load widget class from .py

		self.ui = meniu_principal.Ui_MeniuPrincipal()
		self.ui.setupUi(self) 

class SecondMenu(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.ui = meniu_secundar.Ui_MeniuSecundar()
		self.ui.setupUi(self)
		

class MainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.stack = QtWidgets.QStackedWidget()
		self.setCentralWidget(self.stack)

		# Menu1

		self.meniu1 = MainMenu()
		self.start_button = self.meniu1.ui.buton
		self.start_button.clicked.connect(self.start)
		self.stack.addWidget(self.meniu1)
		
		# Menu2

		self.meniu2 = SecondMenu()
		self.stack.addWidget(self.meniu2)
		self.back_button = self.meniu2.ui.back 
		self.back_button.clicked.connect(self.back)

	def start(self):
		self.show_menu(self.meniu2)
	
	def back(self):
		self.show_menu(self.meniu1)

	def show_menu(self, menu):
		self.stack.setCurrentWidget(menu)	

def render():
	app = QtWidgets.QApplication(sys.argv)

	window = MainWindow()

	window.setFixedWidth(800)
	window.setFixedHeight(600) 

	window.show()

	app.exec_()

