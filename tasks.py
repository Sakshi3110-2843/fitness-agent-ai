from crewai import Task
from agents import plan_agent, review_agent


def plan_task(user_profile, calories, macros):
    diet_type = user_profile.get("diet_type", "vegetarian")
    activity = user_profile.get("activity_level", "moderate")

    if activity == "low":
        level_note = "Beginner level. Start with basic exercises, 3 workout days."
    elif activity == "moderate":
        level_note = "Intermediate level. 4 workout days with moderate intensity."
    else:
        level_note = "Advanced level. 5-6 workout days with progressive overload."

    return Task(
        description=(
            f"""
            You are creating a complete fitness and nutrition plan for this user.

            User Profile: {user_profile}
            Age: {user_profile['age']} | Gender: {user_profile['gender']}
            Weight: {user_profile['weight']}kg | Goal Weight: {user_profile['goal_weight']}kg
            Activity Level: {activity} — {level_note}
            Diet Type: {diet_type}
            Daily Calorie Target: {round(calories)} kcal
            Macros: Protein {macros['protein_g']}g | Carbs {macros['carbs_g']}g | Fats {macros['fats_g']}g

            Your response MUST follow this exact structure using these exact markers:

            
            [HTML table with these exact columns: Day | Meal | Food Item | Portion Size | Calories | Protein(g) | Carbs(g) | Fats(g)]

            Rules for meal plan:
            - Include Breakfast, Lunch, Dinner, Snack for every day
            - Use specific food names (e.g. "200g paneer tikka" not "protein source")
            - Vary meals across all 7 days — zero repetition
            - Every meal must have a clear protein source
            - Strictly follow diet type: {diet_type}
            - Use realistic Indian-friendly foods and portions
            - HTML table only, no intro text

            
            [Day-by-day workout plan]

            Rules for workout:
            - Use this exact format for each day:
              **Day X — Focus Area**
              - Warm-up (5 min): specific activity
              - Exercise 1: name — sets x reps
              - Exercise 2: name — sets x reps
              - Exercise 3: name — sets x reps
              - Exercise 4: name — sets x reps
              - Cool-down (5 min): specific stretches
            - Rest days must say exactly: "Active Recovery: 20 min walk + full body stretching"
            - Mix strength, cardio and HIIT based on activity level
            - Progressive overload for advanced users
            - Beginner-friendly exercises for low activity users

            STRICT RULES:
            - Do NOT put any meal content after <<<WORKOUT_START>>>
            - Do NOT put any workout content after <<<MEAL_PLAN_START>>>
            - Do NOT add any text before <<<MEAL_PLAN_START>>>
            - Produce both sections completely, do not truncate
            """
        ),
        agent=plan_agent,
        expected_output=(
            "<<<MEAL_PLAN_START>>> followed by complete 7-day HTML meal table, "
            "then <<<WORKOUT_START>>> followed by complete 7-day workout plan."
        )
    )


def review_task(user_profile, progress_data=None):
    gender = user_profile.get("gender", "male").lower()
    min_calories = 1200 if gender == "female" else 1500

    if progress_data is None:
        progress_scenario = "This is the user's first week — no progress data yet."
        progress_note = (
            "Give general baseline tips: ideal deficit to aim for, "
            "what to track, and what to expect in week 1."
        )
    else:
        weight_prev  = progress_data["weight_prev"]
        weight_curr  = progress_data["weight_curr"]
        waist_prev   = progress_data["waist_prev"]
        waist_curr   = progress_data["waist_curr"]
        weight_delta = round(weight_prev - weight_curr, 2)
        waist_delta  = round(waist_prev - waist_curr, 2)

        weight_line = (
            f"Lost {weight_delta}kg" if weight_delta > 0
            else f"Gained {abs(weight_delta)}kg" if weight_delta < 0
            else "No weight change"
        )
        waist_line = (
            f"Waist reduced by {waist_delta} inches" if waist_delta > 0
            else f"Waist increased by {abs(waist_delta)} inches" if waist_delta < 0
            else "No waist change"
        )

        progress_scenario = (
            f"Weight: {weight_prev}kg → {weight_curr}kg ({weight_line}). "
            f"Waist: {waist_prev} inches → {waist_curr} inches ({waist_line})."
        )
        progress_note = (
            "Analyze both weight and waist trends. "
            "Target is 0.5–1kg/week fat loss and gradual waist reduction. "
            "If weight dropped but waist didn't, may be water loss. "
            "If waist dropped but weight didn't, likely fat loss with muscle gain. "
            "Give corrective or reinforcing actions based on both metrics."
        )

    return Task(
        description=(
            f"""
            You are reviewing this user's fitness plan for progress and safety.

            User Profile: {user_profile}
            Gender: {gender}
            Weekly Update: {progress_scenario}
            Analysis Note: {progress_note}

            Your response MUST follow this exact structure using these exact markers:

            
            [Exactly 5 bullet points]

            • Point 1: Calorie adjustment — give exact new daily calorie number
            • Point 2: Macro adjustment — give exact new grams for protein/carbs/fats
            • Point 3: Workout change — name a specific exercise or intensity tweak
            • Point 4: Lifestyle tip — sleep hours, water intake (in litres), or stress management
            • Point 5: Mindset/consistency tip — practical and motivating

            Rules for progress:
            - Base advice on BOTH weight and waist changes where available
            - Numbers only, no vague advice
            - No meal plans in this section
            - Max 200 words

           
            [Exactly 4 safety checks]

            ✅ or ⚠️ Minimum Calories: Are daily calories >= {min_calories} kcal? [verdict with numbers]
            ✅ or ⚠️ Calorie Deficit: Is the deficit <= 500 kcal below TDEE? [verdict with numbers]
            ✅ or ⚠️ Rest Days: Are there at least 2 rest/recovery days per week? [verdict with numbers]
            ✅ or ⚠️ Sustainability: Is this plan realistic for 3+ months? [verdict]

            Rules for safety:
            - One line per check, no extra explanation
            - Max 100 words
            - Flag issues clearly with ⚠️ if unsafe

            STRICT RULES:
            - Do NOT put safety content after <<<PROGRESS_START>>>
            - Do NOT put progress content after <<<SAFETY_START>>>
            - Do NOT add any text before <<<PROGRESS_START>>>
            - Produce both sections completely
            """
        ),
        agent=review_agent,
        expected_output=(
            "<<<PROGRESS_START>>> followed by 5 bullet points with exact numbers, "
            "then <<<SAFETY_START>>> followed by 4 safety checks with ✅ or ⚠️ verdicts."
        )
    )