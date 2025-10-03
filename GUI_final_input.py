from tkinter import *
from tkinter import filedialog


def inputs():
    def select_file():
    
        
        file_path = filedialog.askopenfilename()
        file_name = file_path.split("/")[-1]
        return file_name
    
    window = Toplevel()
 #   window.title('Open input file (.csv)')
 #   window.geometry('400x100')
    
    button = tk.Button(window,text="Select File", command=lambda: select_file_and_close(window))
 #   button.pack()
    
    def select_file_and_close(window):
        pixmappath = os.path.abspath(os.path.dirname(__file__)) + '/Data/'
        file_name = select_file()
        textfile = open(pixmappath + 'input_temp.txt', 'w')
        textfile.write(file_name)
        textfile.close()
  #      window.quit()
   #     window.destroy()
        return file_name
    
    #file_name = root.mainloop()
    file_name = window.mainloop()