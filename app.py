import streamlit as st
import json
import os
import datetime
import google.generativeai as genai

# --- Config ---
genai.configure(api_key=os.getenv("GOOGLE_API_KEY") or "your-gemini-api-key")

# --- Memory Setup ---
if "project_memory" not in st.session_state:
    st.session_state.project_memory = {}

# --- Load Gemini Model ---
model = genai.GenerativeModel("gemini-2.0-flash")

# --- Page Config ---
st.set_page_config(page_title="🌟 AI Onboarding Assistant", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(to right, #e0f7fa, #ffffff);
        padding: 1rem;
    }

    .main-card {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }

    h1, h2, h3 {
        color: #1e3a5f;
    }

    div.stButton > button {
        background: linear-gradient(to right, #28a745, #218838);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 128, 0, 0.3);
    }

    [data-testid="stExpander"] {
        border-radius: 14px;
        margin-top: 1rem;
        box-shadow: 0 6px 16px rgba(0,0,0,0.07);
        background: #f9f9f9;
    }

    [data-testid="stExpander"] summary {
        font-weight: 600;
        font-size: 1.1rem;
        background-color: #e6f4ea;
        padding: 0.75rem 1rem;
        border-radius: 10px;
        cursor: pointer;
    }

    [data-testid="stExpander"] summary:hover {
        background-color: #d4edda;
    }

    .stMarkdown {
        font-size: 1rem;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.title("🤖 AI Onboarding Assistant")
st.markdown("Welcome! Fill in the details below and let our AI help you onboard clients smartly. ✨")

# --- Project Selector ---
project_names = list(st.session_state.project_memory.keys())
selected_project = st.selectbox("🔀 Select or Create a Project", ["New Project"] + project_names)

if selected_project == "New Project":
    new_project_name = st.text_input("Enter new project name")
    if new_project_name and new_project_name not in st.session_state.project_memory:
        st.session_state.project_memory[new_project_name] = []
        selected_project = new_project_name
else:
    new_project_name = selected_project

# --- Input Form ---
st.subheader("📋 Client Onboarding Form")

with st.form(key="onboarding_form"):
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)

        name = st.text_input("👤 Client Name")
        company = st.text_input("🏢 Company Name")
        goals = st.text_area("🎯 Key Goals / Use Cases")
        pain_points = st.text_area("❗ Current Pain Points")
        tools = st.text_input("🛠️ Tools in Use (Comma Separated)")
        submitted = st.form_submit_button("✅ Generate Summary")

        st.markdown('</div>', unsafe_allow_html=True)

# --- Handle Submission ---
if submitted and name:
    prompt = f"""
    You're an AI onboarding specialist. Summarize the following client data in an executive tone.

    Name: {name}
    Company: {company}
    Goals: {goals}
    Pain Points: {pain_points}
    Tools: {tools}
    """

    with st.spinner("⚙️ Generating Gemini-powered onboarding summary..."):
        try:
            response = model.generate_content(prompt)
            summary = response.text
        except Exception as e:
            summary = f"⚠️ Error generating summary: {e}"

    # Save to memory
    if new_project_name:
        st.session_state.project_memory[new_project_name].append({
            "timestamp": datetime.datetime.now().isoformat(),
            "summary": summary
        })

    # --- Display Summary ---
    st.markdown("### 📝 AI Summary")
    st.markdown(f'<div class="main-card">{summary}</div>', unsafe_allow_html=True)

    # --- Expander: Next Steps ---
    with st.expander("💡 Suggested Next Steps"):
        next_prompt = f"Based on this onboarding summary, suggest 3 next steps:\n\n{summary}"
        try:
            next_response = model.generate_content(next_prompt)
            st.markdown(next_response.text)
        except Exception as e:
            st.error(f"⚠️ Error generating next steps: {e}")

    # --- Expander: Project History ---
    with st.expander("📂 Project History & Switch"):
        for project, sessions in st.session_state.project_memory.items():
            st.markdown(f"**{project}** ({len(sessions)} entries)")
            for s in sessions[-1:]:
                st.markdown(f"- ⏰ {s['timestamp'][:19]}: {s['summary'][:120]}...")

    # --- Expander: Simulate Push to Jira ---
    with st.expander("🚀 Push to Jira (Simulated)"):
        st.success(f"Pushed to `JIRA-PROJECT/{new_project_name.upper()}` as onboarding notes.")

# --- Load Example ---
if st.button("📌 Load Demo Project"):
    demo_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "summary": "Client: ABC Corp\nGoals: Automate workflows\nPain Points: Manual onboarding\nTools: Notion, Slack"
    }
    st.session_state.project_memory["Demo Project"] = [demo_data]
    st.experimental_rerun()
