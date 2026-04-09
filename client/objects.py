import json
import os
import auth
from PyQt5 import QtWidgets, QtCore, QtGui
from datetime import datetime
import shutil
import interface 

class Exercitiu(QtWidgets.QWidget):
    def __init__(self, enunt, rasp, options=None):
        super().__init__()
        self.enunt = enunt
        self.raspunsuri_corecte = rasp
        self.raspunsuri_user = []
        self.options_text = options or {"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 300)

        self.layout = QtWidgets.QVBoxLayout()
        Form.setLayout(self.layout)
        
        self.enunt_label = QtWidgets.QLabel(self.enunt)
        self.enunt_label.setObjectName("enunt")
        self.enunt_label.setWordWrap(True)
        self.enunt_label.setStyleSheet("font-size: 12px; padding: 10px; background: #f0f0f0; border-radius: 5px;")
        self.layout.addWidget(self.enunt_label)
        
        self.options_layout = QtWidgets.QVBoxLayout()

        self.checkboxes = {}
        for option in ['A', 'B', 'C', 'D']:
            checkbox = QtWidgets.QCheckBox(f"{option}. {self.options_text.get(option, f'Option {option}')}")
            checkbox.setObjectName(option)
            checkbox.stateChanged.connect(self.update_user_answers)
            self.checkboxes[option] = checkbox
            self.options_layout.addWidget(checkbox)

        self.layout.addLayout(self.options_layout)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def update_user_answers(self):
        self.raspunsuri_user = []
        for option, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                self.raspunsuri_user.append(option)

    def get_score(self):
        if set(self.raspunsuri_user) == set(self.raspunsuri_corecte):
            return 1
        return 0

last = []
        


class Subiect(QtWidgets.QWidget):
    def __init__(self, path, stack, current_user):
        super().__init__()
        self.exercitii = []
        self.stack = stack
        self.current_user = current_user
        self.test_name = ""

        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.titlu = data["titlu"]
            self.test_name = os.path.basename(path).replace('.json', '')

            for i in data["Exercitii"]:
                ex = Exercitiu(
                    data["Exercitii"][i]["Enunt"], 
                    data["Exercitii"][i]["Raspunsuri"],
                    data["Exercitii"][i].get("Options", {})
                )
                ex.raspunsuri_user = []
                self.exercitii.append(ex)

    def setupUi(self, Subiect):
        Subiect.setObjectName("Subiect")
        Subiect.resize(580, 880)

        self.layout = QtWidgets.QVBoxLayout()
        Subiect.setLayout(self.layout)
        
        self.titlu_label = QtWidgets.QLabel(self.titlu)
        self.titlu_label.setObjectName("titlu")
        self.titlu_label.setStyleSheet("font-size: 18px; font-weight: bold; text-align: center; padding: 15px;")
        self.titlu_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.titlu_label)
        
        user_info = QtWidgets.QLabel(f"User: {self.current_user['username']} | Role: {self.current_user['role']}")
        user_info.setStyleSheet("font-size: 10px; color: gray; padding: 5px;")
        self.layout.addWidget(user_info)
        
        for i, exercise in enumerate(self.exercitii):
            question_frame = QtWidgets.QFrame()
            question_frame.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; margin: 5px; padding: 10px;")
            question_layout = QtWidgets.QVBoxLayout()
            
            question_num = QtWidgets.QLabel(f"Question {i+1}")
            question_num.setStyleSheet("font-weight: bold; font-size: 14px;")
            question_layout.addWidget(question_num)
            
            w = QtWidgets.QWidget()
            exercise.setupUi(w)
            question_layout.addWidget(w)
            
            question_frame.setLayout(question_layout)
            self.layout.addWidget(question_frame)
        
        self.submit_button = QtWidgets.QPushButton("Submit Test")
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
            
        self.submit_button.clicked.connect(self.submit_test)
        self.layout.addWidget(self.submit_button)

        QtCore.QMetaObject.connectSlotsByName(Subiect)

    def submit_test(self):
        total_score = 0
        max_score = len(self.exercitii)
        
        for exercise in self.exercitii:
            total_score += exercise.get_score()
        
        percentage = (total_score / max_score) * 100 if max_score > 0 else 0
       
        self.current_user["stats"]["tests_taken"]+=1
        self.current_user["stats"]["total_score"]+=percentage
        self.current_user["stats"]["average_score"] = self.current_user["stats"]["total_score"] / self.current_user["stats"]["tests_taken"]
        auth.update_user_stats(self.current_user['username'], total_score, max_score)
        
        analytics_data = {
            "user": self.current_user['username'],
            "test_name": self.test_name,
            "score": total_score,
            "max_score": max_score,
            "percentage": percentage,
            "test_title": self.titlu,
			"time" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        auth.save_analytics_data(analytics_data)
        
        self.show_results(total_score, max_score, percentage)
        
    def show_results(self, score, max_score, percentage):
        dialog = interface.ResultsDialog(score, max_score, percentage, self.exercitii)
        dialog.exec_()


class Page(QtWidgets.QWidget):
    def __init__(self, path, stack, current_user=None):
        super().__init__()
        self.path = path
        self.stack = stack
        self.current_user = current_user

    def setupUi(self, Page):
        self.layout = QtWidgets.QVBoxLayout()
        Page.setLayout(self.layout)
        
        title = QtWidgets.QLabel(self.path[11:])
        title.setStyleSheet("font-size: 20px; font-weight: bold; text-align: center; padding: 15px;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(title)
        
        scroll_area = QtWidgets.QScrollArea()
        scroll_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout()
        
        for i in os.listdir(self.path):
            if i.startswith('.'):  
                continue
                
            button = QtWidgets.QPushButton(i.replace('.json', '').replace('_', ' ').title())
            button.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 15px;
                    font-size: 14px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    margin: 2px;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                }
            """)
            button.clicked.connect(lambda checked, x=i: self.open_dir(x))
            scroll_layout.addWidget(button)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        self.layout.addWidget(scroll_area)

        self.back = QtWidgets.QPushButton("← Back to Main Menu")
        self.back.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 14px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.back.clicked.connect(self.back_func)
        self.layout.addWidget(self.back)

    def open_dir(self, dir_name):
        last.append(self.stack.currentWidget())
        
        if '.json' in dir_name:
            sub = Subiect(os.path.join(self.path, dir_name), self.stack, self.current_user)
            sub.setupUi(sub)
            

            central_widget = QtWidgets.QWidget()
            layout = QtWidgets.QVBoxLayout()
            central_widget.setLayout(layout)

            scroll = QtWidgets.QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setWidget(sub)
            scroll.setFixedHeight(700)

            back = QtWidgets.QPushButton("← Back")
            back.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    padding: 8px;
                    border: none;
                    border-radius: 3px;
                }
            """)
            back.clicked.connect(self.back_func)

            layout.addWidget(scroll)
            layout.addWidget(back)
            self.stack.addWidget(central_widget)
            self.stack.setCurrentWidget(central_widget)
        else:
            page = Page(os.path.join(self.path, dir_name), self.stack, self.current_user)
            wpage = QtWidgets.QWidget()
            page.setupUi(wpage)

            self.stack.addWidget(wpage)
            self.stack.setCurrentWidget(wpage)

    def back_func(self):
        current_widget = self.stack.currentWidget()
        if last:
            self.stack.setCurrentWidget(last[-1])
            last.pop()
        self.stack.removeWidget(current_widget)

