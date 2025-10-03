import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QDialog,QGridLayout,QFileDialog, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel
from icon import MyIcon
from Err import error
import traceback
import subprocess
import ML_GUI
import os

class MyDialog(QDialog):
    def __init__(self, parent=None):
        
        super(MyDialog, self).__init__(parent)
        self.pixmappath = os.path.abspath(os.path.dirname(__file__)) + '/Data/'
        MyIcon(self)
        self.setWindowTitle("Data to Predict")
        # Create combo box to select model type
        self.combo_box = QComboBox()
        self.combo_box.setMinimumSize(200, 30)
        self.combo_box.addItems(['Draw molecule', 'From csv file'])
        
        # Create submit button
        self.submit_button = QPushButton('Run')
        self.submit_button.clicked.connect(self.on_submit)
        
        # Create layout and add widgets
        layout = QGridLayout()
        label = QLabel('Prediction data:')
        font = QFont('Times New Roman', 10)
        label.setFont(font)
        layout.addWidget(self.combo_box, 0, 1)
        layout.addWidget(self.submit_button, 1, 1)
        
        # Set layout
        self.setLayout(layout)
    
        
    def on_submit(self):
        selected_model = self.combo_box.currentText()
        def error(e):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle('Error')
            msg.setText('An error has occurred:\n\n{}'.format(str(e)))
            msg.setDetailedText(traceback.format_exc())
            msg.exec_()   
              
        if selected_model == 'Draw molecule':
            subprocess.run(["python", "chemdraw.py"])
        elif selected_model == 'From csv file':
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getOpenFileName(self, "ChemMPL", "",
                                                   "CSV Files (*.csv);;All Files (*);;Text Files (*)",
                                                   options=options)
            if file_name:
                   textfile = open(self.pixmappath + 'input_temp_pred.txt', 'w')
                   textfile.write(file_name)
                   textfile.close()
                   reply = QMessageBox.information(self, "Confirmation", "The data prediction file has been selected.")
                   if reply:
                       ML_GUI.models() 
def models():
   # app = QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    dialog.exec_()
  #  dialog.close()
#models()  

