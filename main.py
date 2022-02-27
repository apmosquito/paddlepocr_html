# coding=gbk
from typing import Optional
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import time, os
from typing import List
from paddleocr import PaddleOCR, draw_ocr

from paddleocrfunction import get_HTML_code

app = FastAPI()

# 前端页面url
origins = [
    "http://localhost",
    "http://localhost:63342",
    "http://localhost:63342/pythonProject1/imagepost.html",
]

# 后台api允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/sacocr/")
def sacocr():
    return {"Hello": "World"}

@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}

@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
#file option
    filename = str(time.time()) + "_" + file.filename
    path = 'c:/local_image/'
    localUrl = path + filename
    if not os.path.exists(path):
        os.mkdir(path)
    try:
        res = await file.read()
        with open(localUrl, "wb") as f:
            print(f)
            f.write(res)
            f.close()
    except Exception as e:
        return {"message": "您的文件格式不是图片，不能解析！"}
    finally:
        f.close()
#start paddleOcr
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
    result = ocr.ocr(localUrl, cls=True)
    return get_HTML_code(result)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
#nssm.exe install "FastAPIWindowsService" "C:\ProgramData\Anaconda3\envs\paddleocr\python.exe" "C:\Users\Administrator\PycharmProjects\pythonProject1\main.py"
#    C:\ProgramData\Anaconda3\envs\paddleocr\python.exe C:\Users\Administrator\PycharmProjects\pythonProject1\main.py
