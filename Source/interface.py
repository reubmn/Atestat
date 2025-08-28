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
        
        if os.path.exists(f'users/{username}.json'):
            self.status_label.setText("Username already exists")
            return
        
        success = auth.create_user(username, password, role)
        if success:
            self.accept()
        else:
            self.status_label.setText("Registration failed")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        
        
        self.stack = QtWidgets.QStackedLayout() 
        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setLayout(self.stack)
        self.setCentralWidget(self.central_widget)

        self.setup_menu_bar()
        
		# Menu

        self.wmeniu1 = QtWidgets.QWidget()
        self.meniu1 = obj.Ui_MeniuPrincipal(self.current_user)
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
        
    def logout(self):
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
            
        dialog = obj.UploadDialog(self)
        dialog.exec_()
        
    def show_analytics(self):
        if self.current_user['role'] not in ['admin', 'teacher']:
            QtWidgets.QMessageBox.warning(self, "Access Denied", 
                                        "You don't have permission to view analytics.")
            return
            
        dialog = obj.AnalyticsDialog(self.current_user, self)
        dialog.exec_()
        
        
        
class ProfileDialog(QtWidgets.QDialog):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.setupUi()
        
    def setupUi(self):
        self.setWindowTitle("User Profile")
        self.setFixedSize(400, 300)
        
        layout = QtWidgets.QVBoxLayout()
        
        title = QtWidgets.QLabel("User Profile")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 15px;")
        layout.addWidget(title)
        
        
        info_layout = QtWidgets.QFormLayout()
        info_layout.addRow("Username:", QtWidgets.QLabel(self.user['username']))
        info_layout.addRow("Role:", QtWidgets.QLabel(self.user['role']))
        info_layout.addRow("Member since:", QtWidgets.QLabel(self.user['created_date']))
        info_layout.addRow("Tests taken:", QtWidgets.QLabel(str(self.user['stats']['tests_taken'])))
        info_layout.addRow("Average score:", QtWidgets.QLabel(f"{self.user['stats']['average_score']:.1f}%"))
        
        layout.addLayout(info_layout)
        
        close_btn = QtWidgets.QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)



