import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression


class Model_building:
    def __init__(self, random_state):
        self.random_state = random_state

    def training(self, x, y):
        self.log_reg = LogisticRegression(random_state=self.random_state)
        self.log_reg.fit(x, y)
        return self.log_reg
