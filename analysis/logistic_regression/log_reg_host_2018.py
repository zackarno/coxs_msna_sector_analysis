import pandas as pd
import sys
import math
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.utils import resample
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import statsmodels.api as sm
plt.style.use("acaps")

"""
Run a logistic regression on the host 2019 MSNA data.
"""

"""
Read in and process the data
"""
# Read in the data
df = pd.read_csv("../../data/processed/MSNA_Host_2018.csv")

# Set the variables
min_counts = None
all_vars = {"categorical_vars": ["hoh_gender"],
            "continuous_vars": ["hh_size"]}
variables = {"electricity_grid_score": {"categorical_vars": all_vars["categorical_vars"],
                                        "continuous_vars": all_vars["continuous_vars"]},
             "food_borrowed_limited": {"categorical_vars": all_vars["categorical_vars"],
                                       "continuous_vars": all_vars["continuous_vars"]},
             "FCS_Category_acceptable": {"categorical_vars": all_vars["categorical_vars"],
                                       "continuous_vars": all_vars["continuous_vars"]},}

"""
Loop through the dependent variables and run a logistic regression for each with different inputs.
"""
for dependent_variable in variables.keys():
    df_log = df.copy()

    """
    Prepare the data for the model by selecting variables, converting categorical variables using one-hot encoding, dropping nans, and dropping the first column of categorical variables.
    """
    # Set the categorical and continuous variables
    categorical_vars = variables[dependent_variable]["categorical_vars"]
    continuous_vars = variables[dependent_variable]["continuous_vars"]

    # Only keep rows with school age children if we are running the "Materiales de estudio" option
    df_log = df_log[[dependent_variable]+categorical_vars+continuous_vars]
    df_log = df_log.dropna(subset=([dependent_variable]+categorical_vars+continuous_vars), how="any")

    # Remove categories with few datapoints
    if min_counts != None:
        for variable in (categorical_vars+continuous_vars):
            counts = df_log[variable].value_counts()
            df_log = df_log.loc[df_log[variable].isin(counts.index[counts >= min_counts].values)]

    # Convert categorical data using one-hot encoding
    df_log = pd.get_dummies(data=df_log, columns=categorical_vars, drop_first=False)
    df_log = df_log.dropna()

    # Drop an option from each category in order to avoid singularity
    drop_firsts = {"hoh_gender": "male", "union_name": "jalia palong", "hoh_marital_married": 1}

    for categorical_var in categorical_vars:
        drop_column = categorical_var+"_"+str(drop_firsts[categorical_var])
        df_log = df_log.drop(columns=[drop_column])

    # Split into training and testing sets
    X = df_log.loc[:, df_log.columns != dependent_variable]
    y = df_log.loc[:, df_log.columns == dependent_variable]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    columns = X_train.columns

    """
    Run the model using the sklearn package
    """
    # Fit the model
    clf = LogisticRegression(random_state=0).fit(X_train, y_train)

    # Run predictions on the testing set and generate a score and confusion matrix
    y_pred = clf.predict(X_test)
    cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
    score = clf.score(X_test, y_test)

    # Find the coefficients of the model
    coefficients = pd.DataFrame(dict(zip(X_train.columns,clf.coef_[0])),index=[0]).T
    coefficients = coefficients.rename(columns={0:"Coefficients"}).sort_values(by="Coefficients", ascending=False)

    """
    Run the model using the statsmodels package
    """
    # Train and fit the model
    logit_model = sm.Logit(y_train, sm.add_constant(X_train))
    result = logit_model.fit()

    # Write the results summary to a file
    summary = result.summary()
    print(dependent_variable)
    print(len(df_log))
    print(summary)
    #f = open("results/"+dependent_variable.replace(" ","_")+"_summary.txt", "w")
    #f.write(str(summary))
    #f.close()

    # Extract the significant coefficients
    pvalues = result.pvalues.reset_index().rename(columns={"index":"parameter", 0:"pvalues"})
    coeffs = result.params.reset_index().rename(columns={"index":"parameter", 0:"coeffs"})
    df_results = coeffs.merge(pvalues, on="parameter")
    df_results = df_results.loc[df_results["pvalues"]<=0.05]
    df_results = df_results.reindex(df_results["coeffs"].abs().sort_values(ascending=False).index)
    df_results[["coeffs", "pvalues"]] = df_results[["coeffs", "pvalues"]].round(2)
    #df_results.to_csv("results/"+dependent_variable.replace(" ","_")+"results.csv", index=False)
    print(df_results)
    print()
