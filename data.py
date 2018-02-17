import pandas as pd


class DisasterData():

    def __init__(self, file_name="DisasterDeclarationsSummaries.csv"):

        self.file_name = file_name
        self.df = pd.read_csv(file_name)


