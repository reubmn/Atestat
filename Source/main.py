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

login_window = interface.LoginWindow()

if login_window.exec_() == QtWidgets.QDialog.Accepted:
    #login reusit, deschide fereastra principala
    window = interface.MainWindow(login_window.current_user)
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
"""

"""
    trebuie sa fac ca la logout sa se deschida fereastra de login
    
    sa se deschida windowurile mai natural si sa fie full screen 
    
    informatile sa fie stocate intr-un server
    
    analytics sa aiba grafice care arata bine
    
    sa se poata pune exercitile in categorii
    
    sa se poata incarca exercitii in alte forme decat json si manual
    
    
    
"""
