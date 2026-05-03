from pydantic import BaseModel

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

# 2. BMR CALCULATOR (Mifflin-St Jeor)
def calculate_bmr(weight: float, height: float, age: int, gender: str) -> float:
    if gender.lower() == "female":
        return (10 * weight) + (6.25 * height) - (5 * age) - 161
    else:
        return (10 * weight) + (6.25 * height) - (5 * age) + 5


# 3. TDEE CALCULATOR
def calculate_tdee(bmr: float, activity_level: str) -> float:
    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }

    multiplier = activity_multipliers.get(activity_level.lower(), 1.55)
    return bmr * multiplier

# 4. CALORIE TARGET (DEFICIT)
def calculate_calorie_target(tdee: float, deficit: int = 500) -> float:
    return tdee - deficit

# 5. SAFETY GUARDRAIL
def validate_calories(calories: float):
    if calories < 1200:
        raise ValueError("Unsafe calorie recommendation: below 1200 kcal")
    return True


# 6. MACRO SPLIT CALCULATOR
def calculate_macros(calories: float):
    protein = calories * 0.30 / 4   # 30% protein
    carbs = calories * 0.40 / 4     # 40% carbs
    fats = calories * 0.30 / 9      # 30% fats

    return {
        "protein_g": round(protein),
        "carbs_g": round(carbs),
        "fats_g": round(fats)
    }