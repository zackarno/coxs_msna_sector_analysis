import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
import sys
import seaborn as sns
plt.style.use("acaps")

"""
A simple model comparing the areas where men and women felt unsafe between the 2018 and 2019 data.
"""
# Read in the data
df_2018 = pd.read_csv("../../data/processed/MSNA_Rohingya_2018.csv")
df_2019 = pd.read_csv("../../data/processed/MSNA_Rohingya_2019.csv")

"""
Loop through men and women and compare areas where people feel unsafe
"""
descriptions = [["male", "men"], ["female", "women"]]
for men_women in descriptions:

    # Columns (2019 0/1: 2018 True/False)
    safety_columns = [["feel_unsafe_"+men_women[0]+".shelter", "unsafe_"+men_women[1]+"_shelter"],
                      ["feel_unsafe_"+men_women[0]+".latrine", "unsafe_"+men_women[1]+"_latrines"],
                      ["feel_unsafe_"+men_women[0]+".market", "unsafe_"+men_women[1]+"_market"],
                      ["feel_unsafe_"+men_women[0]+".health_center", "unsafe_"+men_women[1]+"_health_centre"],
                      ["feel_unsafe_"+men_women[0]+".water_points", "unsafe_"+men_women[1]+"_water_points"],
                      ["feel_unsafe_"+men_women[0]+".bathing_areas", "unsafe_"+men_women[1]+"_bathing_areas"],
                      ["feel_unsafe_"+men_women[0]+".spaces", "unsafe_"+men_women[1]+"_learning_spaces"],
                      ["feel_unsafe_"+men_women[0]+".distribution_points", "unsafe_"+men_women[1]+"_distribution_pp"],
                      ["feel_unsafe_"+men_women[0]+".firewood_site", "unsafe_"+men_women[1]+"_firewood"],
                      ["feel_unsafe_"+men_women[0]+".inside_home", "unsafe_"+men_women[1]+"_home"],
                      ["feel_unsafe_"+men_women[0]+".other", "unsafe_"+men_women[1]+"_other"],
                      ["feel_unsafe_"+men_women[0]+".dntknow_prefer", "unsafe_"+men_women[1]+"_dont_know"],
                      ["feel_unsafe_"+men_women[0]+".none", "unsafe_"+men_women[1]+"_none"],]
    safety_2018_columns = [columns[1] for columns in safety_columns]
    safety_2019_columns = [columns[0] for columns in safety_columns]
    rename_2019_columns = {columns[0]: columns[1] for columns in safety_columns}
    rename_all_columns = {columns[1]: columns[1].split("unsafe_"+men_women[1]+"_")[1].replace("_", " ").capitalize() for columns in safety_columns}

    # Select the data, drop nans, and rename the 2019 columns to match the 2018 columns
    df_2018_safety = df_2018[safety_2018_columns]
    df_2018_safety = df_2018_safety.dropna(how="all")
    df_2018_safety = df_2018_safety.rename(columns=rename_all_columns)
    df_2019.loc[df_2019["feel_unsafe_"+men_women[0]+".way_to_facilities"]==1.0, "feel_unsafe_"+men_women[0]+".way_to_facilities"] = 1.0
    df_2019_safety = df_2019[safety_2019_columns]
    df_2019_safety = df_2019_safety.dropna(how="all")
    df_2019_safety = df_2019_safety.rename(columns=rename_2019_columns)
    df_2019_safety = df_2019_safety.rename(columns=rename_all_columns)

    # Swap the 2018 True/ False to 1/0 to match 2019
    df_2018_safety = df_2018_safety.replace({True: 1.0, False: 0.0})

    # Calculate the percentages
    df_2018_safety_counts = df_2018_safety.sum().reset_index().rename(columns={"index": "Location feeling unsafe", 0: "total"})
    df_2018_safety_counts["percent"] = 100*df_2018_safety_counts["total"]/len(df_2018_safety.dropna(how="all"))
    df_2018_safety_counts["year"] = "2018"
    df_2019_safety_counts = df_2019_safety.sum().reset_index().rename(columns={"index": "Location feeling unsafe", 0: "total"})
    df_2019_safety_counts["percent"] = 100*df_2019_safety_counts["total"]/len(df_2019_safety.dropna(how="all"))
    df_2019_safety_counts["year"] = "2019"
    df_safety_counts = df_2019_safety_counts.append(df_2018_safety_counts)
    df_safety_counts["Location feeling unsafe"] = df_safety_counts["Location feeling unsafe"].replace({"Bathing areas": "Bathing\nareas",
                                                                                                       "Learning spaces": "Learning\nspaces",
                                                                                                       "Distribution pp": "Distribution\npoints",
                                                                                                       "Health centre": "Health\ncentre",
                                                                                                       "Water points": "Water\npoints"})

    # Create a plot to compare the data
    fig, ax = plt.subplots(figsize=(14,8))
    ax = sns.barplot(x="Location feeling unsafe", y="percent", data=df_safety_counts, hue="year", palette={"2019": "#0096ba", "2018": "#949392"}) #, palette=colours)
    plt.title("Areas where Rohingya "+men_women[1]+" do not feel safe, comparing 2018 and 2019", fontsize=18)
    plt.legend(fontsize=16, loc="upper left")
    plt.xlabel(None)
    plt.ylabel("Percent of households (%)", fontsize=16)
    plt.ylim([0,70])
    plt.xticks(rotation=0, fontsize=12)

    # Add percentages to the bars
    for p in ax.patches:
        width = p.get_width()
        height = p.get_height() if not math.isnan(p.get_height()) else 0.0
        x, y = p.get_xy()
        ax.annotate('{:.0%}'.format(round(height, 1)/100.0), (x + width/2, y + height+1), ha='center', fontsize=12)
    plt.tight_layout()
    plt.savefig(men_women[1]+"_areas_unsafe.png")
    plt.close()
