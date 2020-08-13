import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
plt.style.use("acaps")

"""
Run some general counts/ bar charts of different properties against each other. Run counts for the 2018 and 2019 data, and compare. Save the results in a CSV file.
"""
# Define indicators that can be compared between both datasets
indicators = ["electricity_grid_score", "enough_water_drinking_cooking_washing", "child_marriage_score"]
proportions = {"2018": {}, "2019": {}}

# Loop through indicators and years
for year in ["2018", "2019"]:
    # Read in the data for that year
    df = pd.read_csv("../../data/processed/MSNA_Host_"+year+".csv")

    # Loop through indicators and calculate proportions (indicators are all 0/1)
    for indicator in indicators:

        df_indicator = df[indicator].dropna()
        proportion = df_indicator.sum()/float(df_indicator.size)
        proportions[year][indicator] = round(100*proportion)

print(proportions)
