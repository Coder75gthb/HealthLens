import pandas as pd

from preprocessing.column_mapping import (
    DIABETES_COLUMN_MAP,
    HEART_COLUMN_MAP
)
from preprocessing.schema import OPTIONAL_FEATURES


def build_dataset(raw_path, column_map):
    df = pd.read_csv(raw_path)

    # Keep only mapped columns
    df = df[list(column_map.keys())]

    # Rename columns
    df = df.rename(columns=column_map)

    return df


if __name__ == "__main__":
    diabetes = build_dataset(
        "data/raw/diabetes.csv",
        DIABETES_COLUMN_MAP
    )

    heart = build_dataset(
        "data/raw/heart.csv",
        HEART_COLUMN_MAP
    )

    diabetes.to_csv("data/processed/diabetes_features.csv", index=False)
    heart.to_csv("data/processed/heart_features.csv", index=False)
