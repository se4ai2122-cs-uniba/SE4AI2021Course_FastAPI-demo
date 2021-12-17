"""Data validation script (uses Great Expectations)"""

import great_expectations as ge
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris

# Load Iris data into a Great Expectations dataframe
iris = load_iris()
dataframe = pd.DataFrame(
    data=np.c_[iris["data"], iris["target"]], columns=iris["feature_names"] + ["target"]
)
df = ge.dataset.PandasDataset(dataframe)

# Presence of features
expected_columns = [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)",
    "target",
]
df.expect_table_columns_to_match_ordered_list(column_list=expected_columns)

# No null values
df.expect_column_values_to_not_be_null(column="sepal length (cm)")
df.expect_column_values_to_not_be_null(column="sepal width (cm)")
df.expect_column_values_to_not_be_null(column="petal length (cm)")
df.expect_column_values_to_not_be_null(column="petal width (cm)")
df.expect_column_values_to_not_be_null(column="target")

# Type
df.expect_column_values_to_be_of_type(column="sepal length (cm)", type_="float")
df.expect_column_values_to_be_of_type(column="sepal width (cm)", type_="float")
df.expect_column_values_to_be_of_type(column="petal length (cm)", type_="float")
df.expect_column_values_to_be_of_type(column="petal width (cm)", type_="float")
df.expect_column_values_to_be_of_type(column="target", type_="int")
