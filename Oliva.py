import sys
from PyQt5 import QtWidgets, QtGui
import cv2 as cv
import numpy as np


class Example(QtWidgets.QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        self.dirlist_input = ""
        self.path_file_output = ""

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

        img = cv.imread("C:\\Users\\betterty\\Downloads\\Telegram Desktop\\zzzz.jpg")
        gr = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        bl = cv.medianBlur(gr, 5)
        canny = cv.Canny(bl, 90, 300)
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (10, 10))
        closed = cv.morphologyEx(canny, cv.MORPH_CLOSE, kernel)
        contours = cv.findContours(closed.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[0]

        for cnt in contours:
            rect = cv.minAreaRect(cnt)  # пытаемся вписать прямоугольник
            cv.drawContours(img, contours, -1, (255, 0, 0), 2)  # рисуем прямоугольник
            M = cv.moments(cnt)
            if M["m00"] != 0:
                print(M["m00"])
            cv.putText(img, str(M["m00"]), (np.int0(M["m01"] / M["m00"]), np.int0(M["m10"] / M["m00"])),
                       cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # перебираем все найденные контуры в цикле

        cv.imshow('contours', img)  # вывод обработанного кадра в окно
        cv.waitKey()
        cv.destroyAllWindows()


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    ex.setWindowTitle("Oliva")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
