import pandas as pd
import sys

"""
Compare Rohingya tensions between the 2018 and 2019 datasets. None of the questions are the same, but a general comparison can be made with care.
"""
# Read in the data
df_2018 = pd.read_csv("../../data/processed/MSNA_Host_2018.csv")
df_2019 = pd.read_csv("../../data/processed/MSNA_Host_2019.csv")

# Compare Rohingya relations between 2018 and 2019
print(df_2018["rohingya_comm_relation"].unique())
print(df_2018["rohingya_comm_relation"].value_counts(normalize=True))

print(df_2018["opinion_rohingya"].unique())
print(df_2018["opinion_rohingya"].value_counts(normalize=True))

print(df_2019["tension"].unique())
print(df_2019["tension"].value_counts(normalize=True))

#print(df_2019["rohi_hc_tensions"].unique())
#print(df_2019["rohi_hc_tensions"].value_counts())
