import json
import os
import objects as obj
from PyQt5 import QtWidgets, QtCore

class Exercitiu(QtWidgets.QWidget):
	def __init__(self, enunt, rasp):
		self.enunt = enunt
		self.raspunsuri_corecte = rasp
		self.raspunsuri_user = []

	def setupUi(self, Form):
		Form.setObjectName("Form")
		Form.resize(500, 200)

		self.layout = QtWidgets.QVBoxLayout()
		Form.setLayout(self.layout)

		self.enunt = QtWidgets.QLabel(self.enunt)
		self.enunt.setObjectName("enunt")
		self.enunt.setWordWrap(True)
		self.layout.addWidget(self.enunt)

		self.options = QtWidgets.QHBoxLayout()

		self.A = QtWidgets.QCheckBox('A')
		self.A.setObjectName("A")
		self.B = QtWidgets.QCheckBox('B')
		self.B.setObjectName("B")
		self.C = QtWidgets.QCheckBox('C')
		self.C.setObjectName("C")
		self.D = QtWidgets.QCheckBox('D')
		self.D.setObjectName("D")

		self.options.addWidget(self.A)
		self.options.addWidget(self.B)
		self.options.addWidget(self.C)
		self.options.addWidget(self.D)

		self.layout.addLayout(self.options)

		QtCore.QMetaObject.connectSlotsByName(Form)	

last = []

class Subiect(QtWidgets.QWidget):
	def __init__(self, path, stack):
		
		super().__init__()

		self.exercitii = []
		self.stack = stack	

		with open(path, 'r') as file:
			data = json.load(file)
			self.titlu = data["titlu"]

			for i in data["Exercitii"]:
				ex = Exercitiu(data["Exercitii"][i]["Enunt"], data["Exercitii"][i]["Raspunsuri"])
				ex.raspunsuri_user = []

				self.exercitii.append(ex)

	def setupUi(self, Subiect):
	
		Subiect.setObjectName("Subiect")
		Subiect.resize(580, 880)
	
		self.layout = QtWidgets.QVBoxLayout()
		self.layout.addStretch(True)
		Subiect.setLayout(self.layout)

		self.titlu = QtWidgets.QLabel(self.titlu)
		self.titlu.setObjectName("titlu")
		self.layout.addWidget(self.titlu)

		for i in self.exercitii:
			w = QtWidgets.QWidget()
			i.setupUi(w)
			self.layout.addWidget(w, stretch = 1)
	
		QtCore.QMetaObject.connectSlotsByName(Subiect)
class Page(QtWidgets.QWidget):
	def __init__(self, path, stack):
		super().__init__()
		self.path = path	
		self.stack = stack

	def setupUi(self, Page):
		self.layout = QtWidgets.QVBoxLayout()
		Page.setLayout(self.layout)
		
		for i in os.listdir(self.path):
			b = QtWidgets.QPushButton(i)
			b.clicked.connect(lambda : self.open_dir(i))
			self.layout.addWidget(b)
		
		self.back = QtWidgets.QPushButton("Back")
		self.back.clicked.connect(self.back_func)
		self.layout.addWidget(self.back)

	def open_dir(self, dir_name):
	
		last.append(self.stack.currentWidget())	
	
		if 'json' in dir_name:
			wsub = QtWidgets.QWidget() 
			sub = obj.Subiect("Subiecte/UBB/Info/2024/august.json", self.stack) 
			
			sub.setupUi(wsub)     
			
			central_widget = QtWidgets.QWidget()
			layout = QtWidgets.QVBoxLayout()
			central_widget.setLayout(layout)
 
			scroll = QtWidgets.QScrollArea() 
			scroll.setWidgetResizable(True) 
			scroll.setWidget(wsub) 
			scroll.setFixedHeight(700) 
	 
			back = QtWidgets.QPushButton("Back")
			back.clicked.connect(self.back_func)

			layout.addWidget(scroll)
			layout.addWidget(back)
			self.stack.addWidget(central_widget)   
			self.stack.setCurrentWidget(central_widget) 
		else:	
			self.path = self.path + '/' + dir_name
			page = Page(self.path, self.stack)
			wpage = QtWidgets.QWidget()
			page.setupUi(wpage)

			self.stack.addWidget(wpage)
			self.stack.setCurrentWidget(wpage)
	
	def back_func(self):
		self.stack.setCurrentWidget(last[len(last)-1])
		last.pop()

class Ui_MeniuPrincipal(QtWidgets.QWidget):
	def setupUi(self, MeniuPrincipal):

		MeniuPrincipal.setObjectName("MeniuPrincipal")
		MeniuPrincipal.resize(800, 600)

		self.titlu = QtWidgets.QLabel(MeniuPrincipal)
		self.titlu.setGeometry(QtCore.QRect(50, 110, 771, 111))
		self.titlu.setObjectName("titlu")

		self.button = QtWidgets.QPushButton(MeniuPrincipal)
		self.button.setGeometry(QtCore.QRect(300, 310, 180, 90))
		self.button.setFixedSize(180, 90)
		self.button.setStyleSheet("font: 36pt \"Sans Serif\";")
		self.button.setObjectName("button")

		self.retranslateUi(MeniuPrincipal)
		QtCore.QMetaObject.connectSlotsByName(MeniuPrincipal)

	def retranslateUi(self, MeniuPrincipal):
		_translate = QtCore.QCoreApplication.translate
		MeniuPrincipal.setWindowTitle(_translate("MeniuPrincipal", "Form"))
		self.titlu.setText(_translate("MeniuPrincipal", "<html><head/><body><p><span style=\" font-size:72pt;\">Meniu Princpial</span></p><p><br/></p></body></html>"))
		self.button.setText(_translate("MeniuPrincipal", "Button"))
