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
        self.btn.clicked.connect(self.path_file_input)
        self.btn2 = QtWidgets.QPushButton('Выбор пути для файла csv', self)
        self.btn2.clicked.connect(self.path_file_output)
        self.gridLayout.addWidget(self.btn2, 0, 1, 1, 1)
        self.btn3 = QtWidgets.QPushButton('Старт', self)
        self.btn3.clicked.connect(self.threading_functional)
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
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        self.show()

    def path_file_input(self):
        self.dirlist_input = QtWidgets.QFileDialog.getExistingDirectory(None, "Выбрать папку", ".")

    def path_file_output(self):
        self.dirlist_output = QtWidgets.QFileDialog.getExistingDirectory(None, "Выбрать папку", ".")

    def threading_functional(self):
        t = threading.Thread(target=self.functional)
        t.daemon = True
        t.start()

    def functional(self):
        try:
            photos = os.listdir(self.dirlist_input)
            for photo in photos:
                data_time = None
                Model = None
                N = 0
                img = cv.imread(f"{self.dirlist_input}\\{photo}")
                gr = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                bl = cv.medianBlur(gr, 5)
                canny = cv.Canny(bl, 90, 300)
                kernel = cv.getStructuringElement(cv.MORPH_RECT, (10, 10))
                closed = cv.morphologyEx(canny, cv.MORPH_CLOSE, kernel)
                contours = cv.findContours(closed.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]
                file = open(f"{self.dirlist_output}/{datetime.now().date()} {datetime.now().time().hour};{datetime.now().time().minute};{datetime.now().time().second}.csv", "w")
                edit = csv.writer(file, delimiter=' ',
                                  quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
                edit.writerow(["Дата и время съемки", "Имя изображения", "Высота изображения", "Ширина изображения", "Дата и время обработки", "Площадь в пикселях",
                               "Площадь в см2", "Максимальная линейная длина объекта в пикселях", "Минимальная линейная длина объекта в пикселях", "Размеры описанного прямоугольника в пикселях", "Максимальная линейная длина объекта в см2", "Минимальная линейная длина объекта в см2", "Размеры описанного прямоугольника в см2", "Модель камеры"])

                for cnt in contours:
                    cv.drawContours(img, contours, -1, (255, 0, 0), 2)  # рисуем прямоугольник
                    M = cv.moments(cnt)
                    if M["m00"] != 0:

                        #file.write(f"Имя фото:{photo}  Высота:{h}  Ширина:{w}  Дата и время обработки:{datetime.now()}  Площадь в пикселях: {M['m00']}  Площадь в см2: ")
                        image = Image.open(f"{self.dirlist_input}\\{photo}")
                        exit_data = image.getexif()
                        x, y, w, h = cv.boundingRect(cnt)
                        img = cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        try:
                            data_time = exit_data[306]
                            Model = exit_data[272]
                        except Exception as err:
                            with open(self.file_path_area, "a") as filee:
                                filee.write(f"\nНедостаточно параметров; {err}")
                                filee.close()
                        edit.writerow([f"{data_time}", f"{photo}", f"{h}", f"{w}", f"{datetime.now()}", f"{M['m00']}", f"{M['m00']*float(self.lineEdit.text())}", f"{h}", f"{w}", f"{h*w}", f"{h*float(self.lineEdit.text())}", f"{w*float(self.lineEdit.text())}", f"{h*w*float(self.lineEdit.text())}", f"{Model}"])
                        N+=1
                cv.imshow('contours', img)  # вывод обработанного кадра в окно
                cv.waitKey(0)
                cv.destroyAllWindows()
                file.close()
                print(f"!!!!!{N}!!!!!!")
        except Exception as err:
            with open(self.file_path_area, "a") as file:
                file.write(f"\nОшибка: {err}")
                file.close()
        # перебираем все найденные контуры в цикле
def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    ex.setWindowTitle("Oliva")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
