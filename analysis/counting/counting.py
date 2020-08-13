import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
plt.style.use("acaps")

"""
Run some general counts/ bar charts of different properties against each other.
"""

"""
Read in and process the data
"""
# Read in the data
df = pd.read_csv("../../data/processed/MSNA_Host_2019.csv")

"""
Start some counting
"""
# Count household coping mechanisms for married and unmarried households
df_married = df.loc[df["hoh_marital_married"]==1]
df_not_married = df.loc[df["hoh_marital_married"]==0]
