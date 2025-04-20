from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow

app = QApplication([])
mainwindow = QMainWindow()
QLabel("Hello, PyQt5",mainwindow)
mainwindow.show()
app.exec_()
