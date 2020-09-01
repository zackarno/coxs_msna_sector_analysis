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
Process the 2018 Rohingya MSNA
"""
# Read in the data as CSV
df = pd.read_csv("./raw/MSNA_Rohingya_2018.csv")

# Drop empty rows and irrelevant columns
df = df.dropna(how="all")
survey_questions = [column for column in df.columns if (column not in ["hh_id", "survey_consent"])]
df = df.dropna(how="all", subset=survey_questions)

# Save the processed data
df.to_csv("./processed/MSNA_Rohingya_2018.csv")


"""
Process the 2019 Rohingya MSNA
"""
# Read in the data as CSV
df = pd.read_csv("./raw/MSNA_Rohingya_2019.csv")

# Drop empty rows and irrelevant columns
df = df.dropna(how="all")
survey_questions = [column for column in df.columns if (column not in ["UUID", "survey_date", "informed_consent", "X_index"])]
df = df.dropna(how="all", subset=survey_questions)

# Save the processed data
df.to_csv("./processed/MSNA_Rohingya_2019.csv")
