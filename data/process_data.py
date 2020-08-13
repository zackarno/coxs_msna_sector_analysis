import pandas as pd

"""
Process the data, ensure columns are tidy, convert dates to correct formats, etc.
"""
# Read in the data as CSV
df = pd.read_csv("./raw/MSNA_Host_2019.csv")

# Drop empty rows
df = df.dropna(how="all")
survey_questions = [column for column in df.columns if (column not in ["UUID", "survey_date", "enum_gender", "upazila_name", "union_name", "informed_consent", "X_index"])]
df = df.dropna(how="all", subset=survey_questions)

# Set head of household gender where it is given as N/A
df.loc[df["hoh_gender"].isnull(), "hoh_gender"] = df["respondent_gender"]

# Create a new column for whether or not married
df["hoh_marital_married"] = 0
df.loc[df["hoh_marital"]=="married", "hoh_marital_married"] = 1

# Save the processed data
df.to_csv("./processed/MSNA_Host_2019.csv", index=False)
