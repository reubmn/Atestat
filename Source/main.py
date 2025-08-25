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

window = interface.MainWindow()

window.setFixedWidth(800)
window.setFixedHeight(800) 

setup_directories()
window.show()

app.exec()
