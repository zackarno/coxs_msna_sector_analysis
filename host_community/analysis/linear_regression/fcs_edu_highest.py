import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import sys
plt.style.use("acaps")

"""
Results of the logistic regression for 2019 data found that edu_highest_score had a significant positive effect on FCS_Category_acceptable. Therefore in this module we will plot edu_highest_score against FCS as these are both continuous variables. This can only be done for the 2019 data as the 2018 data did not contain a question on education level.
"""
# Read in the 2019 data and select only required columns
df = pd.read_csv("../../data/processed/MSNA_Host_2019.csv")
df = df[["FCS", "edu_highest_score", "hoh_gender"]]
df = df.dropna(how="any")

# Run a linear regression using the statsmodels package
Y = df["FCS"]
X = df["edu_highest_score"]
X = sm.add_constant(X)
model = sm.OLS(Y,X)
results = model.fit()
print(results.params)
print(results.summary())

# Run a linear regression using the sklearn package
Y = df["FCS"]
X = df["edu_highest_score"]
X = sm.add_constant(X)
reg = LinearRegression().fit(X, Y)
print(reg.score(X,Y))
print(reg.coef_)

# Plot the data as a scatter plot and run a linear regression to check the significance of the slope
fig, ax = plt.subplots(figsize=(15,8))
sns.scatterplot(data=df, x="edu_highest_score", y="FCS", hue="hoh_gender")
plt.savefig("./fcs_edu_highest_scatter.png")
plt.close()

# Plot the data as a box plt
fig, ax = plt.subplots(figsize=(15,8))
sns.boxplot(data=df, x="edu_highest_score", y="FCS")
plt.savefig("./fcs_edu_highest_boxplot.png")
plt.close()
