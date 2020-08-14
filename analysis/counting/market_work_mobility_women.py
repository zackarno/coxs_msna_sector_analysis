import pandas as pd
import sys

"""
Look at changes in women's market/ work mobility between the 2018 and 2019 datasets.
"""
# Read in the data
df_2018 = pd.read_csv("../../data/processed/MSNA_Host_2018.csv")
df_2019 = pd.read_csv("../../data/processed/MSNA_Host_2019.csv")

# Market mobility
df_market_2018 = df_2018["female_market"].dropna()
print(df_market_2018.unique())
print(df_market_2018.value_counts(normalize=True).reset_index().sort_values(by="index"))
print()

df_married_market_2019 = df_2019.loc[df_2019["respondent_gender"]=="female"]
df_married_market_2019 = df_married_market_2019.loc[df_married_market_2019["married_market_mobility"]!="not_applicable"]
df_married_market_2019 = df_married_market_2019["married_market_mobility"].dropna()
print(df_married_market_2019.unique())
print(df_married_market_2019.value_counts(normalize=True).reset_index().sort_values(by="index"))
print()

df_unmarried_market_2019 = df_2019.loc[df_2019["respondent_gender"]=="female"]
df_unmarried_market_2019 = df_unmarried_market_2019.loc[df_unmarried_market_2019["unmarried_market_mobility"]!="not_applicable"]
df_unmarried_market_2019 = df_unmarried_market_2019["unmarried_market_mobility"].dropna()
print(df_unmarried_market_2019.unique())
print(df_unmarried_market_2019.value_counts(normalize=True).reset_index().sort_values(by="index"))

# Working mobility
