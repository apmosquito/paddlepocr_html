#this is function help for ocr to html

#get &nbsp number
def get_NBSP_number(x1, x2, wordheight):
    nbsp = (x1-x2) / wordheight
    return int(nbsp * 1.4)

def get_BNSP_html(number):
    htmlbnsp = ''
    for i in range(0, number):
        htmlbnsp += '&nbsp;'
    return htmlbnsp

def get_HTML_code(result):
    oldmidline :float = 0.0
    xo2, xo3 = 0.0, 0.0
    htmlresult = '<div style="'+'text-align:left;'+'">'
    for line in result:
        print(line)
        coordinate = line[0]  # [[416.0, 140.0], [780.0, 146.0], [780.0, 189.0], [416.0, 183.0]]
        tupwords = line[1]  # ('产布局、数字化水平、生产能力、综合保障、支撑配套 等方', 0.9555808)
        x1 ,y1 = float(coordinate[0][0]), coordinate[0][1]
        x2, y2 = coordinate[1][0], coordinate[1][1]
        x3, y3 = coordinate[2][0], coordinate[2][1]
        x4, y4 = coordinate[3][0], coordinate[3][1]
        tupwordeachline = tupwords[0]
        wordheight = (y4 - y1 + y3 - y2) / 2
        midline: float = (y1 + y2 + y3 + y4) / 4
        htmlbnsp = ''
        # 开始的这块识别 位置在上一块文本前面的，是新的一行,这是另起一行
        # or
        # 行间距大于上字高 则是新行
        print('差值', midline - oldmidline)
        print('字高', wordheight)
        #判断X坐标的起始位置时注意 是有重叠情况发生的，所以先判断这个
        if xo2 == 0.0 or float(midline - oldmidline) > wordheight:
            htmlresult += '</div>'
            bnspNo = get_NBSP_number(x1, 0, wordheight)
            htmlresult += '<div style="'+'text-align:left;'+'">' + get_BNSP_html(bnspNo) + tupwordeachline
        # 不是新的一行 就继续在后面加文字
        else:
            bnspNo = get_NBSP_number(x1, xo2, wordheight)
            htmlresult += get_BNSP_html(bnspNo) + tupwordeachline
        oldmidline = midline
        xo2, xo3 = float(x2), float(x3)
        print(htmlresult)
    return htmlresult
