import sys 
from PyQt5 import QtWidgets, uic
import objects as obj

last = []

class MainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()

	
		self.stack = QtWidgets.QStackedLayout() 
		self.central_widget = QtWidgets.QWidget()
		self.central_widget.setLayout(self.stack)
		self.setCentralWidget(self.central_widget)

		# Menu1

		self.wmeniu1 = QtWidgets.QWidget()
		self.meniu1 = obj.Ui_MeniuPrincipal()
		self.meniu1.setupUi(self.wmeniu1)

	
		self.stack.addWidget(self.wmeniu1)
		self.meniu1.buton.clicked.connect(lambda : self.change_page(self.wmeniu2))		
	
		self.stack.setCurrentWidget(self.wmeniu1)

		# Menu2
		
		self.wmeniu2 = QtWidgets.QWidget()
		self.meniu2 = obj.Ui_MeniuSecundar()

		self.meniu2.setupUi(self.wmeniu2)
		self.stack.addWidget(self.wmeniu2)

		self.meniu2.back.clicked.connect(self.back)
		self.meniu2.subiect_button.clicked.connect(lambda : self.change_page(self.scroll))

		# Subiect 
		
		self.wsub = QtWidgets.QWidget()
		self.sub = obj.Subiect("Subiecte/UBB/Info/2024/august.json")
		self.sub.setupUi(self.wsub)	

		self.scroll = QtWidgets.QScrollArea()
		self.scroll.setWidgetResizable(True)
		self.scroll.setWidget(self.wsub)
		self.scroll.setFixedHeight(800)

		self.stack.addWidget(self.scroll)	

	def change_page(self, widget):
		last.append(self.stack.currentIndex())
		self.stack.setCurrentWidget(widget)

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

