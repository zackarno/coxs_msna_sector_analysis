import pandas as pd
import sys

"""
Process the data, ensure columns are tidy, convert dates to correct formats, etc.
"""
"""
Useful functions
"""
def calculate_fcs_score(cereals_tubers, pulses_nuts_seeds, vegetables, fruits, dairy, meat_fish, oil_fats, sweets):
    weights = {"cereals_tubers": 2, "pulses_nuts_seeds": 3, "vegetables": 1, "fruits": 1, "dairy": 4, "meat_fish": 4, "oil_fats": 0.5, "sweets": 0.5}
    fcs_score = (cereals_tubers*weights["cereals_tubers"])+\
                (pulses_nuts_seeds*weights["pulses_nuts_seeds"])+\
                (vegetables*weights["vegetables"])+\
                (fruits*weights["fruits"])+\
                (dairy*weights["dairy"])+\
                (meat_fish*weights["meat_fish"])+\
                (oil_fats*weights["oil_fats"])+\
                (sweets*weights["sweets"])
    return fcs_score

def calculate_fcs_category(fcs_score):
    categories = {"Poor": [0, 21], "Borderline": [21, 35], "Acceptable": [35]}
    if fcs_score <= 21: return "Poor"
    elif fcs_score <= 35: return "Borderline"
    elif fcs_score > 35: return "Acceptable"

"""
Process the 2019 Host MSNA
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

# Add an electricity_grid_score column to be 1/0 rather than yes/no
df.loc[df["electricity_grid"]=="yes", "electricity_grid_score"] = 1
df.loc[df["electricity_grid"]=="no", "electricity_grid_score"] = 0

# Calculate FCS (https://inddex.nutrition.tufts.edu/data4diets/indicator/food-consumption-score-fcs)
df["FCS"] = df.apply(lambda row: calculate_fcs_score(row["cereals_tubers"], row["pulses_nuts_seeds"], row["vegetables"], row["fruits"], row["dairy"], row["meat_fish"], row["oil_fats"], row["sweets"]), axis=1)
df["FCS_Category"] = df["FCS"].apply(lambda fcs_score: calculate_fcs_category(fcs_score))
df.loc[(df["FCS_Category"]=="Acceptable"), "FCS_Category_acceptable"] = 1
df.loc[(df["FCS_Category"]=="Borderline") | (df["FCS_Category"]=="Poor"), "FCS_Category_acceptable"] = 0

# Convert the child_marriage column into a 0/1 score
df.loc[df["child_marriage"]=="yes", "child_marriage_score"] = 1
df.loc[df["child_marriage"]=="no", "child_marriage_score"] = 0

# Convert the expenditure columns to values to be consistent with the 2018 data
def quantify_expenditure(amount):
    if amount == "0_bdt": return 0
    elif amount == "1_500_bdt": return 250
    elif amount == "501_1000_bdt": return 750
    elif amount == "1001_2000_bdt": return 1500
    elif amount == "2001_5000_bdt": return 3500
    elif amount == "5001_plus_bdt": return 5500
column_mapping = {"exp_medical": "spend_medication", "exp_clothing": "spend_clothing", "exp_shelter_materials": "spend_fix_shelter", "exp_education": "spend_education", "exp_debt": "spend_debts", "exp_fuel": "spend_fuel", "exp_hygiene": "spend_hygiene", "exp_hhitems": "spend_hh_items", "exp_comms": "spend_communication", "exp_transport": "spend_transport", "exp_rent": "spend_rent", "exp_food": "spend_food"}
for categorised_column in column_mapping:
    df[column_mapping[categorised_column]] = df[categorised_column].apply(lambda amount: quantify_expenditure(amount))

# Save the processed data
df.to_csv("./processed/MSNA_Host_2019.csv", index=False)

"""
Process the 2018 Host MSNA
"""
# Read in the data as CSV
df = pd.read_csv("./raw/MSNA_Host_2018.csv")

# Drop empty rows and keep only consenting results
df = df.dropna(how="all")
df = df.loc[df["survey_consent"]=="yes"]

# Rename columns to be consistent with the 2019 MSNA
df = df.rename(columns={"hh_gender": "hoh_gender", "hh_head": "respondent_hoh", "hh_marriage_person": "child_marriage", "main_source_food": "food_source", "main_income": "income_source"})

# Set head of household gender and age where it is given as N/A
df.loc[(df["hoh_gender"].isnull()) & (df["respondent_hoh"] == "yes"), "hoh_gender"] = df["respondent_gender"]

# Add an adult male count
df["adult_male_count"] = df["hh_size"]-df["adult_female_count"]-df["boy_6_11_count"]-df["girl_6_11_count"]-df["boy_12_18_count"]-df["girl_12_18_count"]
df = df.loc[df["adult_male_count"] != -1.0]

# Add an electricity_grid_score column to be 1/0 rather than yes/no
df.loc[df["electricity_grid"]=="yes", "electricity_grid_score"] = 1
df.loc[df["electricity_grid"]=="no", "electricity_grid_score"] = 0

# Add a column to denote whether food had been borrowed or limited in the last week
df["food_borrowed_limited"] = 0
df.loc[(df["borrowed_food"]>0) | (df["limit_portion_size"]>0) | (df["restrict_consumption"]>0) | (df["reduce_meal_numbers"]>0) | (df["eat_elsewhere"]>0) | (df["women_eat_less"]>0) | (df["men_eat_less"]>0) | (df["nofood_wholeday"]>0), "food_borrowed_limited"] = 1

# Check FCS scores are consistent
df["FCS"] = df.apply(lambda row: calculate_fcs_score(row["cereals_tubers"], row["pulses_nuts_seeds"], row["vegetables"], row["fruits"], row["dairy"], row["meat_fish"], row["oil_fats"], row["sweets"]), axis=1)
df["FCS_Category"] = df["FCS"].apply(lambda fcs_score: calculate_fcs_category(fcs_score))
df.loc[(df["FCS_Category"]=="Acceptable"), "FCS_Category_acceptable"] = 1
df.loc[(df["FCS_Category"]=="Borderline") | (df["FCS_Category"]=="Poor"), "FCS_Category_acceptable"] = 0

# Convert the FCS score to 0/1 to be used in logistic regression
df.loc[(df["FCS_Category"]=="Acceptable high") | (df["FCS_Category"]=="Acceptable low"), "FCS_Category_acceptable"] = 1
df.loc[(df["FCS_Category"]=="Borderline Consumption") | (df["FCS_Category"]=="Poor consumption"), "FCS_Category_acceptable"] = 0

# Convert the PPIx_Category column into a 0/1 score to be used in logistic regression
df.loc[df["PPIx_Category"]=="Less than 97% chance to be have less than USD3.10/day", "PPIx_Category_acceptable"] = 1
df.loc[df["PPIx_Category"]=="More than 97% chance to be have less than USD3.10/day", "PPIx_Category_acceptable"] = 0

# Convert the enough_water column into a 0/1 score and rename to be consistent with the 2019 data
df.loc[df["enough_water"]=="yes", "enough_water_drinking_cooking_washing"] = 1
df.loc[df["enough_water"]=="no", "enough_water_drinking_cooking_washing"] = 0

# Convert the child_marriage column into a 0/1 score
df.loc[df["child_marriage"]=="yes", "child_marriage_score"] = 1
df.loc[df["child_marriage"]=="no", "child_marriage_score"] = 0

# Convert the expenditure columns to categories to be consistent with the 2019 data
def categorise_expenditure(amount):
    if amount == 0: return "0_bdt"
    elif amount <= 500: return "1_500_bdt"
    elif amount <= 1000: return "501_1000_bdt"
    elif amount <= 2000: return "1001_2000_bdt"
    elif amount <= 5000: return "2001_5000_bdt"
    elif amount > 5000: return "5001_plus_bdt"
column_mapping = {"exp_medical": "spend_medication", "exp_clothing": "spend_clothing", "exp_shelter_materials": "spend_fix_shelter", "exp_education": "spend_education", "exp_debt": "spend_debts", "exp_fuel": "spend_fuel", "exp_hygiene": "spend_hygiene", "exp_hhitems": "spend_hh_items", "exp_comms": "spend_communication", "exp_transport": "spend_transport", "exp_rent": "spend_rent", "exp_food": "spend_food"}
for categorised_column in column_mapping:
    df[categorised_column] = df[column_mapping[categorised_column]].apply(lambda amount: categorise_expenditure(amount))

# Save the processed data
df.to_csv("./processed/MSNA_Host_2018.csv", index=False)
