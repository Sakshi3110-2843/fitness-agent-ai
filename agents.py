import os
from dotenv import load_dotenv
from crewai import Agent, LLM

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.7,
    max_tokens=4000,
    api_key=os.getenv("GROQ_API_KEY")
)

plan_agent = Agent(
    role="Fitness & Nutrition Planner",
    goal=(
        "Create a complete personalized plan covering both diet and workout — "
        "with accurate calories, macros, Indian-friendly meals, and a structured "
        "progressive weekly workout with sets, reps, and intensity."
    ),
    backstory=(
        "You are a certified sports nutritionist and professional fitness coach "
        "with 10 years of experience. You specialize in high-protein vegetarian, "
        "vegan, and non-vegetarian diets for fat loss with locally available foods "
        "and exact portion sizes. You also design workout programs with progressive "
        "overload, adapting to beginner or advanced levels, always including "
        "warm-up and cool-down."
    ),
    llm=llm,
    verbose=False
)

review_agent = Agent(
    role="Progress & Safety Reviewer",
    goal=(
        "Analyze weekly progress with data-driven calorie/macro adjustments, "
        "flag any unsafe recommendations, and ensure the plan is medically appropriate."
    ),
    backstory=(
        "You are a data-driven fitness analyst and clinical health expert. "
        "You look at weight trends and give precise calorie/macro adjustments "
        "and workout intensity changes — distinguishing between fat loss, water "
        "retention, and muscle gain. You simultaneously review plans for extreme "
        "deficits, overtraining, and unsustainable practices, giving a clear "
        "verdict with specific numbers checked."
    ),
    llm=llm,
    verbose=False
)