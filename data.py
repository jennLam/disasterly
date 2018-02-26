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

    def __advanced_search(self, state=None, incident_type=None, start_date=None, end_date=None):
        """Advanced search of disaster data."""

        condition = self.df

        if state or incident_type or start_date or end_date:

            s = self.search_criteria("state", state, op.eq)
            i = self.search_criteria("incidentType", incident_type, op.eq)
            sd = self.search_criteria("incidentBeginDate", start_date, op.ge)
            ed = self.search_criteria("incidentBeginDate", end_date, op.le)

            condition = self.df[s & i & sd & ed]

        return condition

    def __make_dict(self, dataframe, column_name, time_measure=None):
        """Create a dictionary from dataframe using column_name."""

        data_dict = {}

        for i, row in dataframe.iterrows():

            if not time_measure:
                column = row[column_name]
            elif time_measure == "year":
                column = row[column_name].year
            elif time_measure == "month":
                column = row[column_name].month

            data_dict[column] = data_dict.get(column, 0) + 1

        return data_dict

    def disaster_dict(self, state=None, incident_type=None, start_date=None, end_date=None):

        dataframe = self.__advanced_search(state, incident_type, start_date, end_date)

        unique_disasers = dataframe.drop_duplicates(subset="disasterNumber", keep="last")

        unique_disasers_and_states = dataframe.drop_duplicates(subset=["disasterNumber", "state"], keep="last")

        #incident type

        incident = self.__make_dict(unique_disasers, "incidentType")

        #state

        state = self.__make_dict(unique_disasers_and_states, "state")

        #time

        start_date = unique_disasers["incidentBeginDate"].head(1).iloc[0]
        end_date = unique_disasers["incidentBeginDate"].tail(1).iloc[0]

        if start_date.year == end_date.year:
            date = self.__make_dict(unique_disasers, "incidentBeginDate", "month")
        else:
            date = self.__make_dict(unique_disasers, "incidentBeginDate", "year")

        disaster_dict = {"state": state,
                         "incident": incident,
                         "date": date,
                         "state_county": {}}

        for i, row in dataframe.iterrows():

            county = row["declaredCountyArea"]

            #state and county
            if row["state"] not in disaster_dict["state_county"]:
                disaster_dict["state_county"][row["state"]] = {county: 1}
            else:
                disaster_dict["state_county"][row["state"]][county] = disaster_dict["state_county"][row["state"]].get(county, 0) + 1

        return disaster_dict
