import time
from crewai import Crew
from tasks import plan_task, review_task
from tools import *
from guardrails import *

user_profile = {
    "age": 27,
    "gender": "female",
    "height": 155,
    "weight": 85,
    "goal_weight": 65,
    "activity_level": "very_active",
    "diet_type": "vegetarian"
}

bmi = calculate_bmi(user_profile["weight"], user_profile["height"])
bmr = calculate_bmr(
    user_profile["weight"],
    user_profile["height"],
    user_profile["age"],
    user_profile["gender"]
)
tdee = calculate_tdee(bmr, user_profile["activity_level"])
calories = calculate_calorie_target(tdee)

check_calorie_safety(calories)
check_deficit_safety(tdee, calories)

macros = calculate_macros(calories)

print("\n=== USER METRICS ===")
print("BMI:", bmi)
print("Category:", check_bmi_category(bmi))
print("TDEE:", tdee)
print("Calories:", calories)
print("Macros:", macros)

# Tasks
p_task = plan_task(user_profile, calories, macros)

r_task = review_task(user_profile, weight_lost=None)  # change weight_lost on weekly check-ins
r_task.context = [p_task]

crew = Crew(
    agents=[p_task.agent, r_task.agent],
    tasks=[p_task, r_task],
    verbose=True
)

print("\n🚀 Running AI Fitness System...\n")

result = crew.kickoff()

print("\n=== FINAL OUTPUT ===\n")
print(result)