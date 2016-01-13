import os
import pandas as pd

"""This script merges all selected external data into a single external_data.csv.
NB : merge on "DateOfDeparture"."""

path = os.getcwd()

# Add baril price : departure.
# -------------

baril = pd.read_csv(os.path.join(path, "Submission/baril_departure.csv")).\
    set_index("DateOfDeparture")

# Add holidays.
# -------------

holidays = pd.read_csv(os.path.join(path, "Submission/holidays.csv")).\
    set_index("DateOfDeparture")

# Final.
# -------------

final = pd.concat([baril, holidays], axis=1, join='inner').reset_index()
final.to_csv(path + "/Submission/external_data.csv")
