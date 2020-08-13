import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use("acaps")

"""
The logistic regression for the 2018 MSNA found that female headed households were more likely to have unnacceptable FCS scores than male headed households. This was not found in the 2019 MSNA. Therefore this module will look at the changes in the FCS distributions for female and male headed households between 2018 and 2019.
"""

"""
Loop through both years and combine the data into a single dataframe
"""
df = pd.DataFrame()
for year in ["2018", "2019"]:
    # Read in the data and select only required columns
    df_year = pd.read_csv("../../data/processed/MSNA_Host_"+year+".csv")
    df_year = df_year[["hoh_gender", "FCS", "FCS_Category"]]
    df_year["year"] = year
    df = df.append(df_year)
df = df.reset_index().drop(columns="index")

"""
Generate histograms showing the distribution of FCS scores for both male and female headed households
"""
# Loop through male and female headed households to generate a plot for each
for gender in ["male", "female"]:
    df_hist = df.loc[df["hoh_gender"]==gender]
    for year in ["2018", "2019"]:
        df_hist_year = df_hist.loc[df["year"]==year]
        sns.distplot(df_hist_year[["FCS"]], hist=False, rug=False, norm_hist=True, label=("MSNA "+year))
    plt.title("Distribution in household FCS scores for "+gender+" headed households in the host community", fontsize=20)
    plt.legend(fontsize=14)
    plt.xlim([0,120])
    plt.savefig("histogram_fcs_hoh_"+gender+".png")
    plt.close()
