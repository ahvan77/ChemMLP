import subprocess
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox

class ChempropDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chemprop arguments")
        self.arguments = {}
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.initUI()

    def initUI(self):
        self.line_edits = {}
        for arg in ["--train_path", "--test_path", "--config_path", "--dataset_type", "--num_folds", "--split_type"]:
            label = QLabel(arg, self)
            line_edit = QLineEdit(self)
            self.line_edits[arg] = line_edit
            layout = QHBoxLayout()
            layout.addWidget(label)
            layout.addWidget(line_edit)
            self.layout().addLayout(layout)

        num_molecules_label = QLabel("--number_of_molecules", self)
        self.num_molecules_spin_box = QSpinBox(self)
        self.num_molecules_spin_box.setMinimum(1)
        self.num_molecules_spin_box.setMaximum(100)
        self.num_molecules_spin_box.setValue(1)
        layout = QHBoxLayout()
        layout.addWidget(num_molecules_label)
        layout.addWidget(self.num_molecules_spin_box)
        self.layout().addLayout(layout)

        smiles_label = QLabel("--smiles_columns", self)
        self.smiles_line_edit = QLineEdit(self)
        layout = QHBoxLayout()
        layout.addWidget(smiles_label)
        layout.addWidget(self.smiles_line_edit)
        self.layout().addLayout(layout)

        target_label = QLabel("--target_columns", self)
        self.target_line_edit = QLineEdit(self)
        layout = QHBoxLayout()
        layout.addWidget(target_label)
        layout.addWidget(self.target_line_edit)
        self.layout().addLayout(layout)

        button_box = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        button_box.addWidget(ok_button)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_box.addWidget(cancel_button)
        self.layout().addLayout(button_box)

    def accept(self):
        for arg, line_edit in self.line_edits.items():
            self.arguments[arg] = line_edit.text()
        self.arguments["--number_of_molecules"] = str(self.num_molecules_spin_box.value())
        self.arguments["--smiles_columns"] = self.smiles_line_edit.text()
        self.arguments["--target_columns"] = self.target_line_edit.text()
        super().accept()

def run_chemprop(arguments):
    args = ["python", "-m", "chemprop.train"]
    for arg, value in arguments.items():
        args.extend([arg, value])

    subprocess.run(args)

# This code below should only be executed if this script is run as the main program
if __name__ == '__main__':
    dialog = ChempropDialog()
    if dialog.exec_() == QDialog.Accepted:
        arguments = {
            "--train_path": dialog.arguments["--train_path"],
            "--test_path": dialog.arguments["--test_path"],
            "--config_path": dialog.arguments["--config_path"],
            "--dataset_type": dialog.arguments["--dataset_type"],
            "--num_folds": dialog.arguments["--num_folds"],
            "--split_type": dialog.arguments["--split_type"],
            "--number_of_molecules": dialog.arguments["--number_of_molecules"],
            "--smiles_columns": dialog.arguments["--smiles_columns"],
            "--target_columns": dialog.arguments["--target_columns"],
        }

        run_chemprop(arguments)
