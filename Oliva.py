import datetime
import sys
from PyQt5 import QtWidgets
import numpy as np
import os
from datetime import datetime
import csv
import threading
from rembg import remove
from PIL import Image, ImageFilter, ImageDraw
from math import sqrt

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
        self.label.setText("Коэффициент фото(пикселей в 1см)")
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

    def without_bg(self, date, hour, minute, second):
        try:
            if not os.path.isdir(f'{self.dirlist_output}\\images_without_bg'):
                os.mkdir(f'{self.dirlist_output}\\images_without_bg')

            os.mkdir(f'{self.dirlist_output}\\images_without_bg\\{date} {hour};{minute};{second}')
            for pict in os.listdir(f'{self.dirlist_input}'):
                if pict.endswith('.png') or pict.endswith('.jpg') or pict.endswith('.jpeg') or pict.endswith('.PNG') or pict.endswith('.JPG') or pict.endswith('.JPEG'):
                    output = remove(Image.open(os.path.join(f'{self.dirlist_input}', pict)))
                    output.save(os.path.join(f'{self.dirlist_output}\\images_without_bg\\{date} {hour};{minute};{second}', f'{pict}.png'))
                else:
                    continue
        except Exception as err:
            with open(self.file_path_area, "a") as file:
                file.write(f"\n{date, hour, minute, second} Ошибка without_bg: {err}")
                file.close()

    def white_bg(self,date, hour, minute, second):
        try:
            if not os.path.isdir(f'{self.dirlist_output}\\images_white_bg'):
                os.mkdir(f'{self.dirlist_output}\\images_white_bg')
            os.mkdir(f'{self.dirlist_output}\\images_white_bg\\{date} {hour};{minute};{second}')
            for pict in os.listdir(f"{self.dirlist_output}\\images_without_bg\\{date} {hour};{minute};{second}"):
                image = Image.open(f"{self.dirlist_output}\\images_without_bg\\{date} {hour};{minute};{second}\\{pict}")
                new_image = Image.new("RGBA", image.size, "WHITE")  # Create a white rgba background
                new_image.paste(image, (0, 0),
                                image)  # Paste the image on the background. Go to the links given below for details.
                new_image.convert('RGB').save(f"{self.dirlist_output}\\images_white_bg\\{date} {hour};{minute};{second}\\{pict}", "png")  # Save as JPEG
                image.close()
        except Exception as err:
            with open(self.file_path_area, "a") as file:
                file.write(f"\n{datetime.now()} Ошибка white_bg: {err}")
                file.close()

    def mesh_creator(self, date, hour, minute, second):
        try:
            if not os.path.isdir(f'{self.dirlist_output}\\mesh_creator'):
                os.mkdir(f'{self.dirlist_output}\\mesh_creator')
            os.mkdir(f'{self.dirlist_output}\\mesh_creator\\{date} {hour};{minute};{second}')
            for pict in os.listdir(f"{self.dirlist_output}\\images_without_bg\\{date} {hour};{minute};{second}"):
                img = Image.open(f"{self.dirlist_output}\\images_without_bg\\{date} {hour};{minute};{second}\\{pict}")
                img_size = img.size
                font = Image.new('RGBA', img_size, (255, 255, 255, 255))
                draw = ImageDraw.Draw(font)
                width = int((img_size[0] + img_size[1]) * 0.005)
                # сетка вертикаль
                for i in range(0, img_size[0], int(5 * float(self.lineEdit.text()))):
                    draw.line((i, 0, i, img_size[1]), fill='blue', width=width)
                # сетка горизонталь
                for i in range(0, img_size[1], int(10 * float(self.lineEdit.text()))):
                    draw.line((0, i, img_size[0], i), fill='green', width=width)
                # сетка вертикаль
                for i in range(0, img_size[0], int(50 * float(self.lineEdit.text()))):
                    draw.line((i, 0, i, img_size[1]), fill='red', width=width)
                # сетка горизонталь
                for i in range(0, img_size[1], int(50 * float(self.lineEdit.text()))):
                    draw.line((0, i, img_size[0], i), fill='red', width=width)

                Image.alpha_composite(font, img).save(f"{self.dirlist_output}\\mesh_creator\\{date} {hour};{minute};{second}\\{pict}", "png")
                font.close()
                img.close()
        except Exception as err:
            with open(self.file_path_area, "a") as file:
                file.write(f"\n{datetime.now()} Ошибка mesh_creator: {err}")
                file.close()

    def crop_image(self, left, top, right, bottom, date, hour, minute, second, img, photo):
        try:
            if not os.path.isdir(f'{self.dirlist_output}\\images_crop'):
                os.mkdir(f'{self.dirlist_output}\\images_crop')
            if not os.path.isdir(f'{self.dirlist_output}\\images_crop\\{date} {hour};{minute};{second}'):
                os.mkdir(f'{self.dirlist_output}\\images_crop\\{date} {hour};{minute};{second}')
            im1 = img.crop((left, top, right, bottom))
            im1.save(f"{self.dirlist_output}\\images_crop\\{date} {hour};{minute};{second}\\{photo}", "png")

        except Exception as err:
            with open(self.file_path_area, "a") as file:
                file.write(f"\n{datetime.now()} Ошибка crop_image: {err}")
                file.close()

    def without_bg_crop(self, date, hour, minute, second):
        try:

            for pict in os.listdir(f'{self.dirlist_output}\\images_crop\\{date} {hour};{minute};{second}'):
                output = remove(Image.open(os.path.join(f'{self.dirlist_output}\\images_crop\\{date} {hour};{minute};{second}', pict)))
                output.save(os.path.join(f'{self.dirlist_output}\\images_without_bg\\{date} {hour};{minute};{second}', f'{pict}.png'))
        except Exception as err:
            with open(self.file_path_area, "a") as file:
                file.write(f"\n{date, hour, minute, second} Ошибка without_bg: {err}")
                file.close()

    def functional(self):
        try:
            photos = os.listdir(self.dirlist_input)
            timedate = datetime.now()
            date = timedate.now().date()
            hour = timedate.now().time().hour
            minute = timedate.now().time().minute
            second = timedate.now().time().second
            self.without_bg(date, hour, minute, second)
            file = open(
                f"{self.dirlist_output}/{date} {hour};{minute};{second}.csv",
                "w")
            N = True
            for photo in photos:
                data_time = None
                Model = None
                img = Image.open(f"{self.dirlist_output}\\images_without_bg\\{date} {hour};{minute};{second}\\{photo}.png")

                foto_array = np.asarray(img)
                pix_sqare = 0
                pr_ug = [-1, -1, -1, -1]  # 0-верх, 1-левая, 2-правая, 3-низ
                min_x = 0
                min_y = 0
                i_n = 0
                # подсчёт площади без фона
                # взяли строки изображения
                for i in foto_array:
                    # взяли в строках сами пиксели
                    i_n += 1
                    k_n = 0
                    for k in i:
                        if k[3] >= 100:  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            pix_sqare += 1
                            if pr_ug[0] < i_n and min_x == 0:
                                pr_ug[0] = i_n
                                min_x = 1
                            if pr_ug[1] < k_n and min_y == 0:
                                pr_ug[1] = k_n
                                min_y = 1
                            if pr_ug[2] <= k_n:
                                pr_ug[2] = k_n
                            if pr_ug[3] <= i_n:
                                pr_ug[3] = i_n
                            if pr_ug[1] > k_n and min_y == 1:
                                pr_ug[1] = k_n

                        k_n += 1
                width = sqrt((pr_ug[0] - pr_ug[0]) ** 2 + (pr_ug[2] - pr_ug[1]) ** 2)
                height = sqrt((pr_ug[0] - pr_ug[3]) ** 2 + (pr_ug[1] - pr_ug[1]) ** 2)
                edit = csv.writer(file, delimiter=';',  quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
                if N == True:
                    edit.writerow(["Имя изображения", "Площадь в пикселях",
                                   "Площадь в см2", "Дата и время съемки", "Ширина изображения", "Высота изображения", "Дата и время обработки",  "Максимальная линейная длина объекта в пикселях", "Минимальная линейная длина объекта в пикселях", "Размеры описанного прямоугольника в пикселях", "Максимальная линейная длина объекта в см", "Минимальная линейная длина объекта в см", "Размеры описанного прямоугольника в см2", "Модель камеры"])
                    N = False
                image = Image.open(f"{self.dirlist_input}\\{photo}")
                exit_data = image.getexif()
                try:
                    data_time = exit_data[306]
                    Model = exit_data[272]

                except Exception as err:
                    with open(self.file_path_area, "a") as filee:
                        filee.write(f"\nНедостаточно параметров; {err}")
                        filee.close()
                edit.writerow([f"{photo}", f"{pix_sqare}", f"{pix_sqare/float(self.lineEdit.text())/float(self.lineEdit.text())}", f"{data_time}", f"{img.size[0]}", f"{img.size[1]}", f"{datetime.now()}", f"{height}", f"{width}", f"{height*width}", f"{height/float(self.lineEdit.text())}", f"{width/float(self.lineEdit.text())}", f"{height*width/float(self.lineEdit.text())/float(self.lineEdit.text())}", f"{Model}"])
                self.crop_image(pr_ug[1]-(height*0.1), pr_ug[0]-(height*0.1), pr_ug[2]+(height*0.1), pr_ug[3]+(height*0.1), date, hour, minute, second, img, photo)
            file.close()
            self.without_bg_crop(date, hour, minute, second)
            self.white_bg(date, hour, minute, second)
            self.mesh_creator(date, hour, minute, second)
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
