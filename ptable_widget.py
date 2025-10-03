#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
import sys
import logging
from PySide6.QtGui import QIcon, QPixmap
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtCore import Signal
import os
from PySide6.QtGui import QPalette, QColor, QActionGroup, QAction
from ptable import ptable

class PTable(QtWidgets.QWidget):
	
    def __init__(self):
        super(PTable, self).__init__()
        self.ptable = ptable
        self.initUI()
		#logging
        self.logger = logging.getLogger()
		
    def initUI(self):
        grid = QtWidgets.QGridLayout()
		#Create actions dictionary and group dictionary
        self.atomActionGroup = QActionGroup(self)
        self.atomActions = {}
        self.pixmappath0 = os.path.abspath(os.path.dirname(__file__)) + '/pixfig/'        

		#for atomname in self.editor.atomtypes.keys(): Gives unsorted list
        for key in self.ptable.keys():
            atomname = self.ptable[key]["Symbol"]
            action = QAction( '%s'%atomname,
								    self, 
								    statusTip="Set atomtype to %s"%atomname,
								    triggered=self.atomtypePush, objectName=atomname,
								    checkable=True)
            self.atomActionGroup.addAction(action)
            self.atomActions[atomname] = action
            if action.objectName() == "C":
                action.setChecked(True)		
		
            button = QtWidgets.QToolButton()
            button.setDefaultAction(action)
            button.setFocusPolicy (Qt.FocusPolicy.NoFocus)
            button.setMaximumWidth(40)
            # Use a stylesheet to give the button a 3D appearance
            button.setStyleSheet("QToolButton {"
                     "border: 2px solid #555555;"
                     "border-radius: 6px;"
                     "padding: 4px;"
                     "background-color: #DDDDDD;"
                     "}"
                     "QToolButton:hover {"
                     "background-color: #BBBBBB;"
                     "}")
			
            if self.ptable[key]["Group"] != None:
               grid.addWidget(button, self.ptable[key]["Period"], self.ptable[key]["Group"])
            else:
                if key <72:
                   grid.addWidget(button, 9, key-54)
                else:
                   grid.addWidget(button, 10, key-86)
		#Ensure spacing between main table and actinides/lathanides			
        grid.addWidget(QtWidgets.QLabel(''), 8,1)

        self.setLayout(grid)   
		
        self.move(300, 150)
        self.setWindowTitle('Periodic Table')
        self.setWindowIcon(QIcon(self.pixmappath0 +'icon.png'))
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0,0,0))  # Red background color
        # Apply the palette to the widget
        self.setPalette(palette)

        # Ensure the widget updates its visual style
        self.setAutoFillBackground(True)
    atomtypeChanged = Signal( str, name="atomtypeChanged")
    def atomtypePush(self):
        sender = self.sender()
        self.atomtypeChanged.emit(sender.objectName())

	#For setting the new atomtype		
    def selectAtomtype(self, atomname):
        if atomname in self.atomActions.keys():
           self.atomActions[atomname].setChecked(True)
        else:
           self.debug.error("Unknown atomtype or key error: %s"%atomname)
				
		
def main():
    app = QApplication(sys.argv)
    pt = PTable()
    pt.selectAtomtype("N")
    pt.show()
    sys.exit (app.exec ())


if __name__ == '__main__':
    main()