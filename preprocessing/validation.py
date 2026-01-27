# preprocessing/validation.py

class ValidationError(Exception):
    """Raised when user input is medically invalid."""
    pass


def validate_range(name, value, min_val, max_val):
    if value is None:
        return
    if not (min_val <= value <= max_val):
        raise ValidationError(
            f"{name} must be between {min_val} and {max_val}. Got {value}."
        )


def validate_user_inputs(inputs: dict):
    """
    inputs: dictionary of user-provided values
    """

    validate_range("Age", inputs.get("age"), 1, 100)
    validate_range("Height (cm)", inputs.get("height"), 120, 220)
    validate_range("Weight (kg)", inputs.get("weight"), 30, 200)
    validate_range("BMI", inputs.get("bmi"), 10, 60)

    validate_range("Systolic BP", inputs.get("systolic_bp"), 80, 200)
    validate_range("Diastolic BP", inputs.get("diastolic_bp"), 40, 130)

    validate_range("Blood Sugar", inputs.get("blood_sugar"), 50, 400)
    validate_range("Cholesterol", inputs.get("cholesterol"), 100, 400)
