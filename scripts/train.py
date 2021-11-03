"""Sample training script"""

# Import Required packages
# -------------------------

# Import the Logistic Regression Module from Scikit Learn
from sklearn.linear_model import LogisticRegression

# Import the IRIS Dataset to be used in this Kernel
from sklearn.datasets import load_iris

# Load the Module to split the Dataset into Train & Test
from sklearn.model_selection import train_test_split

# Import pickle Package
import pickle

# Load the data
Iris_data = load_iris()

# Split data
Xtrain, Xtest, Ytrain, Ytest = train_test_split(
    Iris_data.data, Iris_data.target, test_size=0.3, random_state=4
)

# Define the Model
LR_Model = LogisticRegression(
    C=0.1, max_iter=20, fit_intercept=True, solver="liblinear"
)

# Train the Model
LR_Model.fit(Xtrain, Ytrain)

# Save the model to file in the current working directory
Pkl_Filename = "../models/Pickle_RL_Model.pkl"

with open(Pkl_Filename, "wb") as file:
    pickle.dump(LR_Model, file)
