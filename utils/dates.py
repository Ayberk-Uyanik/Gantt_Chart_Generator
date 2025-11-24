# Importing Necessary Libraries #
import pandas as pd

# Arranging Dates #
def separate_dates (dataframe):
    # Convert Dates from Strings into Datetimes #
    dataframe["Start_Date"] = pd.to_datetime(dataframe["Start"], errors="coerce")
    dataframe["Start_Date"] = [i.date() for i in dataframe["Start_Date"]]

    dataframe["Finish_Date"] = pd.to_datetime(dataframe["Finish"], errors="coerce")
    dataframe["Finish_Date"] = [i.date() for i in dataframe["Finish_Date"]]

    return dataframe

def separate_dates_for_most_producing_wells_fields (dataframe):
    dataframe["Dates"] = pd.to_datetime(dataframe["End_Date"], errors="coerce")
    dataframe["Dates"] = [i.date() for i in dataframe["Dates"]]

    return dataframe

def calculate_time_differences(dataframe):
    # Constants #
    time_difference = []

    # Find the difference for the dates #
    for i in range (0, len(dataframe["Finish_Date"]), 1):
        width = dataframe["Finish_Date"][i] - dataframe["Start_Date"][i]
        time_difference.append(width)

    dataframe["Time_Difference"] = time_difference

    return dataframe