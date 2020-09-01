import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
plt.style.use("acaps")

"""
Generate bar charts to show food sources and income sources for the 2018 and 2019 MSNA data.
"""
# Loop through the years
for year in ["2018", "2019"]:
    df = pd.read_csv("../../data/processed/MSNA_Host_"+year+".csv")

    # Loop through categories we're interested in
    for category in ["income_source"]:

        # Expand out options separated by spaces
        df_category = df[category].str.split(' ', expand=True)

        print(df_category)
