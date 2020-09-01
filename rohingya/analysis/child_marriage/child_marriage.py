import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import math
plt.style.use("acaps")

"""
A simple module to compare the number of child marriages in 2018 vs 2019.
"""
# Read in the data
df_2018 = pd.read_csv("../../data/processed/MSNA_Rohingya_2018.csv")
df_2019 = pd.read_csv("../../data/processed/MSNA_Rohingya_2019.csv")

# Select only required data
df_2019 = df_2019.loc[df_2019["child_marriage"]!="dntknow_no_answer"]
df_2019_child_marriage = df_2019[["child_marriage"]]
df_2018_child_marriage = df_2018[["child_marriage"]]
df_2018_child_marriage = df_2018_child_marriage.dropna(how="all")
df_2019_child_marriage = df_2019_child_marriage.dropna(how="all")

# Calculate the percentages for both years and combine the results
df_2018_child_marriage_counts = df_2018_child_marriage.value_counts(normalize=True).reset_index().rename(columns={0: "percent"})
df_2018_child_marriage_counts["year"] = "2018"
df_2018_child_marriage_counts["percent"] = df_2018_child_marriage_counts["percent"]*100.0
df_2019_child_marriage_counts = df_2019_child_marriage.value_counts(normalize=True).reset_index().rename(columns={0: "percent"})
df_2019_child_marriage_counts["year"] = "2019"
df_2019_child_marriage_counts["percent"] = df_2019_child_marriage_counts["percent"]*100.0
df_child_marriage_counts = df_2018_child_marriage_counts.append(df_2019_child_marriage_counts)
df_child_marriage_counts = df_child_marriage_counts.loc[df_child_marriage_counts["child_marriage"]=="yes"]
df_child_marriage_counts["child_marriage"] = df_child_marriage_counts["child_marriage"].replace({"yes":""})

# Create a plot to compare the data
fig, ax = plt.subplots(figsize=(10,8))
ax = sns.barplot(x="child_marriage", y="percent", data=df_child_marriage_counts, hue="year", palette={"2019": "#0096ba", "2018": "#949392"}) #, palette=colours)
plt.title("Percentage of households with children who are married\nor about to get married", fontsize=18)
plt.legend(fontsize=16, loc="upper left")
plt.xlabel(None)
plt.xticks(None)
ax.set_xticks([], minor=True)
plt.ylabel("Percent of households (%)", fontsize=16)
plt.ylim([0,15])

# Add percentages to the bars
for p in ax.patches:
    width = p.get_width()
    height = p.get_height() if not math.isnan(p.get_height()) else 0.0
    x, y = p.get_xy()
    ax.annotate('{:.01%}'.format(round(height, 1)/100.0), (x + width/2, y + height+0.2), ha='center', fontsize=16)
plt.tight_layout()
plt.savefig("child_marriage.png")
plt.close()
