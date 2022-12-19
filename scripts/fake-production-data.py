"""Generate fake iris-dataset-style production data to simulate data-drift detection."""

import argparse
import random

import pandas as pd


def fake_flower_data():
    """Generate fake flower data."""

    flower_data = {
        "sepal_length": round(random.uniform(4.3, 7.9), 1),
        "sepal_width": round(random.uniform(2.0, 4.4), 1),
        "petal_length": round(random.uniform(1.0, 6.9), 1),
        "petal_width": round(random.uniform(0.1, 2.5), 1),
    }

    return flower_data


def main(number_of_samples: int, output_file: str):
    df = pd.DataFrame([fake_flower_data() for _ in range(number_of_samples)])
    df.to_csv(output_file, index=False, header=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Generate fake iris-dataset-style production data to simulate
                    data-drift detection.""",
    )
    parser.add_argument("-n", "--number-of-samples", type=int, default=100)
    parser.add_argument(
        "-o", "--output-file", type=str, default="fake-production-data.csv"
    )

    args = parser.parse_args()

    main(args.number_of_samples, args.output_file)
