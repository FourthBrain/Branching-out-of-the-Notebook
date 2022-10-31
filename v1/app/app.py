# import fastapi
from fastapi import FastAPI, UploadFile, File
from starlette.responses import StreamingResponse
from diffusers import (
    StableDiffusionPipeline,
    StableDiffusionImg2ImgPipeline
)
from PIL import Image
import numpy as np
from torch import autocast
import uvicorn
import cv2
import io
import torch

# instantiate the app
app = FastAPI()

# cuda or cpu config
def get_device():
    if torch.cuda.is_available():
        print('cuda is available')
        return torch.device('cuda')
    else:
        print('cuda is not available')
        return torch.device('cpu')

# create a route
@app.get("/")
def index():
    return {"text" : "We're running!"}

# create a text2img route
@app.post("/text2img")
def text2img(text: str):
    device = get_device()

    text2img_pipe = StableDiffusionPipeline.from_pretrained("../model")
    text2img_pipe.to(device)

    img = text2img_pipe(text).images[0]

    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    res, img = cv2.imencode(".png", img)

    del text2img_pipe
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return StreamingResponse(io.BytesIO(img.tobytes()), media_type="image/png")

# run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)