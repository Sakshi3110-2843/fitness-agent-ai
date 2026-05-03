import time
import streamlit as st
from crewai import Crew
from tasks import plan_task, review_task
from tools import *
from guardrails import *

st.set_page_config(page_title="AI Fitness Coach", layout="wide")

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; max-width: 1100px; }

    .hero {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid #7c3aed33;
    }
    .hero h1 { font-size: 2.4rem; color: #fff; margin: 0; }
    .hero p  { color: #a78bfa; font-size: 1.05rem; margin-top: 0.4rem; }

    
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #3b1f6e, #1e3a6e) !important;
        border: 1px solid #7c3aed88 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        text-align: center !important;
    }
    [data-testid="stMetric"] label,
    [data-testid="stMetricLabel"] p,
    [data-testid="stMetricLabel"] {
        color: #c4b5fd !important;
        font-size: 0.78rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] > div {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricDelta"],
    [data-testid="stMetricDelta"] > div {
        color: #a78bfa !important;
        font-size: 0.85rem !important;
    }

    /* ── MEAL TABLE — full dark theme ── */
    .meal-table-wrap {
        overflow-x: auto;
        border-radius: 10px;
        background: #0f0f1e;
        padding: 1rem;
    }
    .meal-table-wrap table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.82rem;
        background: #0f0f1e;
    }
    .meal-table-wrap thead {
        background: linear-gradient(90deg, #7c3aed, #4f46e5);
    }
    .meal-table-wrap th {
        color: #ffffff !important;
        padding: 12px 10px !important;
        text-align: left !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        border: 1px solid #5d3fd3 !important;
        background: transparent !important;
    }
    .meal-table-wrap td {
        padding: 10px !important;
        border: 1px solid #2a2a4e !important;
        color: #e2e8f0 !important;
        background: #1a1a2e !important;
    }
    .meal-table-wrap tr:nth-child(even) td {
        background: #151530 !important;
    }
    .meal-table-wrap tbody tr:hover td {
        background: #2a1a4e !important;
        cursor: default;
    }

    
    .workout-day {
        background: linear-gradient(135deg, #1e1e2e, #1a1a3e);
        border-left: 4px solid #7c3aed;
        border-radius: 10px;
        padding: 1rem 1.3rem;
        margin-bottom: 1rem;
        color: #e2e8f0;
        line-height: 1.7;
    }
    .workout-day b, .workout-day strong { color: #a78bfa; font-size: 1rem; }

    
    .progress-point {
        background: #1a1a2e;
        border-left: 3px solid #06b6d4;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        margin-bottom: 0.6rem;
        color: #e2e8f0;
        font-size: 0.92rem;
    }

    
    .safety-pass {
        background: linear-gradient(135deg, #052e16, #14532d);
        border: 1px solid #22c55e55;
        border-radius: 10px;
        padding: 0.8rem 1.2rem;
        margin-bottom: 0.6rem;
        color: #86efac;
        font-size: 0.92rem;
    }
    .safety-fail {
        background: linear-gradient(135deg, #2d0a0a, #450a0a);
        border: 1px solid #ef444455;
        border-radius: 10px;
        padding: 0.8rem 1.2rem;
        margin-bottom: 0.6rem;
        color: #fca5a5;
        font-size: 0.92rem;
    }

    
    .delta-card {
        background: linear-gradient(135deg, #1e1e3a, #0f3460);
        border: 1px solid #7c3aed44;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .delta-label { color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; }
    .delta-value { color: #fff; font-size: 1.6rem; font-weight: 700; margin: 0.2rem 0; }
    .delta-good  { color: #4ade80; font-size: 0.9rem; }
    .delta-bad   { color: #f87171; font-size: 0.9rem; }

    
    .disabled-box {
        background: #1a1a2e;
        border: 1px dashed #4f46e5;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        color: #94a3b8;
        font-size: 0.95rem;
    }

    
    [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="hero">
    <h1>🏋️ AI Fitness Coach</h1>
    <p>Personalized meal plans, workouts & progress tracking — powered by AI</p>
</div>
""", unsafe_allow_html=True)

IMAGES = {
    "meal":     "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=1200&q=80",
    "workout":  "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=1200&q=80",
    "progress": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=1200&q=80",
    "safety":   "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=1200&q=80",
}


with st.form("user_form"):
    st.subheader("👤 Your Details")
    col1, col2 = st.columns(2)
    with col1:
        age         = st.number_input("Age", 18, 60, 27)
        gender      = st.selectbox("Gender", ["male", "female"])
        activity    = st.selectbox("Activity Level", ["low", "moderate", "active", "very_active"])
    with col2:
        height      = st.number_input("Height (cm)", 140, 200, 155)
        weight      = st.number_input("Current Weight (kg)", 40, 150, 85)
        goal_weight = st.number_input("Goal Weight (kg)", 40, 150, 65)
    diet_type = st.selectbox("Diet Type", ["vegetarian", "non-vegetarian", "vegan"])
    submit = st.form_submit_button("🚀 Generate My Plan")


st.markdown("---")
st.subheader("📈 Weekly Progress Tracking")
tracking_enabled = st.checkbox("Track this week's progress")

progress_data = None
if tracking_enabled:
    wcol1, wcol2 = st.columns(2)
    with wcol1:
        st.markdown("**⚖️ Weight (kg)**")
        weight_prev = st.number_input("Last week",  40.0, 200.0, float(weight), step=0.1, key="wp")
        weight_curr = st.number_input("This week",  40.0, 200.0, float(weight), step=0.1, key="wc")
    with wcol2:
        st.markdown("**📏 Waist (inches)**")
        waist_prev = st.number_input("Last week ",  20.0, 60.0, 32.0, step=0.1, key="wap")
        waist_curr = st.number_input("This week ",  20.0, 60.0, 32.0, step=0.1, key="wac")
    progress_data = {
        "weight_prev": weight_prev,
        "weight_curr": weight_curr,
        "waist_prev":  waist_prev,
        "waist_curr":  waist_curr,
    }



def extract_section(text, start_marker, end_marker=None):
    if start_marker not in text:
        return ""
    after = text.split(start_marker, 1)[1]
    if end_marker and end_marker in after:
        return after.split(end_marker, 1)[0].strip()
    return after.strip()


def smart_split_plan(raw):
    meal, workout = "", ""

    # 1. Exact markers
    if "<<<MEAL_PLAN_START>>>" in raw and "<<<WORKOUT_START>>>" in raw:
        meal    = extract_section(raw, "<<<MEAL_PLAN_START>>>", "<<<WORKOUT_START>>>")
        workout = extract_section(raw, "<<<WORKOUT_START>>>")
        return meal, workout

    # 2. HTML table detection
    if "<table" in raw.lower():
        table_start = raw.lower().index("<table")
        table_end   = raw.lower().index("</table>") + len("</table>")
        meal    = raw[table_start:table_end]
        workout = raw[table_end:].strip()
        return meal, workout

    
    for kw in ["**Day 1", "Day 1 —", "Day 1:"]:
        if kw in raw:
            parts   = raw.split(kw, 1)
            meal    = parts[0].strip()
            workout = kw + parts[1] if len(parts) > 1 else ""
            return meal, workout

    return raw, ""


def smart_split_review(raw):
    progress, safety = "", ""

    
    if "<<<PROGRESS_START>>>" in raw and "<<<SAFETY_START>>>" in raw:
        progress = extract_section(raw, "<<<PROGRESS_START>>>", "<<<SAFETY_START>>>")
        safety   = extract_section(raw, "<<<SAFETY_START>>>")
        return progress, safety

    
    lines = raw.splitlines()
    prog_lines, safe_lines = [], []
    in_safety = False
    for line in lines:
        if not in_safety and (line.strip().startswith("✅") or line.strip().startswith("⚠️")):
            in_safety = True
        (safe_lines if in_safety else prog_lines).append(line)
    return "\n".join(prog_lines).strip(), "\n".join(safe_lines).strip()


def render_workout(text):
    if not text or not text.strip():
        st.warning("⚠️ Workout data wasn't returned. Try regenerating the plan.")
        return
    st.image(IMAGES["workout"], use_container_width=True)
    days, current = [], []
    for line in text.splitlines():
        stripped = line.strip()
        if (stripped.startswith("**Day") or stripped.startswith("Day ")) and current:
            days.append("\n".join(current))
            current = [line]
        else:
            current.append(line)
    if current:
        days.append("\n".join(current))
    for day in days:
        if day.strip():
            st.markdown(
                f'<div class="workout-day">{day.strip().replace(chr(10), "<br>")}</div>',
                unsafe_allow_html=True
            )


def render_progress(text):
    if not text.strip():
        return
    for line in text.splitlines():
        line = line.strip()
        if line.startswith(("•", "-", "*", "Point")):
            st.markdown(f'<div class="progress-point">{line}</div>', unsafe_allow_html=True)
        elif line:
            st.markdown(f'<p style="color:#94a3b8;font-size:0.88rem;">{line}</p>', unsafe_allow_html=True)


def render_safety(text):
    if not text or not text.strip():
        st.info("Safety data not available.")
        return
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("✅"):
            st.markdown(f'<div class="safety-pass">{line}</div>', unsafe_allow_html=True)
        elif line.startswith("⚠️"):
            st.markdown(f'<div class="safety-fail">{line}</div>', unsafe_allow_html=True)



if submit:
    user_profile = {
        "age": age, "gender": gender, "height": height,
        "weight": weight, "goal_weight": goal_weight,
        "activity_level": activity, "diet_type": diet_type
    }

    bmi      = calculate_bmi(weight, height)
    bmr      = calculate_bmr(weight, height, age, gender)
    tdee     = calculate_tdee(bmr, activity)
    calories = calculate_calorie_target(tdee)
    macros   = calculate_macros(calories)

    try:
        check_calorie_safety(calories)
        check_deficit_safety(tdee, calories)
    except ValueError as e:
        st.error(str(e))
        st.stop()

    
    st.markdown("## 📊 Your Metrics")
    c1, c2, c3 = st.columns(3)
    c1.metric("BMI",      round(bmi, 2),  check_bmi_category(bmi))
    c2.metric("TDEE",     round(tdee))
    c3.metric("Calories", round(calories))
    st.success(f"Protein: {macros['protein_g']}g | Carbs: {macros['carbs_g']}g | Fats: {macros['fats_g']}g")

    
    if tracking_enabled and progress_data:
        weight_delta = round(progress_data["weight_prev"] - progress_data["weight_curr"], 2)
        waist_delta  = round(progress_data["waist_prev"]  - progress_data["waist_curr"],  2)
        st.markdown("### 📉 This Week's Changes")
        d1, d2 = st.columns(2)
        with d1:
            w_class = "delta-good" if weight_delta >= 0 else "delta-bad"
            w_sign  = "▼" if weight_delta > 0 else ("▲" if weight_delta < 0 else "→")
            st.markdown(f"""
            <div class="delta-card">
                <div class="delta-label">Weight</div>
                <div class="delta-value">{progress_data['weight_curr']} kg</div>
                <div class="{w_class}">{w_sign} {abs(weight_delta)} kg from last week</div>
            </div>""", unsafe_allow_html=True)
        with d2:
            wa_class = "delta-good" if waist_delta >= 0 else "delta-bad"
            wa_sign  = "▼" if waist_delta > 0 else ("▲" if waist_delta < 0 else "→")
            st.markdown(f"""
            <div class="delta-card">
                <div class="delta-label">Waist</div>
                <div class="delta-value">{progress_data['waist_curr']} in</div>
                <div class="{wa_class}">{wa_sign} {abs(waist_delta)} in from last week</div>
            </div>""", unsafe_allow_html=True)

    
    p_task = plan_task(user_profile, calories, macros)
    r_task = review_task(user_profile, progress_data=progress_data)
    r_task.context = [p_task]

    crew = Crew(
        agents=[p_task.agent, r_task.agent],
        tasks=[p_task, r_task],
        verbose=False
    )

    with st.spinner("🤖 Generating your personalized fitness plan... (this may take ~30s)"):
        try:
            # Auto-retry on rate limit
            max_retries = 3
            result = None

            for attempt in range(max_retries):
                try:
                    result = crew.kickoff()
                    break  # success — exit retry loop
                except Exception as e:
                    if "rate_limit_exceeded" in str(e) or "RateLimitError" in str(e):
                        wait_time = 30 * (attempt + 1)  # 30s, 60s, 90s
                        st.warning(f"⏳ Rate limit hit — waiting {wait_time}s before retrying... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(wait_time)
                    else:
                        raise e  # non-rate-limit error — raise immediately

            if result is None:
                st.error("❌ Rate limit exceeded after 3 attempts. Please wait a minute and try again.")
                st.stop()

            outputs = result.tasks_output
            time.sleep(12)

            plan_raw   = outputs[0].raw
            review_raw = outputs[1].raw

            meal_content,     workout_content  = smart_split_plan(plan_raw)
            progress_content, safety_content   = smart_split_review(review_raw)

            st.success("✅ Your plan is ready!")

            tab1, tab2, tab3, tab4 = st.tabs([
                "🥗 Meal Plan", "💪 Workout", "📈 Progress", "🛡️ Safety"
            ])

            with tab1:
                st.image(IMAGES["meal"], use_container_width=True)
                st.subheader("🥗 7-Day Meal Plan")
                st.markdown(
                    f'<div class="meal-table-wrap">{meal_content if meal_content else plan_raw}</div>',
                    unsafe_allow_html=True
                )

            with tab2:
                st.subheader("💪 7-Day Workout Plan")
                render_workout(workout_content)

            with tab3:
                st.image(IMAGES["progress"], use_container_width=True)
                st.subheader("📈 Progress Insights")
                if tracking_enabled and progress_data:
                    render_progress(progress_content if progress_content else review_raw)
                else:
                    st.markdown("""
                    <div class="disabled-box">
                        📊 Progress tracking is disabled.<br><br>
                        Check <strong>Track this week's progress</strong> above
                        and enter your weight & waist to get personalised adjustments.
                    </div>""", unsafe_allow_html=True)

            with tab4:
                st.image(IMAGES["safety"], use_container_width=True)
                st.subheader("🛡️ Safety Review")
                render_safety(safety_content if safety_content else review_raw)

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")