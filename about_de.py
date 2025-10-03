import tkinter as tk
from PIL import ImageTk, Image
def about1():
    root = tk.Toplevel()
    canv = tk.Canvas(root, bd=0)
    canv.place(x=10, y=10, width=10, height=10)
    img = (Image.open("icon.gif"))
    resized_image= img.resize((200,200), Image.ANTIALIAS)
    new_image= ImageTk.PhotoImage(resized_image)
    canv.create_image((10, 10), image=new_image, anchor='nw')
    text1 = tk.Text(root, height=20, width=30)
    text1.insert(tk.END, '\n')
    text1.image_create(tk.END, image=new_image)
    
    text1.pack(side=tk.LEFT)
    
    text2 = tk.Text(root, height=20, width=50)
    scroll = tk.Scrollbar(root, command=text2.yview)
    text2.configure(yscrollcommand=scroll.set)
    #text2.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'), justify='center')
    text2.tag_configure('big', font=('Verdana', 20, 'bold'), justify='center')
    text2.tag_configure('color',
                        foreground='#476042',
                        font=('Arial', 10), justify='center')

    text2.insert(tk.END,'\nData prediction software\n', 'big')
    quote = """
    This software can predict based on
    passive observations using various
    Machine learning, and Deep learning methods.
    This version of software is deveoped by python3.9 at: 
    Labratuary of Physical Chemistry of Matter (LPCM)
    at Universite de Sherbrooke, Canada.                
    \nFor more information or assistance please contact me:\n    
             Developer: Sadollah Ebrahimi
             Email: sa.ebrahimi@gmail.com
    """
    text2.insert(tk.END, quote, 'color')
    text2.pack(side=tk.LEFT)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    root.mainloop()