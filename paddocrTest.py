#import os
#os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
from paddleocr import PaddleOCR, draw_ocr

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
img_path = '1.jpg'
result = ocr.ocr(img_path, cls=True)
for line in result:
    coordinate = line[0] #[[416.0, 140.0], [780.0, 146.0], [780.0, 189.0], [416.0, 183.0]]
    tupword = line[1]  # ('产布局、数字化水平、生产能力、综合保障、支撑配套 等方', 0.9555808)
    print(coordinate)
    print(tupword)



# 显示结果
from PIL import Image

image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]
im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
im_show = Image.fromarray(im_show)
im_show.save('result.jpg')



