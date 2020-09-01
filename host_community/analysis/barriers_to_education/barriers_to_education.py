import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sys
import math
plt.style.use("acaps")

"""
Compare the barriers to education between the 2018 and 2019 data.
"""
# Read in the data
df_2018 = pd.read_csv("../../data/processed/MSNA_Host_2018.csv")
df_2019 = pd.read_csv("../../data/processed/MSNA_Host_2019.csv")

"""
Look at the 2018 data
"""
# Loop through primary and secondary school data from 2018 and plot
barriers = ["facillities_too_far", "safety_concerns_way_facilities", "services_too_expensive", "services_too_crowded", "insufficient_poorquality_staff", "school_not_adequate_infra", "school_not_adequate_material", "face_discrimination", "children_support_family", "parents_think_not_appropriate", "other", "dont_know"]
barriers_prefix = {"primary": "/", "secondary": "_1/"}
barriers_first_column = {"primary": "prim", "secondary": "second"}

for school in ["primary", "secondary"]:

    # Select data on girl and boy education barriers for 2018
    df_boy = df_2018[["boy_"+barriers_first_column[school]+"_edu_barrier"]+["boy_edu_barrier"+barriers_prefix[school]+barrier for barrier in barriers]].dropna(how="all").replace({True: 1, False: 0})
    df_girl = df_2018[["girl_"+barriers_first_column[school]+"_edu_barrier"]+["girl_edu_barrier"+barriers_prefix[school]+barrier for barrier in barriers]].dropna(how="all").replace({True: 1, False: 0})
    df_boy = df_boy.rename(columns={("boy_edu_barrier"+barriers_prefix[school]+barrier): barrier for barrier in barriers}).fillna(0).drop(columns=["boy_"+barriers_first_column[school]+"_edu_barrier"])
    df_girl = df_girl.rename(columns={("girl_edu_barrier"+barriers_prefix[school]+barrier): barrier for barrier in barriers}).fillna(0).drop(columns=["girl_"+barriers_first_column[school]+"_edu_barrier"])

    # Calculate the proportions and then combine the datasets
    df_boy_counts = df_boy.sum().reset_index().rename(columns={"index": "Education barrier", 0: "total"})
    df_boy_counts["percent"] = 100*df_boy_counts["total"]/len(df_boy.dropna(how="all"))
    df_boy_counts["child"] = "Boys"
    df_girl_counts = df_girl.sum().reset_index().rename(columns={"index": "Education barrier", 0: "total"})
    df_girl_counts["percent"] = 100*df_girl_counts["total"]/len(df_girl.dropna(how="all"))
    df_girl_counts["child"] = "Girls"
    df_counts = df_boy_counts.append(df_girl_counts)

    # Drop the small results
    main_barriers = {"facillities_too_far": "Facilities\ntoo far",
                     "safety_concerns_way_facilities": "Safety concerns\non the way to\nfacilities",
                     "services_too_expensive": "Services\ntoo expensive",
                     "services_too_crowded": "Services\ntoo crowded",
                     "insufficient_poorquality_staff": "Insufficient\npoor quality\nstaff",
                     "school_not_adequate_infra": "School not\nadequate\ninfrastructure",
                     "school_not_adequate_material": "School not\nadequate\nmaterial",
                     "face_discrimination": "Face\ndiscrimination",
                     "children_support_family": "Children\nsupport the\nfamily",
                     "parents_think_not_appropriate": "Parents\nthink not\nappropriate"}
    #df_counts = df_counts.loc[df_counts["Education barrier"].isin(list(main_barriers.keys()))]
    df_counts = df_counts.loc[~df_counts["Education barrier"].isin(list(["other", "dont_know"]))]
    df_counts["Education barrier"] = df_counts["Education barrier"].replace(main_barriers)

    # Create the plot
    fig, ax = plt.subplots(figsize=(14,8))
    ax = sns.barplot(x="Education barrier", y="percent", hue="child", data=df_counts) #, palette=colours)
    plt.title("Barriers to sending girls and boys to "+school+" school in the host community in 2018", fontsize=18)
    plt.legend(fontsize=16, loc="upper right")
    plt.xlabel(None)
    plt.ylabel("Percent of households (%)", fontsize=16)
    plt.ylim([0,12.5])
    plt.xticks(rotation=0, fontsize=12)

    # Add percentages to the bars
    for p in ax.patches:
        width = p.get_width()
        height = p.get_height() if not math.isnan(p.get_height()) else 0.0
        x, y = p.get_xy()
        ax.annotate('{:.01%}'.format(round(height, 1)/100.0), (x + width/2, y + height+0.25), ha='center', fontsize=12)
    plt.tight_layout()
    plt.savefig(school+"_education_barriers_2018.png")
    plt.close()

"""
Look at the 2019 data
"""
# Loop through data from 2019
barriers = {"education_barrier.facillities_too_far": "Facilities\ntoo far",
            "education_barrier.school_unsafe": "School\nunsafe",
            "education_barrier.way_unsafe": "Way\nunsafe",
            "education_barrier.edu_expensive": "Too\nexpensive",
            "education_barrier.services_too_crowded": "Too\ncrowded",
            "education_barrier.school_not_adequate_material": "Not adequate\nmaterial",
            "education_barrier.wash_not_adequate": "Wash not\nadequate",
            "education_barrier.help_family": "Help\nfamily",
            "education_barrier.child_income": "Child\nincome",
            "education_barrier.not_useful_appropriate": "Not useful/\nappropriate",
            "education_barrier.cultural_reason": "Cultural\nreason",
            "education_barrier.gets_married": "Married",
            "education_barrier.go_to_madrasah": "Go to\nmadrash",
            "education_barrier.child_disabled": "Child\ndisabled",
            "education_barrier.face_discrimination": "Face\ndiscrimination",
            "education_barrier.enough_about_the_educatoin": "Enough\nabout the\neducation",
            "education_barrier.dntknow_no_answer": "Don't\nknow/ no\nanswer",
            "education_barrier.other": "Other"}
df_school = df_2019[list(barriers.keys())].rename(columns=barriers).dropna(how="all")

# Calculate the proportions
df_school_counts = df_school.sum().reset_index().rename(columns={"index": "Education barrier", 0: "total"})
df_school_counts["percent"] = 100*df_school_counts["total"]/len(df_school.dropna(how="all"))
df_school_counts = df_school_counts.sort_values(by="percent", ascending=False)
df_school_counts = df_school_counts.loc[~df_school_counts["Education barrier"].isin(["Other", "Face\ndiscrimination","Wash not\nadequate", "Enough\nabout the\neducation"])]

# Create the plot
fig, ax = plt.subplots(figsize=(14,8))
ax = sns.barplot(x="Education barrier", y="percent", data=df_school_counts) #, palette=colours)
plt.title("Barriers to sending children to school in the host community in 2019", fontsize=18)
plt.legend(fontsize=16, loc="upper right")
plt.xlabel(None)
plt.ylabel("Percent of households (%)", fontsize=16)
#plt.ylim([0,12.5])
plt.xticks(rotation=0, fontsize=12)

# Add percentages to the bars
for p in ax.patches:
    width = p.get_width()
    height = p.get_height() if not math.isnan(p.get_height()) else 0.0
    x, y = p.get_xy()
    ax.annotate('{:.01%}'.format(round(height, 1)/100.0), (x + width/2, y + height+0.25), ha='center', fontsize=12)
plt.tight_layout()
plt.savefig("education_barriers_2019.png")
plt.close()
