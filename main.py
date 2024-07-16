import pandas as pd
import numpy as np
import yaml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle 
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score




def main(random_state) :

    # Open raw data :
    df = pd.read_csv(settings["data"]["raw_data_path"], encoding="utf-8")     

    # 1/ Train test split :
    x = df.drop(columns=settings["features_info"]["target"])
    y = df[settings["features_info"]["target"]]

    X_train, X_test, y_train, y_test = train_test_split(x,y,test_size=0.3,random_state=random_state)


    # 2/ Standardize the dataset :
    # scaling : 
    scaler=StandardScaler()
    X_train=scaler.fit_transform(X_train)
    X_test=scaler.transform(X_test)
    
    # Save scaler : 
    pickle.dump(scaler,open(settings["scaler_model"],'wb'))


    # 3/ Model training :
    # training :
    log_reg=LogisticRegression(random_state=random_state)
    log_reg.fit(X_train,y_train)

    # eval pred :
    pred = log_reg.predict(X_test)
    print(f"F1-score on test set : {f1_score(y_test, pred)}")


    # 4/ Save model :
    pickle.dump(log_reg,open(settings["log_reg_model"],'wb'))







if __name__ == "__main__":
    # Load project setting from setting.yaml :
    with open("config/settings.yaml", "r") as settings_file:
        settings = yaml.safe_load(settings_file)

    main(random_state=settings["random_state"])