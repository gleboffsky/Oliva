import datetime
import sys
from PyQt5 import QtWidgets, QtGui
import cv2 as cv
import numpy as np
import os
from datetime import datetime, date


class Example(QtWidgets.QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        self.dirlist_input = ""
        self.path_file_output = ""
        self.result = ""

    def initUI(self):
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.btn = QtWidgets.QPushButton('Выбор папки с фото', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.path_file_input)
        self.btn2 = QtWidgets.QPushButton('Выбор пути для файла', self)
        self.btn2.move(20, 60)
        self.btn2.clicked.connect(self.path_file_output)
        self.btn3 = QtWidgets.QPushButton('Старт', self)
        self.btn3.move(100, 100)
        self.btn3.clicked.connect(self.functional)
        self.gridLayout.addWidget(self.btn, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.btn2, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.btn3, 1, 1, 1, 1)
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        self.show()

    def path_file_input(self):
        self.dirlist_input = QtWidgets.QFileDialog.getExistingDirectory(None, "Выбрать папку", ".")

    def path_file_output(self):
        self.dirlist_output = QtWidgets.QFileDialog.getExistingDirectory(None, "Выбрать папку", ".")

    def functional(self):
        try:
            photos = os.listdir(self.dirlist_input)
            for photo in photos:
                img = cv.imread(f"{self.dirlist_input}\\{photo}")
                gr = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                bl = cv.medianBlur(gr, 5)
                canny = cv.Canny(bl, 90, 300)
                kernel = cv.getStructuringElement(cv.MORPH_RECT, (10, 10))
                closed = cv.morphologyEx(canny, cv.MORPH_CLOSE, kernel)
                contours = cv.findContours(closed.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]
                file = open(f"{self.dirlist_output}/{datetime.now().date()} {datetime.now().time().hour};{datetime.now().time().minute};{datetime.now().time().second}.csv", "w")
                for cnt in contours:
                    cv.drawContours(img, contours, -1, (255, 0, 0), 2)  # рисуем прямоугольник
                    M = cv.moments(cnt)
                    if M["m00"] != 0:
                        h, w, c = img.shape
                        file.write(f"Имя фото:{photo}  Высота:{h}  Ширина:{w}  Дата и время обработки:{datetime.now()}  Площадь в пикселях: {M['m00']}  Площадь в см2: ")

                file.close()
                #cv.putText(img, str(M["m00"]), (np.int0(M["m01"] / M["m00"]), np.int0(M["m10"] / M["m00"])), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                #cv.imshow('contours', img)  # вывод обработанного кадра в окно
                #cv.waitKey()
                #cv.destroyAllWindows()

        except Exception as err:
            print(err)

        # перебираем все найденные контуры в цикле

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    ex.setWindowTitle("Oliva")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
