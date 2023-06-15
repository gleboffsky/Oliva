import datetime
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import cv2 as cv
import numpy as np
import os
from datetime import datetime, date
import csv
from PIL import Image
import threading
from rembg import remove
class Example(QtWidgets.QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        self.dirlist_input = ""
        self.path_file_output = ""
        self.result = ""
        self.file_path_area = f"C:\\Users\\{os.environ.get('USERNAME')}\\Documents\\Oliva_errors.txt"

    def initUI(self):
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.btn = QtWidgets.QPushButton('Выбор папки с фото', self)
        self.gridLayout.addWidget(self.btn, 0, 0, 1, 1)
        self.btn.clicked.connect(self.set_file_input)
        self.btn2 = QtWidgets.QPushButton('Выбор пути для файла csv', self)
        self.btn2.clicked.connect(self.set_file_output)
        self.gridLayout.addWidget(self.btn2, 0, 1, 1, 1)
        self.btn3 = QtWidgets.QPushButton('Старт', self)
        self.btn3.clicked.connect(self.functional)
        self.gridLayout.addWidget(self.btn3, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("label")
        self.label.setText("Коэффициент фото")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setText("1")
        #self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout.addWidget(self.lineEdit)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.setGeometry(300, 300, 500, 250)
        self.setWindowTitle('Input dialog')
        self.show()

    def set_file_input(self):
        self.dirlist_input = QtWidgets.QFileDialog.getExistingDirectory(None, "Выбрать папку", ".")

    def set_file_output(self):
        self.dirlist_output = QtWidgets.QFileDialog.getExistingDirectory(None, "Выбрать папку", ".")

    def threading_functional(self):
        t = threading.Thread(target=self.functional)
        t.daemon = True
        t.start()

    def without_bg(self):
        try:
            if not os.path.isdir(f'{self.dirlist_output}\\images_without_bg'):
                os.mkdir(f'{self.dirlist_output}\\images_without_bg')
            for pict in os.listdir(self.dirlist_input):
                if pict.endswith('.png') or pict.endswith('.jpg') or pict.endswith('.jpeg') or pict.endswith('.PNG') or pict.endswith('.JPG') or pict.endswith('.JPEG'):
                    print(f'[+] Удаляю фон: "{pict}"...')
                    output = remove(Image.open(os.path.join(self.dirlist_input, pict)))
                    output.save(os.path.join(f'{self.dirlist_output}\\images_without_bg', f'{pict.split(".")[0]}.png'))
                else:
                    continue
        except Exception as err:
            with open(self.file_path_area, "a") as file:
                file.write(f"\n{datetime.now()} Ошибка without_bg: {err}")
                file.close()

    def white_bg(self):
        try:
            if not os.path.isdir(f'{self.dirlist_output}\\images_white_bg'):
                os.mkdir(f'{self.dirlist_output}\\images_white_bg')
            for pict in os.listdir(f"{self.dirlist_output}\\images_without_bg"):
                image = Image.open(f"{self.dirlist_output}\\images_without_bg\\{pict}")
                new_image = Image.new("RGBA", image.size, "WHITE")  # Create a white rgba background
                new_image.paste(image, (0, 0),
                                image)  # Paste the image on the background. Go to the links given below for details.
                new_image.convert('RGB').save(f"{self.dirlist_output}\\images_white_bg\\{pict}", "JPEG")  # Save as JPEG
        except Exception as err:
            with open(self.file_path_area, "a") as file:
                file.write(f"\n{datetime.now()} Ошибка white_bg: {err}")
                file.close()
    def functional(self):
        try:
            photos = os.listdir(self.dirlist_input)
            file = open(
                f"{self.dirlist_output}/{datetime.now().date()} {datetime.now().time().hour};{datetime.now().time().minute};{datetime.now().time().second}.csv",
                "w")
            N = True
            for photo in photos:
                data_time = None
                Model = None
                img = cv.imread(f"{self.dirlist_input}\\{photo}")
                height_img, width_img, channels = img.shape
                gr = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                bl = cv.medianBlur(gr, 5)
                canny = cv.Canny(bl, 90, 300)
                kernel = cv.getStructuringElement(cv.MORPH_RECT, (10, 10))
                closed = cv.morphologyEx(canny, cv.MORPH_CLOSE, kernel)
                contours = cv.findContours(closed.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]

                edit = csv.writer(file, delimiter=';',  quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
                if N == True:
                    edit.writerow(["Имя изображения", "Площадь в пикселях",
                                   "Площадь в см2", "Дата и время съемки", "Высота изображения", "Ширина изображения", "Дата и время обработки",  "Максимальная линейная длина объекта в пикселях", "Минимальная линейная длина объекта в пикселях", "Размеры описанного прямоугольника в пикселях", "Максимальная линейная длина объекта в см2", "Минимальная линейная длина объекта в см2", "Размеры описанного прямоугольника в см2", "Модель камеры"])
                    N = False
                max_cnt = max(contours, key=cv.contourArea)
                moments = cv.moments(max_cnt)
                image = Image.open(f"{self.dirlist_input}\\{photo}")
                exit_data = image.getexif()
                x, y, w, h = cv.boundingRect(max_cnt)
                try:
                    data_time = exit_data[306]
                    Model = exit_data[272]
                except Exception as err:
                    with open(self.file_path_area, "a") as filee:
                        filee.write(f"\nНедостаточно параметров; {err}")
                        filee.close()
                edit.writerow([f"{photo}", f"{moments['m00']}", f"{moments['m00']*float(self.lineEdit.text())}", f"{data_time}", f"{height_img}", f"{width_img}", f"{datetime.now()}", f"{h}", f"{w}", f"{h*w}", f"{h*float(self.lineEdit.text())}", f"{w*float(self.lineEdit.text())}", f"{h*w*float(self.lineEdit.text())}", f"{Model}"])

            file.close()
            self.without_bg()
            self.white_bg()
        except Exception as err:
            with open(self.file_path_area, "a") as file:
                file.write(f"\n{datetime.now()} Ошибка: {err}")
                file.close()
        # перебираем все найденные контуры в цикле
def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    ex.setWindowTitle("Oliva")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
