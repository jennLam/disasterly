import pandas as pd
import numpy as np
import operator as op


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

    def search_criteria(self, column_name, target, operator):
        """Specify search condition for dataframe."""

        if column_name not in list(self.df):
            return

        result = None

        if target:
            result = operator(self.df[column_name], target)
        else:
            result = self.df[column_name] is not None

        return result

    def advanced_search(self, incident_type=None, start_date=None, end_date=None):
        """Advanced search of disaster data."""

        condition = self.df

        if incident_type or start_date or end_date:

            i = self.search_criteria("incidentType", incident_type, op.eq)
            sd = self.search_criteria("incidentBeginDate", start_date, op.ge)
            ed = self.search_criteria("incidentEndDate", end_date, op.le)

            condition = self.df[i & sd & ed]

        return condition

    def create_disaster_dict(self, dataframe):
        """Create a dictionary with flood, state, county infomration."""

        disaster_dict = {}

        for i, row in dataframe.iterrows():

            disaster_dict[i] = {"incidentType": row["incidentType"],
                                "state": row["state"],
                                "declaredCounty": row["declaredCountyArea"]}

        return disaster_dict


    def create_disaster_dict2(self, dataframe):
        """Create a dictionary with flood, state, county infomration."""

        disaster_dict = {}

        for i, row in dataframe.iterrows():

            disaster_dict[row["state"]] = disaster_dict.get(row["state"], 0) + 1

        return disaster_dict

    def create_disaster_dict3(self, dataframe, column_name):
        """Create a dictionary with flood, state, county infomration."""

        disaster_dict = {}

        for i, row in dataframe.iterrows():

            disaster_dict[row[column_name]] = disaster_dict.get(row[column_name], 0) + 1

        return disaster_dict
