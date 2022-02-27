from paddleocr import PaddleOCR

from interface import Ui_MainWindow
from PIL import Image, ImageGrab
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow
import paddlehub as hub


class run(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    # 读取截图，返回截图
    def imread(self, ui):
        img = ImageGrab.grabclipboard()
        try:
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        except TypeError:
            ui.textEdit.setText("请先截图再点击按钮！")
            return
        else:
            return img

    # 使用PPOCR识别截图，返回识别结果
    def imrec(self, img):
        ocr = hub.Module(name="chinese_ocr_db_crnn_mobile")
        #ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
        #result = ocr.ocr(img, cls=True)
        result = ocr.recognize_text(images=[img])
        res = str()
        for data in result[0]["data"]:
            res += data["text"]
        return result

    # 将识别结果打印到文本框中
    def print_res(self, ui, res):
        ui.textEdit.setText(res)

    def all(self, ui):
        img = self.imread(ui)
        if not isinstance(img, np.ndarray):
            return
        res = self.imrec(img)
        self.print_res(ui, res)