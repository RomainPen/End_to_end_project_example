import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.api.types import is_numeric_dtype, is_object_dtype


class EDA:
    def __init__(self, df: pd.DataFrame, target: str):
        """
        Initialize an Exploratory Data Analysis (EDA) object.

        Args:
            df (pd.DataFrame): The input DataFrame for EDA.
            target (str): The name of the target variable.
        """
        self.df = df
        self.target = target
        # Sélection des colonnes numériques à l'exclusion de la variable cible
        self.var_num = df.select_dtypes(include=np.number).columns.tolist()
        self.var_num.remove(target)

        # Sélection des colonnes catégorielles à l'exclusion de la variable CURR_HANDSET_MODE
        self.var_cat = df.select_dtypes(include=object).columns.tolist()

    def correlation_matrix(self, file_saving):
        """
        Create and save a correlation matrix heatmap for selected numerical variables and the target variable.

        Args:
            file_saving: The file path for saving the heatmap.

        Returns:
            None
        """
        # Matrice de corrélation
        correlation_matrix = self.df[
            [elem for elem in self.df.columns if is_numeric_dtype(self.df[elem])]
        ].corr()

        # Sélection des variables les plus corrélées à AFTERGRACE_FLAG avec une corrélation supérieure à 0.15
        threshold = 0.05
        target_correlations = correlation_matrix[self.target][
            (correlation_matrix[self.target] > threshold)
            | (correlation_matrix[self.target] < -threshold)
        ]

        # Filtrage du DataFrame original pour les variables sélectionnées
        filtered_df = self.df[target_correlations.index]

        # Création d'une nouvelle matrice de corrélation avec les variables sélectionnées
        filtered_correlation_matrix = filtered_df.corr()

        # Création de la heatmap de la matrice de corrélation filtrée
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            filtered_correlation_matrix,
            annot=True,
            cmap="coolwarm",
            center=0,
            fmt=".2f",
            annot_kws={"ha": "center"},
        )
        plt.title(
            f"Matrice de corrélation avec variables corrélées à {self.target} (corrélation > 0.15)"
        )
        plt.savefig(file_saving, format="png")
        plt.close()
