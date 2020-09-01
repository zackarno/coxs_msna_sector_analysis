import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
plt.style.use("acaps")

"""
The logistic regression for the 2018 MSNA found that female headed households were more likely to have unnacceptable FCS scores than male headed households. This was not found in the 2019 MSNA. Therefore this module will look at the changes in the FCS distributions for female and male headed households between 2018 and 2019.

Also looking at the distribution in rCSI (a measurement of food security) for male and female headed households in 2018 (this data is not available for 2019).
"""

"""
Loop through both years and combine the data into a single dataframe
"""
df = pd.DataFrame()
for year in ["2018", "2019"]:
    # Read in the data and select only required columns
    df_year = pd.read_csv("../../data/processed/MSNA_Host_"+year+".csv")
    df_year = df_year[["hoh_gender", "FCS", "FCS_Category", "agri_land_yes", "spend_food", "hh_size"]]
    df_year["year"] = year
    df = df.append(df_year)
df = df.reset_index().drop(columns="index")

"""
Generate histograms showing the distribution of FCS scores for both male and female headed households, and households with/ without agricultural land
"""
# Loop through male and female headed households to generate a plot for each
for gender in ["male", "female"]:
    df_hist = df.loc[df["hoh_gender"]==gender]
    for year in ["2018", "2019"]:
        df_hist_year = df_hist.loc[df["year"]==year]
        sns.distplot(df_hist_year[["FCS"]], hist=False, rug=False, norm_hist=True, label=("MSNA "+year))
    plt.title("Distribution in household FCS scores for "+gender+" headed households in the host community", fontsize=20)
    plt.xlabel("Household FCS Score")
    plt.legend(fontsize=14)
    plt.xlim([0,120])
    plt.savefig("histogram_fcs_hoh_"+gender+".png")
    plt.close()

# Loop through households with/ without agricultural land to compare FCS scores
fcs_distributions = {}
for year in ["2018", "2019"]:
    df_year = df.loc[df["year"]==year]
    for owns_agricultural_land in [1,0]:
        df_year_hist = df_year.loc[df["agri_land_yes"]==owns_agricultural_land]
        labels = {1: "Households with agricultural land", 0: "Households without agricultural land"}
        sns.distplot(df_year_hist[["FCS"]], hist=False, rug=False, norm_hist=True, label=labels[owns_agricultural_land])
        fcs_distributions[owns_agricultural_land] = df_year_hist["FCS"]
    plt.title("Distribution in household FCS scores for households with and without agricultural land\nin the host community in "+year, fontsize=20)
    plt.xlabel("Household FCS Score")
    plt.legend(fontsize=14)
    plt.xlim([0,120])
    plt.savefig("histogram_fcs_agricultural_land_"+year+".png")
    plt.close()

    # Run a statistical test (Kolmogorov-Smirnov) to check if the distributions are the same
    results = stats.ks_2samp(fcs_distributions[0], fcs_distributions[1])
    print("Kolmogorov-Smirnov "+year+": "+str(results))
    print("Mean "+year+" without land: "+str(fcs_distributions[0].mean()))
    print("Median "+year+" without land: "+str(fcs_distributions[0].median()))
    print("Mean "+year+" with land: "+str(fcs_distributions[1].mean()))
    print("Median "+year+" with land: "+str(fcs_distributions[1].median()))

# Loop through households spending more/ less than 5000BDT on food to compare FCS scores
fcs_distributions = {}
for year in ["2018", "2019"]:
    df_year = df.loc[df["year"]==year]
    df_year["food_spending_per_person"] = df_year["spend_food"]/df_year["hh_size"]
    # Make the plot
    sns.scatterplot(data=df_year, x="food_spending_per_person", y="FCS")
    plt.title("Spending on food per person against FCS score for households in the host community in "+year, fontsize=20)
    plt.xlabel("Spending on food per person (BDT)")
    plt.ylabel("Household FCS Score")
    plt.legend(fontsize=14)
    plt.xlim([0,13000])
    plt.savefig("scatterplot_food_spending_fcs_"+year+".png")
    plt.close()

"""
Generate a histogram showing the distribution of rCSI (a measurement of food security/ food coping strategies) for the 2018 data (not available for the 2019 data)
"""
# Read in the 2018 data and select only required columns
df_rcsi = pd.read_csv("../../data/processed/MSNA_Host_2018.csv")
df_rcsi = df_rcsi[["hoh_gender", "rCSI"]]
for gender in ["male", "female"]:
    df_hist = df_rcsi.loc[df["hoh_gender"]==gender]
    print(gender.title()+"  headed households mean rCSI:"+str(df_hist["rCSI"].mean()))
    print(gender.title()+"  headed households median rCSI:"+str(df_hist["rCSI"].median()))
    sns.distplot(df_hist[["rCSI"]], hist=True, rug=False, norm_hist=True, kde=False, label=(gender.title()+" headed households"))
plt.title("Distribution in household rCSI scores in the host community", fontsize=20)
plt.legend(fontsize=14)
plt.xlim([0,60])
plt.savefig("histogram_rcsi.png")
plt.close()
