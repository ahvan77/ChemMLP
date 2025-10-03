import pypdf
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image

def manual1():    
    root = tk.Toplevel()
    # Open the PDF file
    with open('Manual.pdf', 'rb') as pdf_file:
        pdf_reader = pypdf.PdfReader(pdf_file)
        # Get the number of pages
        num_pages = len(pdf_reader.pages)
        # Create a Tkinter window
        
        # Create a Text widget to display the PDF's contents
        text_widget = Text(root, width=80)
     #   text_widget.grid(row=0, column=0, stciky=tk.W)
   #     while True:
    #        text_widget.delete(0.0, tk.END)
   #     text_widget.pack(padx = 20, pady = 20)

    count = 0
            # Iterate through all the pages
    for i in range(num_pages):
                # Get the i-th page
                page = pdf_reader.pages[i]
                
                for img in page.images:
                    with open(str(count) + img.name, "wb") as fp:
                        fp.write(img.data)
                        img1 = Image.open(str(count) + img.name)
                        img2 = ImageTk.PhotoImage(img1)
                        text_widget.image_create("current",image=img2)
                        count += 1
                    
                # Extract the text from the page
                text = page.extract_text()
                # Insert the text into the Text widget
                label = Label(root, text=text)
                label.pack()
       #         text_widget.insert(tk.END, text)
            # Run the Tkinter event loop
    root.mainloop()