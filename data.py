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

    def advanced_search(self, state=None, incident_type=None, start_date=None, end_date=None):
        """Advanced search of disaster data."""

        condition = self.df

        if state or incident_type or start_date or end_date:

            s = self.search_criteria("state", state, op.eq)
            i = self.search_criteria("incidentType", incident_type, op.eq)
            sd = self.search_criteria("incidentBeginDate", start_date, op.ge)
            ed = self.search_criteria("incidentBeginDate", end_date, op.le)

            condition = self.df[s & i & sd & ed]

        return condition

    def make_dict(self, dataframe):

        disaster_dict = {"state": {},
                         "state_county": {},
                         "incident": {},
                         "date": {}}

        start_date = dataframe["incidentBeginDate"].head(1).iloc[0]
        end_date = dataframe["incidentBeginDate"].tail(1).iloc[0]

        for i, row in dataframe.iterrows():

            state = row["state"]
            county = row["declaredCountyArea"]
            incident = row["incidentType"]
            date = row["incidentBeginDate"]

            #state
            disaster_dict["state"][state] = disaster_dict["state"].get(state, 0) + 1

            #state and county
            if state not in disaster_dict["state_county"]:
                disaster_dict["state_county"][state] = {county: 1}
            else:
                disaster_dict["state_county"][state][county] = disaster_dict["state_county"][state].get(county, 0) + 1

            #incident
            disaster_dict["incident"][incident] = disaster_dict["incident"].get(incident, 0) + 1

            #date
            if start_date.year == end_date.year:
                disaster_dict["date"][date.month] = disaster_dict["date"].get(date.month, 0) + 1
            else:
                disaster_dict["date"][date.year] = disaster_dict["date"].get(date.year, 0) + 1

        return disaster_dict
