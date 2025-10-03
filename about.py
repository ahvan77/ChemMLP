import os
from PySide6.QtWidgets import QMessageBox, QFileDialog, QApplication
from PySide6.QtGui import QIcon, QPixmap, QAction
import fitz  # PyMuPDF
from icon import MyIcon

class About:
    def about(self):
        msgBox = QMessageBox()
      #  msgBox.setFixedSize(600, 200)
       # title_font = msgBox.font()
       # title_font.setPointSize(16)
      #  msgBox.setFont(title_font)
        msgBox.setWindowTitle("About")
        MyIcon(msgBox)
        msgBox.setText("""<p><strong>ChemMLP</strong></p>""")
        pixmappath0 = os.path.abspath(os.path.dirname(__file__)) + '/pixfig/'
        pixmap = QPixmap(pixmappath0 + 'icon.png')  # Insert the path to your image
        msgBox.setIconPixmap(pixmap)
        msgBox.setInformativeText("""<p>This software empowers you to predict outcomes based on passive observations using cutting-edge machine learning and deep learning techniques.</p>
        <p>Developed with Python 3.9 and Qt 6, this version of the software is proudly crafted at AtomixAI V.01, situated in beautiful Montreal, Canada.</p>
        <p>For further inquiries or assistance, feel free to reach out to us via email:</p>
        <p>  <p><a href="mailto:sadollah.ebrahimi@usherbrooke.ca"> <em>sadollah.ebrahimi@usherbrooke.ca</em></a><p>  </p>
        <p><em>Thank you for choosing the <strong>AtomixAI</strong></p> We look forward to serving you!</em></p>""")
        msgBox.exec()

    def open_manual(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("PDF files (*.pdf)")
        file_dialog.setWindowTitle("Open Manual")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                pdf_path = selected_files[0]
                self.display_pdf_as_images(pdf_path)

    def display_pdf_as_images(self, pdf_path):
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            pixmap = QPixmap()
            pixmap.loadFromData(doc[page_num].get_pixmap().tobytes())
            self.show_image_in_message_box(pixmap)

    def show_image_in_message_box(self, pixmap):
        msg_box = QMessageBox()
        msg_box.setIconPixmap(pixmap)
        msg_box.setWindowTitle("PDF Viewer")
        msg_box.exec()

if __name__ == '__main__':
    app = QApplication([])
    about = About()
    about.about()
    app.exec()
