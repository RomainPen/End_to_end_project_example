from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import numpy as np
import pandas as pd
import pickle
import yaml


# Load project setting from setting.yaml :
with open("config/settings.yaml", "r") as settings_file:
    settings = yaml.safe_load(settings_file)


# Instanciate application :
api = FastAPI()
templates = Jinja2Templates(directory="../frontend/templates")


# Load models :
log_reg_model = pickle.load(open(settings["log_reg_model"], "rb"))
scaler_model = pickle.load(open(settings["scaler_model"], "rb"))


# l'utilisateur recoit une info de la part du système (Page d'acceuil) :
@api.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


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

    return templates.TemplateResponse(
        "home.html", {"request": request, "prediction_text": f"Pred {pred:.2f}"}
    )


if __name__ == "__main__":
    # Run API :
    uvicorn.run(api)
