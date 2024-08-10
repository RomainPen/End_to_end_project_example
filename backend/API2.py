from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import numpy as np
import pandas as pd
import pickle
import yaml



# Load project setting from setting.yaml :
with open("config/settings.yaml", "r") as settings_file:
    settings = yaml.safe_load(settings_file)

# Instanciate fastAPI :
app = FastAPI()
app.mount("/image", StaticFiles(directory="../frontend/image"), name="images")
app.mount("/css", StaticFiles(directory="../frontend/templates/css"), name="css")
app.mount("/js", StaticFiles(directory="../frontend/templates/js"), name="js")
templates = Jinja2Templates(directory="../frontend/templates")


@app.get('/')
def read_root(request: Request):
    return templates.TemplateResponse("home2.html", {"request": request})

@app.get('/new_page')
def new_page(request: Request):
    return templates.TemplateResponse("new_page.html", {"request": request})


@app.post('/print_sum')
def print_name(request: Request, first_nb= Form(...), second_nb= Form(...)):
    total_sum = int(first_nb) + int(second_nb)
    return templates.TemplateResponse(
        "home2.html", {"request": request, "print_sum": f"sum = {total_sum}"}
    )

@app.post('/print_name')
def print_name(request: Request, name=Form(...)):
    return templates.TemplateResponse(
        "home2.html", {"request": request, "print_name": f"you are {name}"}
    )




if __name__ == "__main__":
    # Run API :
    uvicorn.run(app)