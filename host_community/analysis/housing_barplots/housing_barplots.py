import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sys
import math
plt.style.use("acaps")

"""
Produce some bar charts showing shelter situation comparing the 2018 and 2019 data.
"""
# Read in the data
df_2018 = pd.read_csv("../../data/processed/MSNA_Host_2018.csv")
df_2019 = pd.read_csv("../../data/processed/MSNA_Host_2019.csv")

# Rename for consistency between the datasets and select only needed columns
df_2019.rename(columns={"deed": "land_house_deed", "rent_host": "rent_hosted", "agreement": "hh_agreement", "house_eviction": "eviction"}, inplace=True)
df_2018["land_house_deed"] = df_2018["land_house_deed"].replace({"dntknow_prefer": "decline"})
df_2018["eviction"] = df_2018["eviction"].replace({"dntknow_prefer": "decline"})

# Plot the proportion of households with particular housing situations
questions = ["house_land_ownership", "land_house_deed", "rent_hosted", "hh_agreement"]
titles = {"house_land_ownership": "Percentage of households who own land and/ or a house",
          "land_house_deed": "Percentage of households who hold a deed for land and/ or a house",
          "rent_hosted": "Percentage of households who pay rent/ are hosted",
          "hh_agreement": "Percentage of households who hold a written agreement with the landlord"}
answers = {"house_land_ownership": {"yes_own": "Own land and/ or a house", "no_dont_own": "Don't own land or a house", "co_own": "Co-own land and/ or a house"},
          "land_house_deed": {"yes": "Hold a deed", "no": "No deed", "decline": "Decline to answer"},
          "rent_hosted": {"caregiver": "Caregiver", "hosted": "Hosted", "pay_rent": "Pay rent"},
          "hh_agreement": {"no": "No written agreement", "yes": "Written agreement", "dntknow_prefer": "Decline to answer"}}

for question in questions:
    df_counts_2018 = df_2018[question].value_counts(normalize=True).reset_index().rename(columns={"index": "answer", question: "percent"})
    df_counts_2018["year"] = "2018"
    df_counts_2019 = df_2019[question].value_counts(normalize=True).reset_index().rename(columns={"index": "answer", question: "percent"})
    df_counts_2019["year"] = "2019"
    df_counts = df_counts_2018.append(df_counts_2019)
    df_counts["percent"] = df_counts["percent"]*100.0
    df_counts["answer"] = df_counts["answer"].replace(answers[question])

    # Create the plot
    fig, ax = plt.subplots(figsize=(11,8))
    ax = sns.barplot(x="answer", y="percent", hue="year", data=df_counts) #, palette=colours)
    plt.title(titles[question], fontsize=18)
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
        ax.annotate('{:.0%}'.format(round(height)/100.0), (x + width/2, y + height+2), ha='center', fontsize=12)
    plt.tight_layout()
    plt.savefig(question+".png")
    plt.close()
