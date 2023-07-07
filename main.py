import cv2
import qrcode

from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui


class MyGui(QMainWindow):
    def __init__(self):
        super(MyGui, self).__init__()
        uic.loadUi("ui/main.ui", self)
        self.show()

        self.current_file = ""
        self.actionLoad_Image.triggered.connect(self.load_image)
        self.actionSave_Image.triggered.connect(self.save_image)
        self.pushButton.clicked.connect(self.read_qrcode)
        self.pushButton_2.clicked.connect(self.generate_qrcode)

    def load_image(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)", options=options)

        if filename != "":
            self.current_file = filename
            pixmap = QtGui.QPixmap(self.current_file)
            pixmap = pixmap.scaled(300, 300)
            self.label.setScaledContents(True)
            self.label.setPixmap(pixmap)

    def save_image(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "PNG (*.png)", options=options)

        if filename != "":
            img = self.label.pixmap()
            img.save(filename)

    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=2)

        qr.add_data(self.textEdit.toPlainText())
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save("curent.png")
        pixmap = QtGui.QPixmap("curent.png")
        pixmap = pixmap.scaled(300, 300)
        self.label.setScaledContents(True)
        self.label.setPixmap(pixmap)



    def read_qrcode(self):
        img = cv2.imread(self.current_file)
        detector = cv2.QRCodeDetector()
        #data, bbox, straight_qrcode
        data, _, _ = detector.detectAndDecode(img)
        self.textEdit.setText(data)

def main():
    app = QApplication([])

    window = MyGui()
    app.exec_()

if __name__ == "__main__":
    main()
