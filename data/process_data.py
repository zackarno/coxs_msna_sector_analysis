import pandas as pd
import sys

"""
Process the data, ensure columns are tidy, convert dates to correct formats, etc.
"""
# Read in the data as CSV
df = pd.read_csv("./raw/MSNA_Host_2019.csv")

# Drop empty rows
df = df.dropna(how="all")
survey_questions = [column for column in df.columns if (column not in ["UUID", "survey_date", "enum_gender", "upazila_name", "union_name", "informed_consent", "X_index"])]
df = df.dropna(how="all", subset=survey_questions)

# Set head of household gender and age where it is given as N/A
df.loc[(df["hoh_gender"].isnull()) & (df["respondent_hoh"] == "yes"), "hoh_gender"] = df["respondent_gender"]
df.loc[(df["hoh_age"].isnull()) & (df["respondent_hoh"] == "yes"), "hoh_age"] = df["respondent_age"]

# Create a new column for whether or not married
df["hoh_marital_married"] = 0
df.loc[df["hoh_marital"]=="married", "hoh_marital_married"] = 1

# Tidy the edu_highest column to make it numeric for all answers
df["edu_highest_score"] = df["edu_highest"]
df.loc[df["edu_highest_score"]=="none", "edu_highest_score"] = 0
df.loc[df["edu_highest_score"]=="above_12_tertiary_edu", "edu_highest_score"] = 13
df.loc[df["edu_highest_score"]=="madrasah_only", "edu_highest_score"] = 1

# Add a yes/ no column for the feel unsafe columns
df["feel_unsafe_male_yes_no"] = 1
df.loc[df["feel_unsafe_male"]=="none", "feel_unsafe_male_yes_no"] = 0
df.loc[df["feel_unsafe_male"].isnull(), "feel_unsafe_male_yes_no"] = float("nan")
df["feel_unsafe_female_yes_no"] = 1
df.loc[df["feel_unsafe_female"]=="none", "feel_unsafe_female_yes_no"] = 0
df.loc[df["feel_unsafe_female"].isnull(), "feel_unsafe_female_yes_no"] = float("nan")

# Add a yes/ no column to the drinking water column
df["enough_water_drinking_cooking_washing"] = 0
df.loc[df["enough_water.dont_know"]==1, "enough_water_drinking_cooking_washing"] = float("nan")
df.loc[(df["enough_water.drinking"]==1) & (df["enough_water.cooking"]==1) & (df["enough_water.washing_bathing"]==1), "enough_water_drinking_cooking_washing"] = 1

# Save the processed data
df.to_csv("./processed/MSNA_Host_2019.csv", index=False)
