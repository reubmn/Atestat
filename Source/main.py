from PyQt5 import QtWidgets
import interface
import os
import sys

def setup_directories():
    dirs = ['users', 'Subiecte', 'analytics', 'uploads', 'user_data']
    for dir_name in dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

app = QtWidgets.QApplication(sys.argv)

setup_directories()

#incepe cu meniul de login (trebuie creeat)
"""
login_window = interface.LoginWindow()

if login_window.exec_() == QtWidgets.QDialog.Accepted:
    #login reusit, deschide fereastra principala
    window = interface.MainWindow()
    window.setFixedWidth(800)
    window.setFixedHeight(800) 
    window.show()
    app.exec()
"""
window = interface.MainWindow()

window.setFixedWidth(800)
window.setFixedHeight(800) 

window.show()

app.exec()
