import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import sys
plt.style.use("acaps")

"""
Create histograms showing the amount per household spend on different expenditure_categories, comparing the 2018 and 2019 MSNA data.
"""
expenditure_categories = {"exp_medical": "spend_medication", "exp_clothing": "spend_clothing", "exp_shelter_materials": "spend_fix_shelter", "exp_education": "spend_education", "exp_debt": "spend_debts", "exp_fuel": "spend_fuel", "exp_hygiene": "spend_hygiene", "exp_hhitems": "spend_hh_items", "exp_comms": "spend_communication", "exp_transport": "spend_transport", "exp_rent": "spend_rent", "exp_food": "spend_food"}
category_names = {"spend_medication": "medication", "spend_clothing": "clothing", "spend_fix_shelter": "shelter materials", "spend_education": "education", "spend_debts": "debts", "spend_fuel": "fuel", "spend_hygiene": "hygiene", "spend_hh_items": "household items", "spend_communication": "communication", "spend_transport": "transport", "spend_rent": "rent", "spend_food": "food"}

# Read in the 2018 and 2019 data
df_2018 = pd.read_csv("../../data/processed/MSNA_Host_2018.csv")
df_2019 = pd.read_csv("../../data/processed/MSNA_Host_2019.csv")
df_2018 = df_2018.dropna(subset=expenditure_categories, how="all")
df_2019 = df_2019.dropna(subset=expenditure_categories, how="all")
data = {"2018": df_2018, "2019": df_2019}

# Loop through the expenditure expenditure_categories and plot a histogram for each
bins=[0,501,1001,2001,5001,8001]
for category in expenditure_categories.values():
    fig, ax = plt.subplots(figsize=(14,8))
    for year in ["2018", "2019"]:
        hist, np_bins = np.histogram(data[year][[category]], bins)
        widths=[bins[i+1]-bins[i] for i in range(0, len(bins)-1)]
        x_coords = bins[:-1]
        heights = 100.0*hist.astype(np.float32) / hist.sum()
        ax.bar(x=x_coords, height=heights, width=widths, label=("MSNA "+year), alpha=0.5, tick_label=[0,500,1000,2000,5000], align="edge")
        #sns.distplot(data[year][[category]], hist=True, rug=False, norm_hist=False, kde=False, bins=bins, label=("MSNA "+year))
    plt.title("Household spending on "+category_names[category]+" in the host community", fontsize=20)
    plt.xlabel("Amount spent BDT")
    plt.ylabel("Percent of households")
    plt.legend(fontsize=14)
    plt.ylim([0,100])
    plt.xlim([0,7000])
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.savefig("histogram_expenditure_"+category_names[category].replace(" ","_")+".png")
    plt.close()
