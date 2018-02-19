import pandas as pd
import numpy as np


class DisasterData():

    def __init__(self, file_name="DisasterDeclarationsSummaries.csv"):

        self.file_name = file_name
        self.df = pd.read_csv(file_name)

        self.df["incidentBeginDate"] = pd.to_datetime(self.df["incidentBeginDate"], format="%Y/%m/%d")
        self.df["incidentEndDate"] = pd.to_datetime(self.df["incidentEndDate"], format="%Y/%m/%d")

    def get_categories(self, column_name):
        """Create a list of unique categories from dataframe."""

        items = self.df[column_name].unique()
        items = np.array(items).tolist()

        return items
