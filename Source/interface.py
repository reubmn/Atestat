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


