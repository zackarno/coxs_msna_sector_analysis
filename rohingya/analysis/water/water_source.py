import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import math
plt.style.use("acaps")

"""
A simple module to generate some visualisations of water sources comparing 2018 to 2019.
"""

"""
Create a bar chart showing water in 2019
"""
# Read in the data
df_2019 = pd.read_csv("../../data/processed/MSNA_Rohingya_2019.csv")

water_source_questions_2019 = ["water_source_drink.pipe_water", "water_source_drink.tubewells", "water_source_drink.protected_dugwell", "water_source_drink.protected_spring", "water_source_drink.rainwater_collected", "water_source_drink.bottled_water", "water_source_drink.cart_small_tank", "water_source_drink.tanker_truck", "water_source_drink.unprotected_dugwell", "water_source_drink.unprotected_spring", "water_source_drink.surface_water", "water_source_drink.dont_know", "water_source_drink.other"]

# Calculate the proportions
df_2019_water = df_2019[water_source_questions_2019]
df_2019_water_counts = df_2019_water.sum().reset_index().rename(columns={"index": "Water source drink", 0: "total"})
df_2019_water_counts["percent"] = 100*df_2019_water_counts["total"]/len(df_2019_water.dropna(how="all"))
df_2019_water_counts = df_2019_water_counts.sort_values(by="percent", ascending=False)
df_2019_water_counts = df_2019_water_counts.loc[df_2019_water_counts["percent"] > 1]
df_2019_water_counts["Water source drink"] = df_2019_water_counts["Water source drink"].replace({"water_source_drink.tubewells": "Tubewells",
                                                                                                 "water_source_drink.pipe_water": "Pipewater",
                                                                                                 "water_source_drink.rainwater_collected": "Collected rainwater",
                                                                                                 "water_source_drink.cart_small_tank": "Cart small tank"})

# Create the plot
fig, ax = plt.subplots(figsize=(14,8))
ax = sns.barplot(x="Water source drink", y="percent", data=df_2019_water_counts) #, palette=colours)
plt.title("Main source of water for drinking and cooking for Rohingya households in 2019", fontsize=18)
plt.legend(fontsize=16, loc="upper right")
plt.xlabel(None)
plt.ylabel("Percent of households (%)", fontsize=16)
plt.ylim([0,100])
plt.xticks(rotation=0, fontsize=12)

# Add percentages to the bars
for p in ax.patches:
    width = p.get_width()
    height = p.get_height() if not math.isnan(p.get_height()) else 0.0
    x, y = p.get_xy()
    ax.annotate('{:.01%}'.format(round(height, 1)/100.0), (x + width/2, y + height+2), ha='center', fontsize=14)
plt.tight_layout()
plt.savefig("rohi_2019_primary_water_source.png")
plt.close()

"""
Create a bar chart showing water in 2018
"""
# Read in the data
df_2018 = pd.read_csv("../../data/processed/MSNA_Rohingya_2018.csv")

# Calculate the proportions
df_2018_water_counts = df_2018["drnk_wat"].value_counts(normalize=True).reset_index().rename(columns={"index": "Water source drink", "drnk_wat": "percent"})
df_2018_water_counts["percent"] = df_2018_water_counts["percent"]*100.0
df_2018_water_counts = df_2018_water_counts.loc[df_2018_water_counts["percent"] > 1]
df_2018_water_counts["Water source drink"] = df_2018_water_counts["Water source drink"].replace({"tubewell_borehole": "Tubewell or borehole",
                                                                                                 "piped_water": "Piped water",
                                                                                                 "water_tank": "Water tank"})

# Create the plot
fig, ax = plt.subplots(figsize=(14,8))
ax = sns.barplot(x="Water source drink", y="percent", data=df_2018_water_counts) #, palette=colours)
plt.title("Primary source of drinking water for Rohingya households in 2018", fontsize=18)
plt.legend(fontsize=16, loc="upper right")
plt.xlabel(None)
plt.ylabel("Percent of households (%)", fontsize=16)
plt.ylim([0,100])
plt.xticks(rotation=0, fontsize=12)

# Add percentages to the bars
for p in ax.patches:
    width = p.get_width()
    height = p.get_height() if not math.isnan(p.get_height()) else 0.0
    x, y = p.get_xy()
    ax.annotate('{:.01%}'.format(round(height, 1)/100.0), (x + width/2, y + height+2), ha='center', fontsize=14)
plt.tight_layout()
plt.savefig("rohi_2018_primary_water_source.png")
plt.close()
