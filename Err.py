from PySide6.QtWidgets import  QMessageBox
import traceback
from icon import MyIcon

def error(e):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle('Error')
    MyIcon(msg)
    msg.setText('An error has occurred:\n\n{}'.format(str(e)))
    msg.setDetailedText(traceback.format_exc())
    msg.exec ()