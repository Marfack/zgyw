from multiprocessing import Queue
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.main_window import Ui_MainWindow

def ui_process(ui_q: Queue, pt_q: Queue):
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window, ui_q, pt_q)
    window.show()
    app.exec()
    exit()