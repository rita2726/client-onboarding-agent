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
st.set_page_config(page_title="AI Onboarding Assistant", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f3f7fa;
        font-family: 'Segoe UI', sans-serif;
    }

    div.stButton > button {
        background-color: #28a745;
        color: white;
        font-weight: 600;
        padding: 0.6em 1.2em;
        border: none;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 128, 0, 0.2);
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        background-color: #218838;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 128, 0, 0.3);
    }

    [data-testid="stExpander"] {
        background: #ffffff;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin: 1rem 0;
    }

    [data-testid="stExpander"] > details {
        border: none;
    }

    [data-testid="stExpander"] summary {
        font-size: 1rem;
        font-weight: 600;
        color: #155724;
        background-color: #e6f4ea;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        list-style: none;
    }

    [data-testid="stExpander"] summary::-webkit-details-marker {
        display: none;
    }

    .stMarkdown {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        margin-top: 1rem;
        font-size: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- App Title ---
st.title("🤖 AI Onboarding Assistant")

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
st.subheader("📋 Onboarding Form")
with st.form(key="onboarding_form"):
    name = st.text_input("👤 Client Name")
    company = st.text_input("🏢 Company Name")
    goals = st.text_area("🎯 Key Goals / Use Cases")
    pain_points = st.text_area("❗ Current Pain Points")
    tools = st.text_input("🛠️ Tools in Use (Comma Separated)")
    submitted = st.form_submit_button("✅ Generate Summary")

# --- Handle Submit ---
if submitted and name:
    prompt = f"""
    You're an AI Onboarding Specialist. Summarize the following client data in an executive tone.

    Name: {name}
    Company: {company}
    Goals: {goals}
    Pain Points: {pain_points}
    Tools: {tools}
    """

    with st.spinner("Generating Gemini-powered onboarding summary..."):
        try:
            response = model.generate_content(prompt)
            summary = response.text
        except Exception as e:
            summary = f"Error generating summary: {e}"

    # Save to project memory
    if new_project_name:
        st.session_state.project_memory[new_project_name].append({
            "timestamp": datetime.datetime.now().isoformat(),
            "summary": summary
        })

    st.markdown("### 📝 AI Summary")
    st.markdown(summary)

    # --- Expander: Suggested Next Steps ---
    with st.expander("💡 Suggested Next Steps"):
        next_prompt = f"Based on this onboarding summary, suggest 3 next steps:\n\n{summary}"
        try:
            next_response = model.generate_content(next_prompt)
            st.markdown(next_response.text)
        except Exception as e:
            st.error(f"Error generating next steps: {e}")

    # --- Expander: Project History ---
    with st.expander("📂 Switch Between Projects"):
        for project, sessions in st.session_state.project_memory.items():
            st.markdown(f"**{project}** ({len(sessions)} entries)")
            for s in sessions[-1:]:
                st.markdown(f"- {s['timestamp'][:19]}: {s['summary'][:100]}...")

    # --- Expander: Push to Jira ---
    with st.expander("🚀 Push to Jira"):
        st.markdown("🧪 This is a simulated Jira ticket creation.")
        st.markdown(f"✅ Pushed summary to `JIRA-PROJECT/{new_project_name.upper()}` as onboarding notes.")

# --- Load Example ---
if st.button("📌 Load Example Project"):
    demo_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "summary": "Client: ABC Corp\nGoals: Automate workflows\nPain Points: Manual onboarding\nTools: Notion, Slack"
    }
    st.session_state.project_memory["Demo Project"] = [demo_data]
    st.experimental_rerun()
