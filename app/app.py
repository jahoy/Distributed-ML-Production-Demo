import sys
import json
import os
import logging
from celery import Celery
from celery.signals import after_task_publish
import uvicorn
from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from app import celery_tasks
from pydantic import BaseModel
from typing import Optional

templates = Jinja2Templates(directory="templates")

class Flower(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

    @classmethod
    def as_form(cls, sepal_length: float = Form(...), sepal_width: float = Form(...), petal_length: float = Form(...), petal_width: float = Form(...)) -> Flower:
        return cls(sepal_length=sepal_length, sepal_width=sepal_width, petal_length=petal_length, petal_width=petal_width)

app = FastAPI()

@app.get('/')
async def index():
    """ 
    index page
    """
    return templates.TemplateResponse("index.html")


@app.post('/predict')
async def predict(data: Flower = Depends(Flower.as_form)):
    """ 
    celery를 통한 예측을 진행한다.
    """
    data = data.dict()
    task = await celery_tasks.get_prediction_result_pdf.delay(data)
    return templates.TemplateResponse("home.html", {"TASKID": task.id})


@app.get('/download/')
async def result(taskid: Optional[str] = None):
    """ 
    PDF결과를 다운로드한다.
    """
    if taskid:
        task = await celery_tasks.get_task(taskid)
        pdf_output = await task.get()
        return FileResponse(pdf_output)
    raise HTTPException(status_code=404, detail="Item not found")


@app.get('/progress/')
async def progress(taskid: Optional[str] = None):
    """ 
    task_id의 진행상태를 check한다
    """
    return_result = '{}'
    if taskid:
        task = await celery_tasks.get_task(taskid)
        if task.state == 'PROGRESS':
            return_result = json.dumps(dict(
                state=task.state,
                progress=task.result['current'],
            ))
        elif task.state == 'SUCCESS':
            return_result = json.dumps(dict(
                state=task.state,
                progress=1.0,
            ))
        elif task.state == 'FAILURE':
            return_result = json.dumps(dict(
                state=task.state,
                progress=1.0,
            ))
    return return_result


if __name__ == '__main__':
    uvicorn.run(app)
