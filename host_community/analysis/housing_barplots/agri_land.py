import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sys
import math
plt.style.use("acaps")

"""
Compare households owning agricultural land in 2018 and 2019 in the host community.
"""
# Read in the data
df_2018 = pd.read_csv("../../data/processed/MSNA_Host_2018.csv")
df_2019 = pd.read_csv("../../data/processed/MSNA_Host_2019.csv")

# Calculate proportions and merge the datasets
df_counts_2018 = df_2018["hh_agri_land"].value_counts(normalize=True).reset_index().rename(columns={"index": "answer", "hh_agri_land": "percent"})
df_counts_2018["year"] = "2018"
df_counts_2019 = df_2019["agricultural_land"].value_counts(normalize=True).reset_index().rename(columns={"index": "answer", "agricultural_land": "percent"})
df_counts_2019["year"] = "2019"
df_counts = df_counts_2018.append(df_counts_2019)
df_counts["percent"] = df_counts["percent"]*100.0
df_counts["answer"] = df_counts["answer"].replace({"yes": "Yes", "no": "No"})

# Create the plot
fig, ax = plt.subplots(figsize=(10,8))
ax = sns.barplot(x="answer", y="percent", hue="year", data=df_counts)
plt.title("Percentage of households in the host community\nwith agricultural land in 2018 and 2019", fontsize=18)
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
plt.savefig("agricultural_land.png")
plt.close()
