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

# Load models :
log_reg_model = pickle.load(open(settings["log_reg_model"], "rb"))
scaler_model = pickle.load(open(settings["scaler_model"], "rb"))





# Instanciate fastAPI :
api = FastAPI()
api.mount("/image", StaticFiles(directory="../frontend/image"), name="image")
api.mount("/css", StaticFiles(directory="../frontend/templates/css"), name="css")
api.mount("/js", StaticFiles(directory="../frontend/templates/js"), name="js")
templates = Jinja2Templates(directory="../frontend/templates")


# get :
@api.get('/')
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@api.get('/new_page')
def new_page(request: Request):
    return templates.TemplateResponse("new_page.html", {"request": request})



# post : 
# Le système recup l'info entrée par l'utilisateur et fait un retour :
@api.post("/predict")
def prediction(
    request: Request,
    Pregnancies: float = Form(...),
    Glucose: float = Form(...),
    BloodPressure: float = Form(...),
    SkinThickness: float = Form(...),
    Insulin: float = Form(...),
    BMI: float = Form(...),
    DiabetesPedigreeFunction: float = Form(...),
    Age: float = Form(...),
):

    # 1/ Transform dict to dataframe
    data = [
        Pregnancies,
        Glucose,
        BloodPressure,
        SkinThickness,
        Insulin,
        BMI,
        DiabetesPedigreeFunction,
        Age,
    ]
    data = np.array(data).reshape(1, -1)

    # 2/ Scale dataframe
    data = scaler_model.transform(data)

    # 3/ Pred dataframe
    pred = log_reg_model.predict(data)[0]
    pred_proba = log_reg_model.predict_proba(data)[0][1]

    return templates.TemplateResponse(
        "home.html", {"request": request, "prediction_text": f"Pred {pred:.2f}", "predict_proba": f"Pred proba {pred_proba:.2f}"}
    )






if __name__ == "__main__":
    # Run API :
    uvicorn.run(api)