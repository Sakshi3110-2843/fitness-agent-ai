
# CALORIE SAFETY CHECK
def check_calorie_safety(calories: float):
    if calories < 1200:
        raise ValueError("❌ Unsafe: Calories below 1200 kcal")

    if calories > 4000:
        raise ValueError("❌ Unrealistic: Calories too high")

    return calories


# BMI SAFETY CHECK
def check_bmi_category(bmi: float):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"


# DEFICIT SAFETY CHECK
def check_deficit_safety(tdee: float, calories: float):
    deficit = tdee - calories

    if deficit > 1000:
        raise ValueError("❌ Too aggressive deficit (over 1000 kcal)")

    return deficit


# PROGRESS RATE SAFETY
def check_weekly_weight_loss(rate: float):
    if rate > 1.0:
        raise ValueError("❌ Unsafe weight loss rate (>1 kg/week)")

    return rate