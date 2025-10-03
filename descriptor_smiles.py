from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QIcon, QPixmap
import csv
from PySide6.QtWidgets import *
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from icon import MyIcon
import data_xy
import ML_GUI
import sys
from Err import error
import os
from PySide6.QtGui import QPalette, QColor

class PropertiesDialog(QDialog):
    def __init__(self, mol_file_path, parent=None):
        super(PropertiesDialog, self).__init__(parent)
        self.pixmappath = os.path.abspath(os.path.dirname(__file__)) + '/Data/'
     #   target,index1, index, X, df = data_xy.Check_index()
        try: 
            os.remove(self.pixmappath + 'Data_predict.csv') 
            os.remove(self.pixmappath + 'input_temp_pred.txt') 
        except:
                pass      
            
        self.index1, self.index, target, df, X, y = data_xy.input1()
        try:
            self.index.remove('Encoding Molecules IDs: SMILES')
        except:
            pass

        # Set the window title
        self.setWindowTitle("Molecule Descriptors")
        MyIcon(self)
     #   palette = QPalette()
     #   palette.setColor(QPalette.ColorRole.Window, QColor(169,169,169))  # Red background color
        # Apply the palette to the widget
     #   self.setPalette(palette)
        # Create the labels and line edits for the properties
        self.smiles_label = QLabel("SMILES:")
        self.smiles_edit = QLineEdit()
       # self.smiles_edit.setReadOnly(True)
        self.mol_weight_label = QLabel("Molecular weight:")
        self.mol_weight_edit = QLineEdit()
        self.logp_label = QLabel("LogP:")
        self.logp_edit = QLineEdit()
        self.hbd_label = QLabel("HBD:")
        self.hbd_edit = QLineEdit()
        self.hba_label = QLabel("HBA:")
        self.hba_edit = QLineEdit()

        # Create the checkboxes for the properties
        self.smiles_checkbox = QCheckBox("SMILES From Draw")
        self.smiles_checkbox.setToolTip("SMILES")
        self.smiles_checkbox.setChecked(False)
    #    self.mol_weight_checkbox = QCheckBox("Molecular weight")
    #    self.mol_weight_checkbox.setToolTip("Molecular weight")
    #    self.mol_weight_checkbox.setChecked(False)
    #    self.logp_checkbox = QCheckBox("LogP")
    #    self.logp_checkbox.setToolTip("Wildman-Crippen LogP")
    #    self.logp_checkbox.setChecked(False)
    #    self.hbd_checkbox = QCheckBox("HBD") 
    #    self.hbd_checkbox.setToolTip("Number of H-bond donors")
    #    self.hbd_checkbox.setChecked(False)
    #    self.hba_checkbox = QCheckBox("HBA")
    #    self.hba_checkbox.setToolTip("Number of H-bond acceptors")        
    #    self.hba_checkbox.setChecked(False)
        i = 1
        self.feature_edits = []
        self.feature_checkboxs = []
        layout = QGridLayout()
        for x, Feature in enumerate(self.index):
            i += 1
            if Feature == 'Encoding Molecules IDs: SMILES':
                Feature = 'SMILES'
            Feature_label = QLabel(Feature+' :')
            Feature_edit = QLineEdit()
            Feature_edit.setReadOnly(False)
            Feature_checkbox = QCheckBox(Feature)
            Feature_checkbox.setChecked(True)
            layout.addWidget(Feature_label, i, 0)
            layout.addWidget(Feature_edit, i, 1)
            layout.addWidget(Feature_checkbox, i, 2)
            self.feature_edits.append(Feature_edit)
            self.feature_checkboxs.append(Feature_checkbox)
        
        # Create the submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)

        # Add the labels, line edits, checkboxes, and button to the layout
        
        layout.addWidget(self.smiles_label, 0, 0)
        layout.addWidget(self.smiles_edit, 0, 1)
        layout.addWidget(self.smiles_checkbox, 0, 2)
    #    layout.addWidget(self.mol_weight_label, 1, 0)
    #    layout.addWidget(self.mol_weight_edit, 1, 1)
    #    layout.addWidget(self.mol_weight_checkbox, 1, 2)
    #    layout.addWidget(self.logp_label, 2, 0)
    #    layout.addWidget(self.logp_edit, 2, 1)
    #    layout.addWidget(self.logp_checkbox, 2, 2)
    #    layout.addWidget(self.hbd_label, 3, 0)
    #    layout.addWidget(self.hbd_edit, 3, 1)
    #    layout.addWidget(self.hbd_checkbox, 3, 2)
    #    layout.addWidget(self.hba_label, 4, 0)
    #    layout.addWidget(self.hba_edit, 4, 1)
    #    layout.addWidget(self.hba_checkbox, 4, 2)
        layout.addWidget(self.submit_button, i+1, 0, 1, 3)
        self.setLayout(layout)

        # Load the molecule from the MOL file and extract its properties
        self.mol = Chem.MolFromMolFile(mol_file_path)
        self.smiles_edit.setText(Chem.MolToSmiles(self.mol))
        self.mol_weight_edit.setText(str(rdMolDescriptors.CalcExactMolWt(self.mol)))
        self.logp_edit.setText(str(rdMolDescriptors.CalcCrippenDescriptors(self.mol)[0]))
        self.hbd_edit.setText(str(rdMolDescriptors.CalcNumHBD(self.mol)))
        self.hba_edit.setText(str(rdMolDescriptors.CalcNumHBA(self.mol)))

    
    def submit(self):
        try: 

            # Write the selected properties to the CSV file
            with open(self.pixmappath + 'Data_predict.csv', mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                header = []                             
                selected_properties = []
                
    
                if self.smiles_checkbox.isChecked():
                    header.append('SMILES')
                    selected_properties.append(self.smiles_edit.text())
  #              if self.mol_weight_checkbox.isChecked():
  #                  header.append('Molecular weight')
  #                  selected_properties.append(self.mol_weight_edit.text())
  #              if self.logp_checkbox.isChecked():
  #                  header.append('LogP')
  #                  selected_properties.append(self.logp_edit.text())
  #              if self.hbd_checkbox.isChecked():
  #                  header.append('HBD')
  #                  selected_properties.append(self.hbd_edit.text())
  #              if self.hba_checkbox.isChecked():
  #                  header.append('HBA')
  #                  selected_properties.append(self.hba_edit.text())
                for i in range(len(self.index)):
                    if self.feature_checkboxs[i].isChecked():
                        header.append(self.index[i])
                        selected_properties.append(self.feature_edits[i].text())    
                writer.writerow(header)
                writer.writerow(selected_properties)
        
            # Close the dialog box
            csv_file.close()
            self.accept()
            self.close()
        except Exception as e:
            error(e)      
if __name__ == '__main__':
    
    # The path to the MOL file is provided as a command-line argument
    pixmappath = os.path.abspath(os.path.dirname(__file__)) + '/Data/'
    mol_file_path = pixmappath + 'molecule.mol'
    
    app = QApplication(sys.argv)
    dialog = PropertiesDialog(mol_file_path)
    if dialog.exec_() == QDialog.Accepted:
        MyIcon(app)
        QMessageBox.information(None, "Confirmation & Prediction", "The data prediction file has been selected.")
        try:
            with open(pixmappath + 'input_temp_pred.txt', 'w') as textfile:
                textfile.write(pixmappath + 'Data_predict.csv')
                textfile.close()    
        except Exception as e:
            error(e)    
    ML_GUI.models() 
  #  dialog.exec_() 
 #   dialog.close()
