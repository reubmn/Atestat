import sys 
import os
from PyQt5 import QtWidgets, uic
import objects as obj

last = []

class MainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()

		self.path = '.'
	
		self.stack = QtWidgets.QStackedLayout() 
		self.central_widget = QtWidgets.QWidget()
		self.central_widget.setLayout(self.stack)
		self.setCentralWidget(self.central_widget)

		# Menu

		self.wmeniu1 = QtWidgets.QWidget()
		self.meniu1 = obj.Ui_MeniuPrincipal()
		self.meniu1.setupUi(self.wmeniu1)

	
		self.stack.addWidget(self.wmeniu1)
		self.meniu1.button.clicked.connect(self.start)		

	def start(self):
		last.append(self.meniu1)
		# Start creating pages

		page = obj.Page('.', self.stack)
		page.open_dir('Subiecte')	

	def back(self):
		if len(last) > 0:
			self.stack.setCurrentIndex(last[len(last)-1])
			last.pop()

def render():
	app = QtWidgets.QApplication(sys.argv)

	window = MainWindow()

	window.setFixedWidth(800)
	window.setFixedHeight(800) 
	
	window.show()

	app.exec()

