# preprocessing/imputation.py

def add_missing_flags(inputs: dict, optional_features: list) -> dict:
    """
    Adds binary flags indicating which optional features are missing.
    """
    flagged = inputs.copy()

    for feature in optional_features:
        flag_name = f"{feature}_missing"
        flagged[flag_name] = 1 if flagged.get(feature) is None else 0

    return flagged


def impute_with_median(inputs: dict, medians: dict) -> dict:
    """
    Imputes missing optional values using precomputed medians.
    Mandatory features should never reach here as missing.
    """
    imputed = inputs.copy()

    for feature, median in medians.items():
        if imputed.get(feature) is None:
            imputed[feature] = median

    return imputed
