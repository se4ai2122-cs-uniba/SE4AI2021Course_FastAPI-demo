"""Sample training script"""

import json
import pickle
from pathlib import Path
from typing import List

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.svm import SVC

MODELS_DIR = Path("models/")
model_wrappers_list: List[dict] = []


# ================ #
# Data preparation #
# ================ #


def load_data():
    """Load data and split it into train and test sets"""

    # Load data
    Iris_data = load_iris()

    # Split data
    Xtrain, Xtest, Ytrain, Ytest = train_test_split(
        Iris_data.data,  # pylint: disable=no-member
        Iris_data.target,  # pylint: disable=no-member
        test_size=0.3,
        random_state=4,
    )

    return Xtrain, Xtest, Ytrain, Ytest


# ================== #
# LogisticRegression #
# ================== #


def train_log_reg_model(Xtrain, Ytrain):
    """Train a Logistic Regression model"""

    print("Creating logistic regression model...")

    # Define the Logistic Regression model
    LR_parameters = {
        "C": 0.1,
        "max_iter": 21,
        "fit_intercept": True,
        "solver": "liblinear",
        "random_state": 0,
    }
    LR_model = LogisticRegression(**LR_parameters)

    # Train the Model
    LR_model.fit(Xtrain, Ytrain)

    # Evaluate model accuracy by cross-validation
    LR_accuracies = cross_val_score(estimator=LR_model, X=Xtrain, y=Ytrain, cv=10)
    LR_metrics = {"accuracy": LR_accuracies.mean()}

    # Wrap the trained model in a Model namedtuple and append it to the model list
    LR_model_dict = {
        "type": "LogisticRegression",
        "params": LR_parameters,
        "metrics": LR_metrics,
    }
    print("\nLogistic regression model created.\n")
    print(json.dumps(LR_model_dict, indent=4))

    LR_model_dict["model"] = LR_model
    model_wrappers_list.append(LR_model_dict)


# =============================== #
# C-Support Vector Classification #
# =============================== #


def train_svc_model(Xtrain, Ytrain):
    """Train a SVC model"""

    print("\n\nCreating SVC model...")

    # Define the SVC model
    SVC_parameters = {"kernel": "linear", "random_state": 0}

    SVC_model = SVC(**SVC_parameters)

    # Train the Model
    SVC_model.fit(Xtrain, Ytrain)

    # Evaluate model accuracy by cross-validation
    SVC_accuracies = cross_val_score(estimator=SVC_model, X=Xtrain, y=Ytrain, cv=10)
    SVC_metrics = {"accuracy": SVC_accuracies.mean()}

    # Wrap the trained model in a Model namedtuple and append it to the model list
    SVC_model_dict = {
        "type": "SVC",
        "params": SVC_parameters,
        "metrics": SVC_metrics,
    }
    print("\nSVC model created.\n")
    print(json.dumps(SVC_model_dict, indent=4))

    SVC_model_dict["model"] = SVC_model
    model_wrappers_list.append(SVC_model_dict)


# ============= #
# Serialization #
# ============= #


def serialize_models():
    """Serialize the trained models"""

    print("\nSerializing model wrappers...")

    for wrapped_model in model_wrappers_list:

        pkl_filename = f"{wrapped_model['type']}_model.pkl"
        pkl_path = MODELS_DIR / pkl_filename

        with open(pkl_path, "wb") as file:
            pickle.dump(wrapped_model, file)

    print("Serializing completed.")


# ============ #
# Main program #
# ============ #

if __name__ == "__main__":
    Xtrain, Xtest, Ytrain, Ytest = load_data()

    train_log_reg_model(Xtrain, Ytrain)
    train_svc_model(Xtrain, Ytrain)

    serialize_models()
