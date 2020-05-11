# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from test_mtcnn_wider import face_detect
import cv2
import numpy as np
from test_vgg_ck import emotion


class picture(QWidget):
    def __init__(self):
        super(picture, self).__init__()

        self.data_path = ''
        self.rectangles = None

        self.resize(300, 400)
        self.setWindowTitle("label显示图片")
        self.input = QLabel(self)
        self.input.move(50, 90)
        self.input.setFixedSize(200, 300)

        btn = QPushButton(self)
        btn.setText("打开图片")
        btn.move(50, 30)
        btn.clicked.connect(self.openimage)

        det = QPushButton(self)
        det.setText("检测")
        det.move(170, 30)
        det.clicked.connect(self.detect)

    def openimage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(imgName).scaled(self.input.width(), self.input.height())
        print(type(jpg))
        self.input.setPixmap(jpg)
        self.data_path = imgName

    def detect(self):
        self.rectangles, points = face_detect(image_path=self.data_path)
        img = cv2.imread(self.data_path)
        for rectangle in self.rectangles:
            print(rectangle)
            x1, y1, width, height, face_score = rectangle
            x1, y1, x2, y2 = x1, y1, x1 + width, y1 + height

            cv2.putText(img, str(rectangle[4]), (int(rectangle[0]), int(rectangle[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0))
            cv2.rectangle(img, (int(rectangle[0]), int(rectangle[1])), (int(rectangle[2]), int(rectangle[3])),
                          (255, 0, 0), 1)

            category, emotion_score = emotion(img[int(y1):int(y2), int(x1):int(x2)])
            print(category, emotion_score)
            cv2.putText(img, category, (int(x1), int(y1) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1,
                        cv2.LINE_AA)

        cv2.imshow('image', img)
        cv2.waitKey(0)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my = picture()
    my.move(300, 300)
    my.show()
    sys.exit(app.exec_())
