from sklearn.preprocessing import StandardScaler
import pickle

class Scaling:
    def __init__(self):
        pass

    def scale_train_and_test(self, x_train, x_test) :

        x_train_scaled= x_train.copy()
        x_test_scaled= x_test.copy()

        self.scaler=StandardScaler()
        x_train_scaled = self.scaler.fit_transform(x_train_scaled)
        x_test_scaled = self.scaler.transform(x_test_scaled)

        return x_train_scaled, x_test_scaled
    


    def save_scaling(self, saving_path):
        pickle.dump(self.scaler,open(saving_path,'wb'))