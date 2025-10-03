import pandas as pd
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.model_selection import KFold
from math import sqrt
from sklearn.metrics import mean_squared_error
import sklearn
import data_xy
from sklearn.preprocessing import StandardScaler
import sys
from PySide6.QtWidgets import QLineEdit, QFrame, QTextEdit, QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QDialog,QGridLayout, QMessageBox
from PySide6 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtGui import QIcon
from icon import MyIcon
from Err import error
import csv
import os
import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, execute
import math
import random
import matplotlib.pyplot as plt
from scipy.optimize import minimize

class LinerR(QDialog):
    def __init__(self, parent=None):

        super().__init__(parent)
        self.init_ui()

    def  init_ui(self):   
       # self.setGeometry(100, 100, 50, 50)
        self.pixmappath = os.path.abspath(os.path.dirname(__file__)) + '/Data/'
        self.setWindowTitle('Variational Quantum Regression parameters')
        MyIcon(self)
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)
        
        
        self.label7 = QLabel('K-Fold :', self)
        grid_layout.addWidget(self.label7, 0, 0)
        self.line_edit7 = QLineEdit(self)
        grid_layout.addWidget(self.line_edit7, 0, 1)
        
        self.button1 = QPushButton('Run', self)
        self.button1.clicked.connect(self.run_svr)
        grid_layout.addWidget(self.button1, 1, 2)
        
        
    def run_svr(self):
        try:

                k_fold = int(self.line_edit7.text())
         
                
                index1, index, target, df, X, y, df1, X_test1 = data_xy.input0()
                y = y.reshape(-1,1)
                
                def is_power_of_two(n):
                    return (n & (n - 1) == 0) and n != 0
                
                while not is_power_of_two(len(X)):
                    # randomly choose an index to delete
                    idx = np.random.randint(len(X))
                    
                    # delete the corresponding rows in X and y
                    X = np.delete(X, idx)
                    y = np.delete(y, idx)
                
                xnorm = np.linalg.norm(X)          # normalise vectors x and y
                ynorm = np.linalg.norm(y)
                x = X/xnorm
                y = y/ynorm
                #x = x[:,0]
                #y = y[:,0]
                # check if the length of the arrays is a power of two
                
                N = len(x)
                nqubits = math.ceil(np.log2(N)) 
                circ = QuantumCircuit(nqubits+1)   # create circuit
                vec = np.concatenate((x,y))/np.sqrt(2)    # concatenate x and y as above, with renormalisation
                
                circ.initialize(vec, range(nqubits+1))
                circ.h(nqubits)                    # apply hadamard to bottom qubit
                
                #circ.draw()                  # draw the circuit
                
                #Creates a quantum circuit to calculate the inner product between two normalised vectors
                
                def inner_prod(vec1, vec2):
                    #first check lengths are equal
                    if len(vec1) != len(vec2):
                        raise ValueError('Lengths of states are not equal')
                        
                    circ = QuantumCircuit(nqubits+1)
                    vec = np.concatenate((vec1,vec2))/np.sqrt(2)
                    
                    circ.initialize(vec, range(nqubits+1))
                    circ.h(nqubits)
                
                    backend = Aer.get_backend('statevector_simulator')
                  #  run_options = {"shots": 1024, "max_parallel_threads": 4}
                    run_options = {}
                    job = execute(circ, backend, **{"zero_threshold": 1e-20, **run_options})
                
                    result = job.result()
                    o = np.real(result.get_statevector(circ))
                
                    m_sum = 0
                    for l in range(N):
                        m_sum += o[l]**2
                        
                    return 2*m_sum-1
                
               # print("The inner product of x and y equals: ", inner_prod(x,y))
                
                #Implements the entire cost function by feeding the ansatz to the quantum circuit which computes inner products
                
                def calculate_cost_function(parameters):
                
                    a, b = parameters
                    
                    ansatz = a*x + b                        # compute ansatz
                    ansatzNorm = np.linalg.norm(ansatz)     # normalise ansatz
                    ansatz = ansatz/ansatzNorm
                    
                    y_ansatz = ansatzNorm/ynorm * inner_prod(y,ansatz)     # use quantum circuit to test ansatz
                                                                           # note the normalisation factors
                    return (1-y_ansatz)**2
                
                
                def calculate_cost_function_n(parameters):
                    
                    ansatz = parameters[0]                   # compute ansatz
                
                    for i in range(1,len(parameters)):
                
                        ansatz += parameters[i] * x**i
                        
                    ansatzNorm = np.linalg.norm(ansatz)      # normalise ansatz
                    ansatz = ansatz/ansatzNorm
                    y_ansatz = ansatzNorm/ynorm * inner_prod(y,ansatz)     # use quantum circuit to test ansatz
                                                                           # note the normalisation factors

                    return (1-y_ansatz)**2
#                a = 1.0
 #               b = 1.0
            #    print("Cost function for a =", a, "and b =", b, "equals:", calculate_cost_function([a,b]))
                x0 = [10,0.5]                 # initial guess for a and b
             #   order = 1

              #  x0 = [random.uniform(0,2) for p in range(order+1)]  
                #now use different classical optimisers to see which one works best
                
                out = minimize(calculate_cost_function, x0=x0, method="BFGS", options={'maxiter':200}, tol=1e-6)
                out1 = minimize(calculate_cost_function, x0=x0, method="COBYLA", options={'maxiter':200}, tol=1e-6)
                out2 = minimize(calculate_cost_function, x0=x0, method="Nelder-Mead", options={'maxiter':200}, tol=1e-6)
                out3 = minimize(calculate_cost_function, x0=x0, method="CG", options={'maxiter':200}, tol=1e-6)
                out4 = minimize(calculate_cost_function, x0=x0, method="trust-constr", options={'maxiter':200}, tol=1e-6)
                
                out_a1 = out1['x'][0]
                out_b1 = out1['x'][1]
                
                out_a = out['x'][0]
                out_b = out['x'][1]
                
                out_a2 = out2['x'][0]
                out_b2 = out2['x'][1]
                
                out_a3 = out3['x'][0]
                out_b3 = out3['x'][1]
                
                out_a4 = out4['x'][0]
                out_b4 = out4['x'][1]

                y_BFGS = out_a*x + out_b
              #  ansatzNorm = np.linalg.norm(y_BFGS)     # normalise ansatz
              #  y_BFGS = y_BFGS/ansatzNorm
                
                y_COBYLA = out_a1*x + out_b1
               # ansatzNorm = np.linalg.norm(y_COBYLA)     # normalise ansatz
               # y_COBYLA = y_COBYLA/ansatzNorm
                
                y_Nelder_Mead = out_a2*x + out_b2
               # ansatzNorm = np.linalg.norm(y_Nelder_Mead)     # normalise ansatz
              #  y_Nelder_Mead = y_Nelder_Mead/ansatzNorm
                
                y_CG = out_a3*x + out_b3
               # ansatzNorm = np.linalg.norm(y_CG)     # normalise ansatz
              #  y_CG = y_CG/ansatzNorm
                
                y_trust_constr = out_a4*x + out_b4
              #  ansatzNorm = np.linalg.norm(y_trust_constr)     # normalise ansatz
             #   y_trust_constr = y_trust_constr/ansatzNorm
                
             #   print(y,x, y_BFGS)
                CF = {'BFGS': calculate_cost_function([out_a,out_b]), 'COBYLA': calculate_cost_function([out_a1,out_b1]), 'Nelder-Mead': calculate_cost_function([out_a2,out_b2]), 'CG': calculate_cost_function([out_a3,out_b3]),'trust_constr': calculate_cost_function([out_a4,out_b4])}
                #print(out_a4,out_b4)
                #print("Cost function for a =", out_a1, "and b =", out_b1, "equals:", calculate_cost_function([out_a1,out_b1]))
                #print("Cost function for a =", out_a2, "and b =", out_b2, "equals:", calculate_cost_function([out_a2,out_b2]))
                #print("Cost function for a =", out_a3, "and b =", out_b3, "equals:", calculate_cost_function([out_a3,out_b3]))
                #print("Cost function for a =", out_a4, "and b =", out_b4, "equals:", calculate_cost_function([out_a4,out_b4]))

                y1 = y*ynorm
                textfile = open(self.pixmappath + 'Output.txt', 'w')
                
                APE_BFGS=100*(abs(y1 - y_BFGS)/y1)
                APE_COBYLA=100*(abs(y1 - y_COBYLA)/y1)
                APE_Nelder_Mead =100*(abs(y1 - y_Nelder_Mead )/y1)
                APE_CG=100*(abs(y1 - y_CG)/y1)
                APE_trust_constr=100*(abs(y1 - y_trust_constr)/y1)
                
                textfile.write('========================= '+ '\n')
             #   print(out_a, out_b)
                textfile.write("BFGS: Cost function for a = {} and b = {} equals: {} \n".format(out_a, out_b, calculate_cost_function([out_a,out_b])) )
                textfile.write('========================= '+ '\n')
                textfile.write('y_test ' + 'y_predict'+ '\n') 
                data = np.column_stack([y1,y_BFGS])
                np.savetxt(textfile , data, fmt=['%d','%-4d'])
                textfile.write('========================= '+ '\n')
                textfile.write("COBYLA: Cost function for a = {} and b = {} equals: {} \n)".format(out_a1, out_b1, calculate_cost_function([out_a1,out_b1])) )
                textfile.write('========================= '+ '\n')
                textfile.write('y_test ' + 'y_predict'+ '\n') 
                data = np.column_stack([y1,y_COBYLA])
                np.savetxt(textfile , data, fmt=['%d','%-4d'])
                textfile.write('========================= '+ '\n')
                textfile.write("Nelder-Mead: Cost function for a = {} and b = {} equals: {} \n)".format(out_a2, out_b2, calculate_cost_function([out_a2,out_b2])) )
                textfile.write('========================= '+ '\n')
                textfile.write('y_test ' + 'y_predict'+ '\n') 
                data = np.column_stack([y1,y_Nelder_Mead])
                np.savetxt(textfile , data, fmt=['%d','%-4d'])
                textfile.write('========================= '+ '\n')
                textfile.write( "CG: Cost function for a = {} and b = {} equals: {} \n)".format(out_a3, out_b3, calculate_cost_function([out_a3,out_b3])) )
                textfile.write('========================= '+ '\n')
                textfile.write('y_test ' + 'y_predict'+ '\n') 
                data = np.column_stack([y1,y_CG])
                np.savetxt(textfile , data, fmt=['%d','%-4d'])
                textfile.write('========================= '+ '\n')
                textfile.write( "trust_constr: function for a = {} and b = {} equals: {} \n)".format(out_a4, out_b4, calculate_cost_function([out_a4,out_b4])) )
                textfile.write('========================= '+ '\n')
                textfile.write('y_test ' + 'y_predict'+ '\n') 
                data = np.column_stack([y1,y_trust_constr])
                np.savetxt(textfile , data, fmt=['%d','%-4d'])
                textfile.write('========================= '+ '\n')

                textfile.close()     #   self.root.mainloop()
                            

                

                dialog = QtWidgets.QDialog()
                dialog.setWindowTitle('Variational Quantum Regression model Results')
                MyIcon(dialog)
                
                layout = QtWidgets.QVBoxLayout(dialog)

                text_widget = QtWidgets.QLabel()
                figure_widget = QtWidgets.QWidget()
                        
                layout.addWidget(text_widget)
                layout.addWidget(figure_widget)
                
                text_widget.setText("Features: \n")
                layout.addWidget(text_widget)
                
 
                for x in index1:
                    text_widget.setText(text_widget.text()+' '.join(x)+'\n')

                text_widget.setText(text_widget.text()+'========================= \n')   
                text_widget.setText(text_widget.text()+'The Accuracy of BFGS method is: ' + str(100-np.mean(APE_BFGS)) + '\n')
                text_widget.setText(text_widget.text()+'The Accuracy of COBYLA method is: ' + str(100-np.mean(APE_COBYLA)) + '\n')
                text_widget.setText(text_widget.text()+'The Accuracy of Nelder-Mead method is: ' + str(100-np.mean(APE_Nelder_Mead)) + '\n')
                text_widget.setText(text_widget.text()+'The Accuracy of CG method is: ' + str(100-np.mean(APE_CG)) + '\n')
                text_widget.setText(text_widget.text()+'The Accuracy of trust_constr method is: ' + str(100-np.mean(APE_trust_constr)) + '\n')

                fig, ax = plt.subplots()
                y = y*ynorm
                ax.scatter(y, y_BFGS, label='BFGS')
                ax.scatter(y, y_COBYLA, label='COBYLA')
                ax.scatter(y, y_Nelder_Mead, label='Nelder-Mead')
                ax.scatter(y, y_CG, label='CG')
                ax.scatter(y, y_trust_constr, label='trust_constr')
                ax.legend()
                ax.set_xlabel(target+'_test')
                ax.set_ylabel(target+'_prediction')
                ax.set_title('Variational Quantum Regression')
                
                canvas = FigureCanvas(fig)
                layout.addWidget(canvas)
                canvas.destroyed.connect(fig.clf)
                dialog.exec_()

                
                textfile = open(self.pixmappath +'VQR_'+'Output.txt', 'w')
                min_value = min(CF.values())
                min_key = min(CF, key=CF.get)
                min_index = next(index for index, value in enumerate(CF.values()) if value == min_value)
                Method = {'BFGS':out['x'] , 'COBYLA':out1['x'], 'Nelder-Mead':out2['x'], 'CG':out3['x'], 'trust_constr':out4['x']}
                
                for index, (key, value) in enumerate(Method.items()):
                    
                    if key == min_key:
                        x_pred = np.linalg.norm(X_test1)
                        Predictions1 = value[0]*(X_test1/x_pred) + value[1]
                       # print(predictions1)
                        
                        
                    
                
                        
                df1[target+'_prediction']=Predictions1
                df1.to_csv(self.pixmappath +'VQR_Output.csv', index=False, line_terminator='\n')
                textfile.close()    
                

        except Exception as e:
            error(e)          

def QLR():

  #  app = QApplication(sys.argv)
    window = LinerR()
    window.show()
    window.exec_()   
#QLR()    