import pandas as pd
import numpy as np
import yaml
from sklearn.model_selection import train_test_split
import pickle
from sklearn.metrics import f1_score

from src.data_visualization.EDA import EDA
from src.data_treatment.data_scaling import Scaling
from src.model.model_building import Model_building


def main(random_state):

    # Open raw data :
    df = pd.read_csv(settings["data"]["raw_data_path"], encoding="utf-8")

    # EDA :
    Exp_data_analysis = EDA(df=df, target=settings["features_info"]["target"])
    Exp_data_analysis.correlation_matrix(
        file_saving=settings["reports"]["EDA"]["corr_matrix"]
    )

    # 1/ Train test split :
    x = df.drop(columns=settings["features_info"]["target"])
    y = df[settings["features_info"]["target"]]

    X_train, X_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, random_state=random_state
    )

    # 2/ Standardize the dataset :
    # scaling :
    scaler = Scaling()
    X_train_scaled, X_test_scaled = scaler.scale_train_and_test(X_train, X_test)

    # Save scaler :
    scaler.save_scaling(saving_path=settings["scaler_model"])

    # 3/ Model training :
    # training :
    model_building = Model_building(random_state=random_state)
    model = model_building.training(X_train_scaled, y_train)

    # eval pred :
    pred = model.predict(X_test_scaled)
    print(f"F1-score on test set : {f1_score(y_test, pred)}")

    # 4/ Save model :
    pickle.dump(model, open(settings["log_reg_model"], "wb"))


if __name__ == "__main__":
    # Load project setting from setting.yaml :
    with open("config/settings.yaml", "r") as settings_file:
        settings = yaml.safe_load(settings_file)

    main(random_state=settings["random_state"])
