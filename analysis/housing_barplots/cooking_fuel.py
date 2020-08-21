import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sys
import math
plt.style.use("acaps")

"""
Produce some bar charts showing the use of cooking fuel in 2018 and 2019.
"""
# Read in the data
df_2018 = pd.read_csv("../../data/processed/MSNA_Host_2018.csv")
df_2019 = pd.read_csv("../../data/processed/MSNA_Host_2019.csv")

df_2018 = df_2018[["cooking_fuel"]]
df_2019 = df_2019[["cooking_fuel"]]

# Pivot the data
for idx, row in df_2019.iterrows():
    for cooking_fuel in row["cooking_fuel"].split(" "):
        df_2019.loc[idx, cooking_fuel] = 1
for cooking_fuel in df_2018["cooking_fuel"].unique():
    df_2018.loc[df_2018["cooking_fuel"]==cooking_fuel, cooking_fuel] = 1

df_2018 = df_2018.fillna(0)
df_2019 = df_2019.fillna(0)

# Make the 2018 and 2019 datasets consistent
df_2019.loc[(df_2019["purchased_firewood"]==1) | (df_2019["collected_firewood"]==1), "firewood"] = 1
cooking_fuel_list = {"firewood": "Firewood", "lpg_gas_cylinder": "LPG gas cylinder", "dried_leaf_hay": "Dried leaf hay", "biogas": "Biogas", "dung_cakes": "Dung cakes", "induction": "Induction"}
df_2018 = df_2018[list(cooking_fuel_list.keys())]
df_2019 = df_2019[list(cooking_fuel_list.keys())]
data = {"2018": df_2018, "2019": df_2019}

# Calculate proportions
df_2018_counts = df_2018.sum().reset_index().rename(columns={"index": "Cooking Fuel", 0: "total"})
df_2018_counts["percent"] = 100*df_2018_counts["total"]/len(df_2018.dropna(how="all"))
df_2019_counts = df_2019.sum().reset_index().rename(columns={"index": "Cooking Fuel", 0: "total"})
df_2019_counts["percent"] = 100*df_2019_counts["total"]/len(df_2019.dropna(how="all"))

# Loop through years and create plots
titles = {"2018": "Primary cooking fuel used by households in the host community in 2018",
          "2019": "All cooking fuels used by households in the host community in 2019"}
for year in ["2018", "2019"]:
    # Select the data and calculate proportions
    df = data[year]
    df = df.sum().reset_index().rename(columns={"index": "Cooking Fuel", 0: "total"})
    df["percent"] = 100*df["total"]/len(data[year].dropna(how="all"))
    df["Cooking Fuel"] = df["Cooking Fuel"].replace(cooking_fuel_list)

    # Create the plot
    fig, ax = plt.subplots(figsize=(14,8))
    ax = sns.barplot(x="Cooking Fuel", y="percent", data=df) #, palette=colours)
    plt.title(titles[year], fontsize=18)
    plt.legend(fontsize=16, loc="upper right")
    plt.xlabel(None)
    plt.ylabel("Percent of households (%)", fontsize=16)
    plt.ylim([0,100])
    plt.xticks(rotation=0, fontsize=14)

    # Add percentages to the bars
    for p in ax.patches:
        width = p.get_width()
        height = p.get_height() if not math.isnan(p.get_height()) else 0.0
        x, y = p.get_xy()
        ax.annotate('{:.0%}'.format(round(height)/100.0), (x + width/2, y + height+2), ha='center', fontsize=14)
    plt.tight_layout()
    plt.savefig("cooking_fuels_"+year+".png")
    plt.close()
