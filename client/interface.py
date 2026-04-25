from PyQt5 import QtWidgets, QtCore, QtGui
import objects as obj
import auth
import json
import os

last = []

class LoginWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.setupUi()
        
    def setupUi(self):
        self.setObjectName("LoginDialog")
        self.setFixedSize(400, 300)
        self.setWindowTitle("Login")
        
        layout = QtWidgets.QVBoxLayout()
        
        title = QtWidgets.QLabel("Login System")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        self.username_label = QtWidgets.QLabel("Username:")
        self.username_input = QtWidgets.QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        
        self.password_label = QtWidgets.QLabel("Password:")
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        
        button_layout = QtWidgets.QHBoxLayout()
        
        self.login_button = QtWidgets.QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setDefault(True)
        
        self.register_button = QtWidgets.QPushButton("Register")
        self.register_button.clicked.connect(self.show_register_dialog)
        
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.register_button)
        
        layout.addLayout(button_layout)
        
        
        self.status_label = QtWidgets.QLabel("")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
        self.password_input.returnPressed.connect(self.handle_login)
        
    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            self.status_label.setText("Please fill in all fields")
            return
            
        user = auth.authenticate_user(username, password)
          
        if user:
            self.current_user = user
            self.accept()
        else:
            self.status_label.setText("Invalid username or password")
            
    def show_register_dialog(self):
        dialog = RegisterDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.status_label.setText("Registration successful! Please login.")
            self.status_label.setStyleSheet("color: green;")
            
           

class RegisterDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        
    def setupUi(self):
        self.setWindowTitle("Register New User")
        self.setFixedSize(400, 350)
        
        layout = QtWidgets.QVBoxLayout()
        
        title = QtWidgets.QLabel("Create Account")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 15px;")
        layout.addWidget(title)
        
        layout.addWidget(QtWidgets.QLabel("Username:"))
        self.username_input = QtWidgets.QLineEdit()
        layout.addWidget(self.username_input)
        
        layout.addWidget(QtWidgets.QLabel("Password:"))
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        layout.addWidget(QtWidgets.QLabel("Confirm Password:"))
        self.confirm_password_input = QtWidgets.QLineEdit()
        self.confirm_password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.confirm_password_input)
        
        layout.addWidget(QtWidgets.QLabel("Role:"))
        self.role_combo = QtWidgets.QComboBox()
        self.role_combo.addItems(["student", "teacher", "admin"])
        layout.addWidget(self.role_combo)
        
        button_layout = QtWidgets.QHBoxLayout()
        
        register_btn = QtWidgets.QPushButton("Register")
        register_btn.clicked.connect(self.handle_register)
        
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(register_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.status_label = QtWidgets.QLabel("")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
    def handle_register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        role = self.role_combo.currentText()
        
        if not username or not password:
            self.status_label.setText("Please fill in all fields")
            return
            
        if password != confirm_password:
            self.status_label.setText("Passwords do not match")
            return
            
        if len(password) < 4:
            self.status_label.setText("Password must be at least 4 characters")
            return
        
        
        success = auth.create_user(username, password, role)
        if success:
            self.accept()
        else:
            self.status_label.setText("Registration failed")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, current_user):
        super().__init__()
        self.exit_message = "exit"
        self.current_user = current_user
        
        self.stack = QtWidgets.QStackedLayout() 
        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setLayout(self.stack)
        self.setCentralWidget(self.central_widget)

        self.setup_menu_bar()
        
		# Menu

        self.wmeniu1 = QtWidgets.QWidget()
        self.meniu1 = Ui_MeniuPrincipal(self.current_user)
        self.meniu1.setupUi(self.wmeniu1)
	
        self.stack.addWidget(self.wmeniu1)
        self.meniu1.start_button.clicked.connect(self.start_tests)
        if hasattr(self.meniu1, 'upload_button'):
            self.meniu1.upload_button.clicked.connect(self.show_upload_dialog)

        if hasattr(self.meniu1, 'analytics_button'):
            self.meniu1.analytics_button.clicked.connect(self.show_analytics)
        
        
        
    def setup_menu_bar(self):
        menubar = self.menuBar()
        
        user_menu = menubar.addMenu('User')
        
        profile_action = QtWidgets.QAction('Profile', self)
        profile_action.triggered.connect(self.show_profile)
        user_menu.addAction(profile_action)
        
        logout_action = QtWidgets.QAction('Logout', self)
        logout_action.triggered.connect(self.logout)
        user_menu.addAction(logout_action)
        
        exit_action = QtWidgets.QAction('Exit', self)
        exit_action.triggered.connect(self.exit)
        user_menu.addAction(exit_action)
        
        if self.current_user['role'] in ['admin', 'teacher']:
            admin_menu = menubar.addMenu('Admin')
            
            upload_action = QtWidgets.QAction('Upload Tests', self)
            upload_action.triggered.connect(self.show_upload_dialog)
            admin_menu.addAction(upload_action)
            
            analytics_action = QtWidgets.QAction('Analytics', self)
            analytics_action.triggered.connect(self.show_analytics)
            admin_menu.addAction(analytics_action)
            
    def show_profile(self):
        dialog = ProfileDialog(self.current_user, self)
        dialog.exec_()
        
    def exit(self):
        self.exit_message = "exit"
        self.close()
        
    def logout(self):
        while len(last):
            last.pop()

        self.exit_message = "logged out"
        self.close()
    def start_tests(self):
        last.append(self.meniu1)
        page = obj.Page('.', self.stack, self.current_user)
        page.open_dir('Subiecte')
        
    def show_upload_dialog(self):
        if self.current_user['role'] not in ['admin', 'teacher']:
            QtWidgets.QMessageBox.warning(self, "Access Denied", 
                                        "You don't have permission to upload files.")
            return
            
        dialog = UploadDialog(self)
        dialog.exec_()
        
    def show_analytics(self):
        if self.current_user['role'] not in ['admin', 'teacher']:
            QtWidgets.QMessageBox.warning(self, "Access Denied", 
                                        "You don't have permission to view analytics.")
            return
            
        dialog = AnalyticsDialog(self.current_user, self)
        dialog.exec_()
        
        
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

        self.question_layout = QtWidgets.QVBoxLayout()

        self.question_layout.addWidget(QtWidgets.QLabel("Question:"))
        self.question_input = QtWidgets.QTextEdit()
        self.question_input.setMaximumHeight(100)
        self.question_layout.addWidget(self.question_input)

		#Number of options 
        self.question_layout.addWidget(QtWidgets.QLabel("Number of options")) 
        noOptions = QtWidgets.QSpinBox()
        noOptions.setRange(2, 10)
        noOptions.valueChanged.connect(self.noOptionsChanged)
        self.question_layout.addWidget(noOptions)

		#Options 
        self.question_layout.addWidget(QtWidgets.QLabel("Options:"))
        self.options_layouts = [] # used when removing options from a question
        self.option_inputs = []
        self.options_layout = QtWidgets.QVBoxLayout()
        for option in range(0, noOptions.value()):
            option_layout = QtWidgets.QHBoxLayout()
            option_layout.addWidget(QtWidgets.QLabel(str(chr(65+option))))
            input_field = QtWidgets.QLineEdit()
            self.option_inputs.append(input_field)
            option_layout.addWidget(input_field)
            self.options_layouts.append(option_layout)
            self.options_layout.addLayout(option_layout)
        self.question_layout.addLayout(self.options_layout)

        self.question_layout.addWidget(QtWidgets.QLabel("Correct Answers (check all that apply):"))
        self.correct_checkboxes = []
        self.correct_widgets = [] # used when removing options from a question 
        self.correct_layout = QtWidgets.QHBoxLayout()
        
        for option in range(0, noOptions.value()):
            checkbox = QtWidgets.QCheckBox(str(chr(65+option)))
            self.correct_checkboxes.append(checkbox)
            self.correct_widgets.append(checkbox)
            self.correct_layout.addWidget(checkbox)
        
        self.question_layout.addLayout(self.correct_layout)

        button_layout = QtWidgets.QHBoxLayout()
        
        add_btn = QtWidgets.QPushButton("Add Question")
        add_btn.clicked.connect(self.accept)
        
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(add_btn)
        button_layout.addWidget(cancel_btn)
        
        self.question_layout.addLayout(button_layout)

        self.setLayout(self.question_layout)

    def noOptionsChanged(self, value):

        #Remove options
        while len(self.options_layouts) > int(value):
           
            while self.options_layouts[-1].count():
                item = self.options_layouts[-1].takeAt(0)
                if item is not None:
                    widget = item.widget()
                    if widget is not None:
                        widget.hide()
                        widget.setParent(None)
                        widget.deleteLater()
            self.options_layouts[-1].deleteLater()
            self.options_layouts.pop()

            self.option_inputs.pop()

            self.correct_checkboxes.pop()

            self.correct_widgets[-1].deleteLater()
            self.correct_widgets.pop()

        #Add options
        while len(self.options_layouts) < value:
            option_layout = QtWidgets.QHBoxLayout()
            option_layout.addWidget(QtWidgets.QLabel(str(chr(65+len(self.options_layouts)))))
            input_field = QtWidgets.QLineEdit()
            self.option_inputs.append(input_field)
            option_layout.addWidget(input_field)
            self.options_layouts.append(option_layout)
            self.options_layout.addLayout(option_layout)

            checkbox = QtWidgets.QCheckBox(str(chr(65+len(self.options_layouts)-1)))
            self.correct_checkboxes.append(checkbox)
            self.correct_widgets.append(checkbox)
            self.correct_layout.addWidget(checkbox)

    def get_question_data(self):
        question = self.question_input.toPlainText().strip()
        options = {chr(65 + i): input_field.text().strip() for i, input_field in enumerate(self.option_inputs)}
        correct_answers = [chr(65+option) for option, checkbox in enumerate(self.correct_checkboxes) if checkbox.isChecked()]
        
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
             
            user_answers = ", ".join(exercise.raspunsuri_user)
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

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure

def get_user_progress_graph(name) -> Figure:
    fig = Figure()
    ax = fig.add_subplot()
    x = []
    y = []

    tests = auth.get_tests_by_user(name)
    tests = tests['records']
    s = 0 
    cnt = 0    

    for i in tests:
        s += i['percentage']
        cnt+=1
        x.append(s/cnt)       

    for i in range(1, len(x)+1):
        y.append(i)

    ax.plot(y, x)
	
    return fig

class AnalyticsDialog(QtWidgets.QDialog):
    def __init__(self, current_user, parent=None):
        super().__init__(parent)
        self.current_user = current_user
        self.setupUi()	

    def setupUi(self):
        self.setWindowTitle("Analytics Dashboard")
        self.setFixedSize(1200, 900)

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

    def on_selectionChanged(self, selected, deselected):
        if not selected.indexes():
            return

        index = selected.indexes()[0]
        
        row = index.row()
        col = index.column()
        
        item = self.users_table.item(row, col)
        fig = get_user_progress_graph(item.text())
        self.user_graph.figure = fig
        self.user_graph.draw()

    def setup_users_tab(self, tab):
        layout = QtWidgets.QVBoxLayout()
        
        self.users_table = QtWidgets.QTableWidget()
        users = auth.get_all_users()
        
        self.users_table.setColumnCount(5)
        self.users_table.setHorizontalHeaderLabels(["Username", "Role", "Tests Taken", "Average Score", "Member Since"])
        self.users_table.setRowCount(len(users))

        for i, user in enumerate(users):
            self.users_table.setItem(i, 0, QtWidgets.QTableWidgetItem(user['username']))
            self.users_table.setItem(i, 1, QtWidgets.QTableWidgetItem(user['role']))
            self.users_table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(user['stats']['tests_taken'])))
            self.users_table.setItem(i, 3, QtWidgets.QTableWidgetItem(f"{user['stats']['average_score']:.1f}%"))
            self.users_table.setItem(i, 4, QtWidgets.QTableWidgetItem(user['created_date']))

        self.users_table.resizeColumnsToContents()
        layout.addWidget(self.users_table)
        
        # Showing graph for selected user
        
        self.user_graph = FigureCanvas(Figure())
        layout.addWidget(self.user_graph) 
        self.users_table.selectionModel().selectionChanged.connect(self.on_selectionChanged)

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
            results_table.setItem(i, 2, QtWidgets.QTableWidgetItem(f"{record.get('score', 0)}/{record.get('max_score', 1)}"))
            results_table.setItem(i, 3, QtWidgets.QTableWidgetItem(f"{record.get('percentage', 0):.1f}%"))
            results_table.setItem(i, 4, QtWidgets.QTableWidgetItem(record.get('time', 'Unknown')))

        results_table.resizeColumnsToContents()
        layout.addWidget(results_table)
        
        tab.setLayout(layout)
        
class ProfileDialog(QtWidgets.QDialog):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.setupUi()
        
    def setupUi(self):
        self.setWindowTitle("User Profile")
        self.setFixedSize(600, 450)
        
        layout = QtWidgets.QVBoxLayout()
        
        title = QtWidgets.QLabel("User Profile")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 15px;")
        layout.addWidget(title)
        
        
        container = QtWidgets.QWidget()
        container_layout = QtWidgets.QHBoxLayout(container)

        info_layout = QtWidgets.QFormLayout()
        info_layout.setFormAlignment(QtCore.Qt.AlignCenter)

        info_layout.addRow("Username:", QtWidgets.QLabel(self.user['username']))
        info_layout.addRow("Role:", QtWidgets.QLabel(self.user['role']))
        info_layout.addRow("Member since:", QtWidgets.QLabel(self.user['created_date']))
        info_layout.addRow("Tests taken:", QtWidgets.QLabel(str(self.user['stats']['tests_taken'])))
       	info_layout.addRow("Average score:", QtWidgets.QLabel(f"{self.user['stats']['average_score']:.1f}%"))
        

        container_layout.addLayout(info_layout)

        layout.addWidget(container, alignment=QtCore.Qt.AlignCenter)
        
        # Graph

        fig = get_user_progress_graph(self.user['username'])
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        # Close button

        close_btn = QtWidgets.QPushButton("Close")
       	close_btn.clicked.connect(self.accept)
       	layout.addWidget(close_btn)
        

        self.setLayout(layout)



