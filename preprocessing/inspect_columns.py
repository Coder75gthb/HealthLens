import pandas as pd

diabetes = pd.read_csv("data/raw/diabetes.csv")
heart = pd.read_csv("data/raw/heart.csv")

print("DIABETES COLUMNS:\n")
print(diabetes.columns.tolist())

print("\n----------------------\n")

print("HEART DISEASE COLUMNS:\n")
print(heart.columns.tolist())
