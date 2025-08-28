import json
import os
import auth
import objects as obj
from PyQt5 import QtWidgets, QtCore, QtGui
from datetime import datetime
import shutil

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
        print("Button clicked")
        total_score = 0
        max_score = len(self.exercitii)
        
        for exercise in self.exercitii:
            total_score += exercise.get_score()
        
        percentage = (total_score / max_score) * 100 if max_score > 0 else 0
        
        auth.update_user_stats(self.current_user['username'], total_score, max_score)
        
        analytics_data = {
            "user": self.current_user['username'],
            "test_name": self.test_name,
            "score": total_score,
            "max_score": max_score,
            "percentage": percentage,
            "test_title": self.titlu
        }
        auth.save_analytics_data(analytics_data)
        
        self.show_results(total_score, max_score, percentage)
        
    def show_results(self, score, max_score, percentage):
        dialog = ResultsDialog(score, max_score, percentage, self.exercitii)
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
        
        title = QtWidgets.QLabel("Available Tests")
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

class Ui_MeniuPrincipal(QtWidgets.QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user

    def setupUi(self, MeniuPrincipal):
        MeniuPrincipal.setObjectName("MeniuPrincipal")
        MeniuPrincipal.resize(800, 600)

        main_layout = QtWidgets.QVBoxLayout()
        MeniuPrincipal.setLayout(main_layout)

        self.titlu = QtWidgets.QLabel()
        self.titlu.setText(f"<html><head/><body><p><span style='font-size:48pt; font-weight:bold;'>Test System</span></p><p><span style='font-size:16pt;'>Welcome, {self.current_user['username']}</span></p></body></html>")
        self.titlu.setAlignment(QtCore.Qt.AlignCenter)
        self.titlu.setStyleSheet("padding: 30px;")
        main_layout.addWidget(self.titlu)

        buttons_layout = QtWidgets.QVBoxLayout()
        buttons_layout.setSpacing(20)

        self.start_button = QtWidgets.QPushButton("Start Tests")
        self.start_button.setFixedSize(300, 80)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        if self.current_user['role'] in ['admin', 'teacher']:
            self.upload_button = QtWidgets.QPushButton("Upload Tests")
            self.upload_button.setFixedSize(300, 80)
            self.upload_button.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    font-size: 20px;
                    font-weight: bold;
                    border: none;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
            """)
            
            self.analytics_button = QtWidgets.QPushButton("View Analytics")
            self.analytics_button.setFixedSize(300, 80)
            self.analytics_button.setStyleSheet("""
                QPushButton {
                    background-color: #FF9800;
                    color: white;
                    font-size: 20px;
                    font-weight: bold;
                    border: none;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #F57C00;
                }
            """)

        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QVBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignCenter)
        
        button_layout.addWidget(self.start_button)
        if self.current_user['role'] in ['admin', 'teacher']:
            button_layout.addWidget(self.upload_button)
            button_layout.addWidget(self.analytics_button)
            
        button_container.setLayout(button_layout)
        main_layout.addWidget(button_container)

        stats_label = QtWidgets.QLabel(f"Tests completed: {self.current_user['stats']['tests_taken']} | Average score: {self.current_user['stats']['average_score']:.1f}%")
        stats_label.setAlignment(QtCore.Qt.AlignCenter)
        stats_label.setStyleSheet("color: gray; font-size: 12px; padding: 10px;")
        main_layout.addWidget(stats_label)

        QtCore.QMetaObject.connectSlotsByName(MeniuPrincipal)
        
class UploadDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Upload Test Files")
        self.setFixedSize(500, 400)

        layout = QtWidgets.QVBoxLayout()

        title = QtWidgets.QLabel("Upload New Test")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 15px;")
        layout.addWidget(title)

        file_layout = QtWidgets.QHBoxLayout()
        self.file_path_label = QtWidgets.QLabel("No file selected")
        self.file_path_label.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 3px;")
        
        self.browse_button = QtWidgets.QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_file)
        
        file_layout.addWidget(self.file_path_label)
        file_layout.addWidget(self.browse_button)
        layout.addLayout(file_layout)

        form_layout = QtWidgets.QFormLayout()
        
        self.test_name_input = QtWidgets.QLineEdit()
        form_layout.addRow("Test Name:", self.test_name_input)
        
        self.test_description = QtWidgets.QTextEdit()
        self.test_description.setMaximumHeight(100)
        form_layout.addRow("Description:", self.test_description)
        
        layout.addLayout(form_layout)

        separator = QtWidgets.QLabel("--- OR ---")
        separator.setAlignment(QtCore.Qt.AlignCenter)
        separator.setStyleSheet("font-weight: bold; padding: 10px;")
        layout.addWidget(separator)

        self.create_manual_button = QtWidgets.QPushButton("Create Test Manually")
        self.create_manual_button.clicked.connect(self.create_manual_test)
        layout.addWidget(self.create_manual_button)

        button_layout = QtWidgets.QHBoxLayout()
        
        upload_btn = QtWidgets.QPushButton("Upload")
        upload_btn.clicked.connect(self.upload_file)
        
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(upload_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)

        self.status_label = QtWidgets.QLabel("")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def browse_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Test File", "", "JSON files (*.json);;All Files (*)"
        )
        if file_path:
            self.file_path_label.setText(file_path)
            self.selected_file = file_path

    def upload_file(self):
        if not hasattr(self, 'selected_file'):
            self.status_label.setText("Please select a file")
            self.status_label.setStyleSheet("color: red;")
            return

        test_name = self.test_name_input.text().strip()
        if not test_name:
            self.status_label.setText("Please enter a test name")
            self.status_label.setStyleSheet("color: red;")
            return

        try:
            destination = os.path.join('Subiecte', f"{test_name}.json")
            shutil.copy2(self.selected_file, destination)
            
            self.status_label.setText("File uploaded successfully!")
            self.status_label.setStyleSheet("color: green;")
            
            QtCore.QTimer.singleShot(1500, self.accept)
            
        except Exception as e:
            self.status_label.setText(f"Upload failed: {str(e)}")
            self.status_label.setStyleSheet("color: red;")

    def create_manual_test(self):
        dialog = TestCreatorDialog(self)
        dialog.exec_()

class TestCreatorDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.questions = []
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Create Test Manually")
        self.setFixedSize(700, 600)

        layout = QtWidgets.QVBoxLayout()

        info_layout = QtWidgets.QFormLayout()
        self.title_input = QtWidgets.QLineEdit()
        self.filename_input = QtWidgets.QLineEdit()
        
        info_layout.addRow("Test Title:", self.title_input)
        info_layout.addRow("File Name:", self.filename_input)
        
        layout.addLayout(info_layout)

        self.questions_list = QtWidgets.QListWidget()
        layout.addWidget(QtWidgets.QLabel("Questions:"))
        layout.addWidget(self.questions_list)

        add_question_btn = QtWidgets.QPushButton("Add Question")
        add_question_btn.clicked.connect(self.add_question)
        layout.addWidget(add_question_btn)

        button_layout = QtWidgets.QHBoxLayout()
        
        save_btn = QtWidgets.QPushButton("Save Test")
        save_btn.clicked.connect(self.save_test)
        
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def add_question(self):
        dialog = QuestionDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            question_data = dialog.get_question_data()
            self.questions.append(question_data)
            self.questions_list.addItem(f"Q{len(self.questions)}: {question_data['question'][:50]}...")

    def save_test(self):
        title = self.title_input.text().strip()
        filename = self.filename_input.text().strip()
        
        if not title or not filename or not self.questions:
            QtWidgets.QMessageBox.warning(self, "Error", "Please fill all fields and add at least one question")
            return

        test_data = {
            "titlu": title,
            "Exercitii": {}
        }

        for i, question in enumerate(self.questions, 1):
            test_data["Exercitii"][str(i)] = {
                "Enunt": question["question"],
                "Raspunsuri": question["correct_answers"],
                "Options": question["options"]
            }

        try:
            filepath = os.path.join('Subiecte', f"{filename}.json")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(test_data, f, indent=4, ensure_ascii=False)
            
            QtWidgets.QMessageBox.information(self, "Success", "Test created successfully!")
            self.accept()
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save test: {str(e)}")

class QuestionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Add Question")
        self.setFixedSize(500, 450)

        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(QtWidgets.QLabel("Question:"))
        self.question_input = QtWidgets.QTextEdit()
        self.question_input.setMaximumHeight(100)
        layout.addWidget(self.question_input)

        layout.addWidget(QtWidgets.QLabel("Options:"))
        
        self.option_inputs = {}
        for option in ['A', 'B', 'C', 'D']:
            option_layout = QtWidgets.QHBoxLayout()
            option_layout.addWidget(QtWidgets.QLabel(f"{option}:"))
            input_field = QtWidgets.QLineEdit()
            self.option_inputs[option] = input_field
            option_layout.addWidget(input_field)
            layout.addLayout(option_layout)

        layout.addWidget(QtWidgets.QLabel("Correct Answers (check all that apply):"))
        self.correct_checkboxes = {}
        correct_layout = QtWidgets.QHBoxLayout()
        
        for option in ['A', 'B', 'C', 'D']:
            checkbox = QtWidgets.QCheckBox(option)
            self.correct_checkboxes[option] = checkbox
            correct_layout.addWidget(checkbox)
        
        layout.addLayout(correct_layout)

        button_layout = QtWidgets.QHBoxLayout()
        
        add_btn = QtWidgets.QPushButton("Add Question")
        add_btn.clicked.connect(self.accept)
        
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(add_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_question_data(self):
        question = self.question_input.toPlainText().strip()
        options = {option: input_field.text().strip() for option, input_field in self.option_inputs.items()}
        correct_answers = [option for option, checkbox in self.correct_checkboxes.items() if checkbox.isChecked()]
        
        return {
            "question": question,
            "options": options,
            "correct_answers": correct_answers
        }

class ResultsDialog(QtWidgets.QDialog):
    def __init__(self, score, max_score, percentage, exercises, parent=None):
        super().__init__(parent)
        self.score = score
        self.max_score = max_score
        self.percentage = percentage
        self.exercises = exercises
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Test Results")
        self.setFixedSize(600, 500)

        layout = QtWidgets.QVBoxLayout()

        results_frame = QtWidgets.QFrame()
        results_frame.setStyleSheet("background: #f0f0f0; padding: 20px; border-radius: 10px;")
        results_layout = QtWidgets.QVBoxLayout()

        title = QtWidgets.QLabel("Test Completed!")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #4CAF50;")
        results_layout.addWidget(title)

        score_label = QtWidgets.QLabel(f"Score: {self.score}/{self.max_score} ({self.percentage:.1f}%)")
        score_label.setAlignment(QtCore.Qt.AlignCenter)
        score_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        results_layout.addWidget(score_label)

        if self.percentage >= 80:
            message = "Excellent work! 🎉"
            color = "#4CAF50"
        elif self.percentage >= 60:
            message = "Good job! 👍"
            color = "#FF9800"
        else:
            message = "Keep studying! 📚"
            color = "#f44336"

        message_label = QtWidgets.QLabel(message)
        message_label.setAlignment(QtCore.Qt.AlignCenter)
        message_label.setStyleSheet(f"font-size: 16px; color: {color}; padding: 10px;")
        results_layout.addWidget(message_label)

        results_frame.setLayout(results_layout)
        layout.addWidget(results_frame)

        details_label = QtWidgets.QLabel("Question Details:")
        details_label.setStyleSheet("font-size: 16px; font-weight: bold; padding-top: 20px;")
        layout.addWidget(details_label)

        details_scroll = QtWidgets.QScrollArea()
        details_widget = QtWidgets.QWidget()
        details_layout = QtWidgets.QVBoxLayout()

        for i, exercise in enumerate(self.exercises, 1):
            is_correct = exercise.get_score() == 1
            status_icon = "✓" if is_correct else "✗"
            status_color = "#4CAF50" if is_correct else "#f44336"
            
            question_frame = QtWidgets.QFrame()
            question_frame.setStyleSheet(f"border-left: 3px solid {status_color}; padding: 10px; margin: 5px;")
            question_layout = QtWidgets.QVBoxLayout()
            
            question_header = QtWidgets.QLabel(f"{status_icon} Question {i}")
            question_header.setStyleSheet(f"font-weight: bold; color: {status_color};")
            question_layout.addWidget(question_header)
            
            user_answers = ", ".join(exercise.raspunsuri_user) if exercise.raspunsuri_user else "No answer"
            correct_answers = ", ".join(exercise.raspunsuri_corecte)
            
            answers_label = QtWidgets.QLabel(f"Your answer: {user_answers}\nCorrect: {correct_answers}")
            answers_label.setStyleSheet("font-size: 10px; color: gray;")
            question_layout.addWidget(answers_label)
            
            question_frame.setLayout(question_layout)
            details_layout.addWidget(question_frame)

        details_widget.setLayout(details_layout)
        details_scroll.setWidget(details_widget)
        details_scroll.setWidgetResizable(True)
        layout.addWidget(details_scroll)

        close_btn = QtWidgets.QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        self.setLayout(layout)

class AnalyticsDialog(QtWidgets.QDialog):
    def __init__(self, current_user, parent=None):
        super().__init__(parent)
        self.current_user = current_user
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Analytics Dashboard")
        self.setFixedSize(800, 600)

        layout = QtWidgets.QVBoxLayout()

        title = QtWidgets.QLabel("Analytics Dashboard")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; padding: 20px;")
        layout.addWidget(title)

        tabs = QtWidgets.QTabWidget()

        users_tab = QtWidgets.QWidget()
        self.setup_users_tab(users_tab)
        tabs.addTab(users_tab, "User Statistics")

        results_tab = QtWidgets.QWidget()
        self.setup_results_tab(results_tab)
        tabs.addTab(results_tab, "Test Results")

        layout.addWidget(tabs)

        close_btn = QtWidgets.QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        self.setLayout(layout)

    def setup_users_tab(self, tab):
        layout = QtWidgets.QVBoxLayout()
        
        users_table = QtWidgets.QTableWidget()
        users = auth.get_all_users()
        
        users_table.setColumnCount(5)
        users_table.setHorizontalHeaderLabels(["Username", "Role", "Tests Taken", "Average Score", "Member Since"])
        users_table.setRowCount(len(users))

        for i, user in enumerate(users):
            users_table.setItem(i, 0, QtWidgets.QTableWidgetItem(user['username']))
            users_table.setItem(i, 1, QtWidgets.QTableWidgetItem(user['role']))
            users_table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(user['stats']['tests_taken'])))
            users_table.setItem(i, 3, QtWidgets.QTableWidgetItem(f"{user['stats']['average_score']:.1f}%"))
            users_table.setItem(i, 4, QtWidgets.QTableWidgetItem(user['created_date']))

        users_table.resizeColumnsToContents()
        layout.addWidget(users_table)
        
        tab.setLayout(layout)

    def setup_results_tab(self, tab):
        layout = QtWidgets.QVBoxLayout()
        
        results_table = QtWidgets.QTableWidget()
        analytics_data = auth.get_analytics_data()
        records = analytics_data.get('records', [])
        
        results_table.setColumnCount(5)
        results_table.setHorizontalHeaderLabels(["User", "Test", "Score", "Percentage", "Date"])
        results_table.setRowCount(len(records))

        for i, record in enumerate(records):
            results_table.setItem(i, 0, QtWidgets.QTableWidgetItem(record.get('user', 'Unknown')))
            results_table.setItem(i, 1, QtWidgets.QTableWidgetItem(record.get('test_name', 'Unknown')))
            results_table.setItem(i, 2, QtWidgets.QTableWidgetItem(f"{record.get('score', 0)}/{record.get('max_score', 0)}"))
            results_table.setItem(i, 3, QtWidgets.QTableWidgetItem(f"{record.get('percentage', 0):.1f}%"))
            results_table.setItem(i, 4, QtWidgets.QTableWidgetItem(record.get('timestamp', 'Unknown')))

        results_table.resizeColumnsToContents()
        layout.addWidget(results_table)
        
        tab.setLayout(layout)
