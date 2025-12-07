from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from paddleocr import PaddleOCR
import uvicorn
import tempfile

app = FastAPI()

ocr = PaddleOCR(
    lang='ch',
    use_angle_cls=True,
    ocr_version='PP-OCRv5'
)

@app.post("/ocr")
async def ocr_api(file: UploadFile = File(...)):
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(await file.read())
    temp.close()

    result = ocr.ocr(temp.name, cls=True)

    lines = []
    for line in result[0]:
        text = line[1][0]
        score = float(line[1][1])
        lines.append({"text": text, "score": score})

    return JSONResponse({
        "text": "\n".join([l["text"] for l in lines]),
        "lines": lines
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
