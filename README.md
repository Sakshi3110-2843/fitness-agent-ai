# 🏋️ AI Fitness Coach — Your Personal AI-Powered Health Partner

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-purple?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-LLM-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> **Stop guessing. Start transforming.**
> AI Fitness Coach builds your complete personalized fitness plan in seconds — meal plan, workout schedule, progress analysis and safety review, all in one place.

## ✨ What Makes This Different?

| Feature | What You Get |
|---|---|
| 🥗 **Smart Meal Planning** | 7-day Indian-friendly diet with exact calories, protein, carbs & fats |
| 💪 **Adaptive Workouts** | Progressive plans tailored to beginner, intermediate or advanced level |
| 📈 **Progress Intelligence** | Weekly weight + waist analysis with exact number-based adjustments |
| 🛡️ **Safety First** | Automated checks — no extreme deficits, no overtraining, no unsafe plans |
| ⚡ **Powered by Llama 3.3** | State-of-the-art LLM running on Groq's ultra-fast inference engine |

## 🖥️ App Preview

> 📸 *Screenshots coming soon — run it locally to see the full experience!*

## 🧠 How It Works
You fill the form
↓
AI calculates your BMI, BMR, TDEE & Macros
↓
Agent 1 → Builds your 7-day Meal Plan + Workout Plan
↓
Agent 2 → Reviews your Progress + Safety checks
↓
You get a complete, personalized fitness plan

## 🛠️ Tech Stack
Frontend     →  Streamlit
AI Agents    →  CrewAI (2 agents, 2 tasks)
LLM          →  Groq — llama-3.3-70b-versatile
Calculations →  Custom BMI / BMR / TDEE / Macro engine
Safety       →  Custom guardrails layer
Env Mgmt     →  python-dotenv

## 🚀 Get Started in 5 Minutes

### Step 1 — Clone the repo
```bash
git clone https://github.com/Sakshi3110-2843/fitness-agent-ai.git
cd fitness-agent-ai
```

### Step 2 — Set up virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Add your Groq API key
Create a `.env` file in the root folder:
GROQ_API_KEY=your_groq_api_key_here
👉 Get your free key at [console.groq.com](https://console.groq.com)

### Step 5 — Launch
```bash
streamlit run app.py
```
Open **http://localhost:8501** and start your fitness journey 🎯

## 📁 Project Structure
fitness-agent-ai/
│
├── 🧠 agents.py          → AI agent definitions (Planner + Reviewer)
├── 📋 tasks.py           → Task prompts for each agent
├── 🖥️  app.py             → Streamlit UI + main app logic
├── 🔧 tools.py           → BMI, BMR, TDEE, Macro calculators
├── 🛡️  guardrails.py      → Safety validation layer
├── 📦 requirements.txt   → Dependencies
├── 🔐 .env               → API keys (never pushed to GitHub)
└── 🚫 .gitignore         → Ignores .env and cache files

## ⚠️ Rate Limit Notice

This app uses **Groq's free tier** which allows 12,000 tokens per minute.
The app handles this automatically with smart retry logic — but if you see a delay, that's why.

For unlimited usage → [Upgrade to Groq Dev Tier](https://console.groq.com/settings/billing) (~$5 credit)


## 🗺️ Roadmap

- [x] v1.0 — Core meal plan + workout + progress + safety
- [ ] v2.0 — SQLite history to track progress across weeks
- [ ] v2.0 — PDF export of your full fitness plan
- [ ] v2.0 — Smarter rate limit queue
- [ ] v3.0 — User login & personal dashboard
- [ ] v3.0 — Multi-language support (Hindi, Spanish)

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you'd like to change.

## 📄 License

MIT License — free to use, modify and distribute.

<p align="center">
  Built with ❤️ using CrewAI + Groq + Streamlit
</p>