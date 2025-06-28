import json
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

		self.A = QtWidgets.QCheckBox(Form)
		self.A.setObjectName("A")
		self.B = QtWidgets.QCheckBox(Form)
		self.B.setObjectName("B")
		self.C = QtWidgets.QCheckBox(Form)
		self.C.setObjectName("C")
		self.D = QtWidgets.QCheckBox(Form)
		self.D.setObjectName("D")

		self.options.addWidget(self.A)
		self.options.addWidget(self.B)
		self.options.addWidget(self.C)
		self.options.addWidget(self.D)

		self.layout.addLayout(self.options)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)
	
	def retranslateUi(self, Form):
		_translate = QtCore.QCoreApplication.translate
		Form.setWindowTitle(_translate("Form", "Form"))
		self.A.setText(_translate("Form", "A"))
		self.B.setText(_translate("Form", "B"))
		self.C.setText(_translate("Form", "C"))
		self.D.setText(_translate("Form", "D"))

class Subiect(QtWidgets.QWidget):
	def __init__(self, path):
		
		super().__init__()

		self.exercitii = []
	
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
		Subiect.setLayout(self.layout)

		self.titlu = QtWidgets.QLabel(self.titlu)
		self.titlu.setObjectName("titlu")
		self.layout.addWidget(self.titlu)

		for i in self.exercitii:
			w = QtWidgets.QWidget()
			i.setupUi(w)
			self.layout.addWidget(w, stretch = 1)
	
		QtCore.QMetaObject.connectSlotsByName(Subiect)

class Ui_MeniuPrincipal(QtWidgets.QWidget):
	def setupUi(self, MeniuPrincipal):

		MeniuPrincipal.setObjectName("MeniuPrincipal")
		MeniuPrincipal.resize(800, 600)

		self.titlu = QtWidgets.QLabel(MeniuPrincipal)
		self.titlu.setGeometry(QtCore.QRect(50, 110, 771, 111))
		self.titlu.setObjectName("titlu")

		self.buton = QtWidgets.QPushButton(MeniuPrincipal)
		self.buton.setGeometry(QtCore.QRect(300, 310, 180, 90))
		self.buton.setFixedSize(180, 90)
		self.buton.setStyleSheet("font: 36pt \"Sans Serif\";")
		self.buton.setObjectName("buton")

		self.retranslateUi(MeniuPrincipal)
		QtCore.QMetaObject.connectSlotsByName(MeniuPrincipal)

	def retranslateUi(self, MeniuPrincipal):
		_translate = QtCore.QCoreApplication.translate
		MeniuPrincipal.setWindowTitle(_translate("MeniuPrincipal", "Form"))
		self.titlu.setText(_translate("MeniuPrincipal", "<html><head/><body><p><span style=\" font-size:72pt;\">Meniu Princpial</span></p><p><br/></p></body></html>"))
		self.buton.setText(_translate("MeniuPrincipal", "Buton"))



class Ui_MeniuSecundar(QtWidgets.QWidget):
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
		
		self.subiect_button = QtWidgets.QPushButton(MeniuSecundar)
		self.subiect_button.setGeometry(QtCore.QRect(330, 280, 121, 41))
		self.subiect_button.setObjectName("subiect_button")

		self.retranslateUi(MeniuSecundar)
		QtCore.QMetaObject.connectSlotsByName(MeniuSecundar)

	def retranslateUi(self, MeniuSecundar):
		_translate = QtCore.QCoreApplication.translate
		MeniuSecundar.setWindowTitle(_translate("MeniuSecundar", "Form"))
		self.scris.setText(_translate("MeniuSecundar", "<html><head/><body><p><span style=\" font-size:36pt;\">Meniu Secundar</span></p></body></html>"))
		self.back.setText(_translate("MeniuSecundar", "Back"))
		self.subiect_button.setText(_translate("MeniuSecundar", "Subiect"))
		
