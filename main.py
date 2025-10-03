from PySide6.QtGui import QGuiApplication, QAction, QIcon ,QPixmap # Import the QGuiApplication module for accessing desktop information
from PySide6.QtWidgets import ( QApplication, QMainWindow, 
                          QMenuBar, QMenu, QLineEdit, QFileDialog, QLabel, 
                          QMessageBox, QPlainTextEdit, QWidget, QStatusBar, QToolBar,)

from PySide6.QtCore import Qt, QSize
import os
import subprocess
#import GUI_final1
import FT 
import ML_GUI
from ptable_widget import PTable
import chemdraw
import Predict_methods
from icon import MyIcon
import sys
from about import About
import read_csv 
import ml_GUI_de
import LASSO
import LR
import PLS
import GBR
import RFR
import KNR
import VR
import ANNew
import GNN_chem
from Err import error
import feature_optimizer 
#import descriptor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.pixmappath = os.path.abspath(os.path.dirname(__file__)) + '/Data/'
        self.pixmappath0 = os.path.abspath(os.path.dirname(__file__)) + '/pixfig/'
        MyIcon(self)
        
      #  self.ptable = PTable()
        self.central_widget = QWidget()

        self.setCentralWidget(self.central_widget)
        self.setGeometry(300,300, 800, 600)
        self.center()
        
        self.setWindowTitle("ChemMLP")
      #  pixmap = QPixmap('background.png')
      #  self.setStyleSheet("background-image: url({});".format(pixmap))
    #    self.setWindowIcon(QIcon(self.pixmappath0 +'icon.png'))
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 800, 600)  # set the same size as the window
        self.pixmap = QPixmap(self.pixmappath0 +'Name.png').scaled(200, 60)
        self.label.setPixmap(self.pixmap)
        self.label.setAlignment(Qt.AlignCenter)  # center the image in the label
        self.setCentralWidget(self.label)
        self.setupMenuBar()
   #     self.setStyleSheet("background-image: url(background.gif")
    #    movie = QMovie("background.gif", QByteArray(), self)
     #   movie.setCacheMode(QMovie.CacheAll)
     #   movie.setSpeed(100)

      #  self.movie_label = QLabel(self)
      #  self.movie_label.setAlignment(Qt.AlignCenter)
      #  self.movie_label.setMovie(movie)
      #  self.movie_label.setGeometry(500, 600, 700, 600)
      #  self.movie_label.move(0, 0)

      #  movie.start()

      ##  text_label = QLabel(self)
      ##  text_label.setText("AtomixAI")
      ##  text_label.setGeometry(0, 0, 700, 500)
      ##  text_label.setAlignment(Qt.AlignCenter)
     ##   text_label.setStyleSheet("color: black; font-size: 48px;") # set the text color and font size
       # self.setupMenuBar()
	#def setupMenuBar(self)
        # Create a menu bar
    def setupMenuBar(self):   
        self.setStatusBar(QStatusBar(self))      
        menu_bar = self.menuBar()

        # Create a File menu
        file_menu = menu_bar.addMenu("&File")

        # Create an Open action
        
        New_action = QAction(QIcon(self.pixmappath0 + 'New.png'), "N&ew", self)
        file_menu.addAction(New_action)
        
        New_menu = QMenu("New", self)
        New_action.setMenu(New_menu)
        
        open_action = QAction(QIcon(self.pixmappath0 + 'open_file.jpg'),"I&nsert", self)
        New_menu.addAction(open_action)
        
        open_menu = QMenu("Insert", self)
        open_action.setMenu(open_menu)

        # Create an Edit action
        
        open_train_action = QAction(QIcon(self.pixmappath0 + 'open_file1.jpg'), "T&rain", self)
        open_menu.addAction(open_train_action)       
        open_train_action.triggered.connect(self.GUI_input)
        
        
        Predict_action = QAction(QIcon(self.pixmappath0 + 'open_file1.jpg'), "P&redict", self)
        open_menu.addAction(Predict_action)
        Predict_menu = QMenu("Predict data", self)
        Predict_action.setMenu(Predict_menu)

     
        from_file_action1 = QAction(QIcon(self.pixmappath0 + 'from_file.png'), "I&nsert manually", self)
        Predict_menu.addAction(from_file_action1)
        from_file_action1.triggered.connect(self.predict_manual)
        
        
        
        Manual_action = QAction(QIcon(self.pixmappath0 + 'Manually.png'), "I&nsert From File", self)
        Predict_menu.addAction(Manual_action)
        Manual_action.triggered.connect(self.GUI_input_predict)
        
        #open_predict_action.triggered.connect(self.GUI_input_predict)
        
        
        open_draw_action = QAction(QIcon(self.pixmappath0 + 'draw.png'),"D&raw", self)
        open_menu.addAction(open_draw_action)
        open_draw_action.triggered.connect(self.GUI_draw)
        
        Feature_action = QAction(QIcon(self.pixmappath0 + 'Features.png'), "F&eature", self)
        New_menu.addAction(Feature_action)
      #  Feature_action.triggered.connect(self.GUI_f)
        
        Feature_menu = QMenu("Feature", self)
        Feature_action.setMenu(Feature_menu)

     
        from_file_action = QAction(QIcon(self.pixmappath0 + 'from_file.png'), "I&nsert from File", self)
        Feature_menu.addAction(from_file_action)
        from_file_action.triggered.connect(self.Feature_file)
        
        
        
        Manual_action = QAction(QIcon(self.pixmappath0 + 'Manually.png'), "I&nsert Manually", self)
        Feature_menu.addAction(Manual_action)
        Manual_action.triggered.connect(self.F_manual)
        
        
        self.exitAction = QAction( QIcon(self.pixmappath0 + 'icons8-Shutdown.png'), 'E&xit',
                                   self, shortcut="Ctrl+Q",
                                   statusTip="Exit the Application",
                                   triggered=self.exitFile)                        
        file_menu.addAction(self.exitAction)  

        
        
        
        #Insert menu
        insert_menu = menu_bar.addMenu("&Insert")

        open_train1_action = QAction(QIcon(self.pixmappath0 + 'train.png'), "T&rain", self)
        insert_menu.addAction(open_train1_action)
        Train_menu = QMenu("Train data", self)
        open_train1_action.setMenu(Train_menu)
        train_from_file_action = QAction(QIcon(self.pixmappath0 + 'from_file.png'), "I&nsert Train Data", self)
        Train_menu.addAction(train_from_file_action)
        train_from_file_action.triggered.connect(self.GUI_input)
        
        Train_add_action = QAction(QIcon(self.pixmappath0 + 'Add_data.png'), "Add Data to Train data", self)
        Train_menu.addAction(Train_add_action)
        Train_add_action.triggered.connect(self.AddRow)
        
        p_action = QAction(QIcon(self.pixmappath0 + 'predict.png'), "P&redict", self)
        insert_menu.addAction(p_action)
        
        p_menu = QMenu("P&redict", self)
        p_action.setMenu(p_menu)
        
        
        p_draw_action = QAction(QIcon(self.pixmappath0 + 'draw.png'),"D&raw Molecule", self)
        p_menu.addAction(p_draw_action)
        p_draw_action.triggered.connect(self.GUI_draw)
        
        p_file_action1 = QAction(QIcon(self.pixmappath0 + 'from_file.png'), "I&nsert SMILES", self)
        p_menu.addAction(p_file_action1)
        p_file_action1.triggered.connect(self.predict_manual)
        
        
        p_Manual_action = QAction(QIcon(self.pixmappath0 + 'Manually.png'), "I&nsert From File", self)
        p_menu.addAction(p_Manual_action)
        p_Manual_action.triggered.connect(self.GUI_input_predict)
        
        f_action = QAction(QIcon(self.pixmappath0 + 'Feature.png'), "F&eature", self)
        insert_menu.addAction(f_action)
        
        f_menu = QMenu("Feature", self)
        f_action.setMenu(f_menu)
        
        fo_action = QAction(QIcon(self.pixmappath0 + 'Feature.png'), "F&eature Optimization", self)
        insert_menu.addAction(fo_action)
        fo_action.triggered.connect(self.Feature_opt)
       # Feature_action = QAction(QIcon(self.pixmappath0 + 'Features.png'), "F&eature", self)
   #     insert_menu.addAction(Feature_action)

        f_Manual_action = QAction(QIcon(self.pixmappath0 + 'Manually.png'), "I&nsert From File", self)
        f_menu.addAction(f_Manual_action)
        f_Manual_action.triggered.connect(self.GUI_input_predict)
        

        F_I_action = QAction(QIcon(self.pixmappath0 + 'Feature_manual.png'), "I&nsert Manually", self)
        f_menu.addAction(F_I_action)
        F_I_action.triggered.connect(self.F_manual)
        
        
        exitAction = QAction( QIcon(self.pixmappath0 + 'icons8-Shutdown.png'), 'E&xit',
                                   self, shortcut="Ctrl+Q",
                                   statusTip="Exit the Application")
        exitAction.triggered.connect(self.exitFile)
        exitAction.setCheckable(True)
        file_menu.addAction(exitAction)  

		# Create a Model menu
        Models_menu = menu_bar.addMenu("&Models")
		
        Reg_action = QAction(QIcon(self.pixmappath0 + 'Reg.png'), "Regression Models", self)
        Models_menu.addAction(Reg_action)
        Reg_menu = QMenu("Reg Models", self)
        Reg_action.setMenu(Reg_menu)
        SVR_action = QAction("SVR", self)
        Reg_menu.addAction(SVR_action)
        SVR_action.triggered.connect(self.SVR)
        Reg_menu.addSeparator()
        
        Lasso_action = QAction("LASSO", self)
        Reg_menu.addAction(Lasso_action)
        Lasso_action.triggered.connect(self.Lasso)
        Reg_menu.addSeparator()
        
        LR_action = QAction("LR", self)
        Reg_menu.addAction(LR_action)
        LR_action.triggered.connect(self.Lr)
        Reg_menu.addSeparator()
        
        PLS_action = QAction("PLS", self)
        Reg_menu.addAction(PLS_action)
        PLS_action.triggered.connect(self.Pls)
        Reg_menu.addSeparator()
        
        GBR_action = QAction("GBR", self)
        Reg_menu.addAction(GBR_action)
        GBR_action.triggered.connect(self.Gbr)
        Reg_menu.addSeparator()
            
        RFR_action = QAction("RFR", self)
        Reg_menu.addAction(RFR_action)
        RFR_action.triggered.connect(self.Rfr)
        Reg_menu.addSeparator()
        
        KNR_action = QAction("KNR", self)
        Reg_menu.addAction(KNR_action)
        KNR_action.triggered.connect(self.Knr)   
        Reg_menu.addSeparator()
        
        VR_action = QAction("VR", self)
        Reg_menu.addAction(VR_action)
        VR_action.triggered.connect(self.Vr)                                     
        Reg_menu.addSeparator()
        
        NN_action = QAction(QIcon(self.pixmappath0 + 'NN.png'), "Neural Network Models", self)
        Models_menu.addAction(NN_action)        
        NN_menu = QMenu("NN Models", self)
        NN_action.setMenu(NN_menu)
        DL_action = QAction("Deep Learning NN", self)
        NN_menu.addAction(DL_action)
        DL_action.triggered.connect(self.DL)
        NN_menu.addSeparator()

        GNN_action = QAction("GNN", self)
        NN_menu.addAction(GNN_action)
        GNN_action.triggered.connect(self.GNN)
        NN_menu.addSeparator()

        
        
        

                # Create a Help menu
        helpMenu = menu_bar.addMenu("Help")
        
                        # Create an About action
        about_action = QAction( QIcon(self.pixmappath0 + 'manual.png'), 'M&anual',
                                    self, statusTip="Displays info about text editor")                       
        helpMenu.addAction(about_action)
        about_action.triggered.connect(self.manual)

        #Help menu
        aboutAct = QAction( QIcon(self.pixmappath0 + 'about.png'), 'A&bout',
                                    self, statusTip="Displays info about text editor")
        helpMenu.addAction(aboutAct)
        aboutAct.triggered.connect(self.aboutHelp)
        
        helpMenu.addSeparator()                    
        aboutQtAction = QAction(QIcon(self.pixmappath0 + 'Qt.jpg'),"About &Qt", self,
                                statusTip="Show the Qt library's About box",
                                triggered=QApplication.aboutQt)
        
        helpMenu.addAction(aboutQtAction)
        
    def SVR(self):
           try:
               ml_GUI_de.SVR2()
           except Exception as e:
               error(e)
               
    def Lasso(self):
           try:
               LASSO.Las()
           except Exception as e:
               error(e)
    def Lr(self):
           try:
               LR.LR()
           except Exception as e:
               error(e)     
    def Pls(self):
           try:
               PLS.PLS()
           except Exception as e:
               error(e) 
    def Gbr(self):
           try:
               GBR.GBR()
           except Exception as e:
               error(e) 
    def Rfr(self):
           try:
               RFR.RFR()
           except Exception as e:
               error(e) 
    def Knr(self):
           try:
               KNR.KNR()
           except Exception as e:
               error(e) 
    def Vr(self):
           try:
               VR.VR()
           except Exception as e:
               error(e) 
    def DL(self):
           try:
               ANNew.ANN()
           except Exception as e:
               error(e)                                                                                      
    def GNN(self):
           try:
               GNN_chem.GNN2()
           except Exception as e:
               error(e)                                       
                                                                                                    
                              
    def aboutHelp(self):
        About.about(self)
		
    def ManualHelp(self):
        About.open_manual(self)                     
    def exitFile(self):
            response = self.msgApp("Confirmation","This will quit the application. Do you want to Continue?")
            if response == "Y":
                QCoreApplication.quit()  # Properly exit the application
#                self.ptable.close()
            #    exit(0) #TODO, how to exit qapplication from within class instance?
            else:
                pass
               # self.editor.logger.debug("Abort closing")
    
    def msgApp(self,title,msg):
        userInfo = QMessageBox.question(self,title,msg,
                                        QMessageBox.Yes | QMessageBox.No)
        if userInfo == QMessageBox.Yes:
            return "Y"
        if userInfo == QMessageBox.No:
            return "N"
        self.close()
   
    def openPtable(self):
        self.ptable.show()
        
    def center(self):
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        window_size = self.geometry()
        self.move((screen_geometry.width() - window_size.width()) // 2, (screen_geometry.height() - window_size.height()) // 2)
    
    def GUI_input(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "ChemMLP", "",
                                                   "CSV Files (*.csv);;All Files (*);;Text Files (*)",
                                                   options=options)
            
        if file_name:
               textfile = open(self.pixmappath+'input_temp.txt', 'w')
               textfile.write(file_name)
               textfile.close()
               MyIcon(self)
               QMessageBox.information(self, "Confirmation", "The Train data file has been selected.")
   

    def GUI_input_predict(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "ChemMLP", "",
                                                   "CSV Files (*.csv);;All Files (*);;Text Files (*)",
                                                   options=options)
        if file_name:
               textfile = open(self.pixmappath + 'input_temp_pred.txt', 'w')
               textfile.write(file_name)
               textfile.close()
               MyIcon(self)
               QMessageBox.information(self, "Confirmation", "The data prediction file has been selected.")

        
    def GUI_draw(self):  
        subprocess.run(["python", "chemdraw.py"])
          #  GUI_final1   

  #  def about(self):
  #      import about_de
  #      about_de.about1()

    def AddRow(self):
        read_csv.add_data()

    def manual(self):
        import manual_de
        manual_de.manual1()

    def Feature_file(self):
        Predict_methods.models()
        ML_GUI.models()
      #  subprocess.run(["python", "ML_GUI.py"])0
    def Feature_opt(self):
           try:
               feature_optimizer.FO()
           except Exception as e:
               error(e)         
      #  ML_GUI.models()
      #  subprocess.run(["python", "ML_GUI.py"])
      
    def F_manual(self):
        FT.FT()
    def predict_manual(self):
        subprocess.run(["python", "descriptor_smiles.py"])   
        #  subprocess.run(["python", "ML_GUI.py"])
        
    def GUI_f(self):
      #  GUI_final1.Planificador()
       # GUI_final1.f1() 
       subprocess.run(["python", "GUI_final1.py"])

    def save_text(self, text):
        with open("text.txt", "w") as f:
            f.write(text)
 
    def exit_app(self):
        QApplication.quit()

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("AtomixAI") 
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"An error occurred: {str(e)}")