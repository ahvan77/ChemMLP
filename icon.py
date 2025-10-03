from PySide6.QtGui import QIcon
import os

def MyIcon(self):
    icon_path = os.path.abspath(os.path.dirname(__file__)) + '/pixfig/icon.png'
    
    if os.path.isfile(icon_path):
        self.setWindowIcon(QIcon(icon_path))
    else:
        print(f"Icon file not found: {icon_path}")

