import streamlit as st
import google.generativeai as genai
import json
import os
import datetime

# Inject SaaS-style Custom CSS
st.markdown("""
    <style>
    /* Base background + typography */
    .stApp {
        background-color: #f4f7fa;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #28a745;
        color: white;
        border-radius: 10px;
        padding: 0.6em 1.2em;
        font-weight: 600;
        border: none;
        box-shadow: 0 2px 6px rgba(40, 167, 69, 0.3);
        transition: all 0.2s ease-in-out;
    }

    div.stButton > button:hover {
        background-color: #218838;
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(40, 167, 69, 0.4);
    }

    /* Expanders – card style */
    details {
        border-radius: 12px;
        background-color: white;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-top: 1rem;
        padding: 0;
    }

    summary {
        padding: 12px 16px;
        font-weight: 600;
        font-size: 1.05rem;
        color: #155724;
        background-color: #e6f4ea;
        border-radius: 12px;
        list-style: none;
    }

    summary::-webkit-details-marker {
        display: none;
    }

    /* Text input / area */
    input, textarea {
        background-color: #ffffff !important;
        border: 1px solid #ced4da !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
    }

    /* Markdown box (e.g. LLM output) */
    .stMarkdown {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        margin-top: 1rem;
        font-size: 1rem;
    }

    </style>
""", unsafe_allow_html=True)


# Configure Gemini API Key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

# Paths
MEMORY_FILE = "multi_project_memory.json"

# Initialize memory
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump({}, f)

# Load memory
with open(MEMORY_FILE, "r") as f:
    memory_data = json.load(f)

# Title
st.title("🚀 AI Project Onboarding Assistant")
st.markdown("Make your PMO process faster, smarter, and risk-aware with AI ✨")

# 1️⃣ Project Form Section
with st.expander("📝 Fill New Project Intake Form", expanded=True):
    st.markdown("Enter client project details below or load an example:")

    # Load Example Button
    if st.button("🧪 Load Example Project"):
        st.session_state.client_name = "TechNova Ltd."
        st.session_state.project_title = "Customer Onboarding AI Automation"
        st.session_state.goals = "Automate user onboarding, reduce manual steps by 80%, integrate with CRM."
        st.session_state.stakeholders = "CTO, Product Manager, Customer Success Lead"
        st.session_state.deadline = "15 August 2025"
        st.session_state.risks = "Limited internal tech bandwidth; unclear user journey"
        st.session_state.questions = "What’s the expected TAT for full onboarding?"

    # Input Fields with Tooltips
    client_name = st.text_input("👤 Client Name", value=st.session_state.get("client_name", ""), help="Who is the client or company you're working with?")
    project_title = st.text_input("📌 Project Title", value=st.session_state.get("project_title", ""), help="What is the name of the project or initiative?")
    goals = st.text_area("🎯 Project Goals", value=st.session_state.get("goals", ""), help="List the primary objectives or outcomes of the project.")
    stakeholders = st.text_area("👥 Stakeholders", value=st.session_state.get("stakeholders", ""), help="Mention key people or roles involved.")
    deadline = st.text_input("🗓️ Timeline / Deadline", value=st.session_state.get("deadline", ""), help="Mention any fixed timelines or target launch dates.")
    risks = st.text_area("⚠️ Known Risks / Concerns", value=st.session_state.get("risks", ""), help="Any known challenges or risks you foresee?")
    questions = st.text_area("❓ Client Questions or Flags", value=st.session_state.get("questions", ""), help="Any queries or concerns raised by the client?")

    submitted = st.button("✅ Generate AI Summary")

# 2️⃣ AI Summary Section
if submitted:
    with st.spinner("Generating summary using Gemini..."):
        prompt = f"""
You are a project manager at a top consulting firm. A new client has submitted a project intake form.

Generate a warm, confident internal summary for the team using the following details:

Client Name: {client_name}
Project Title: {project_title}
Goals: {goals}
Stakeholders: {stakeholders}
Timeline: {deadline}
Risks: {risks}
Client Questions: {questions}

Make the summary sound human, structured, and useful for onboarding.
"""
        try:
            response = model.generate_content(prompt)
            summary = response.text
            st.session_state.generated_summary = summary
            st.session_state.last_project_key = f"{client_name} - {project_title}"

            # Save to memory
            memory_data[st.session_state.last_project_key] = {
                "client_name": client_name,
                "project_title": project_title,
                "goals": goals,
                "stakeholders": stakeholders,
                "deadline": deadline,
                "risks": risks,
                "questions": questions,
                "summary": summary,
                "timestamp": datetime.datetime.now().isoformat()
            }

            with open(MEMORY_FILE, "w") as f:
                json.dump(memory_data, f, indent=2)

            st.success("✅ Summary generated!")

        except Exception as e:
            st.error(f"Failed to generate summary: {e}")

# 3️⃣ View AI Summary
if "generated_summary" in st.session_state:
    with st.expander("📄 View AI Summary", expanded=True):
        st.markdown(st.session_state.generated_summary)

# 4️⃣ Multi-Project Memory Selector
if memory_data:
    with st.expander("🧠 Switch Between Saved Projects", expanded=False):
        project_keys = list(memory_data.keys())
        selected_project = st.selectbox("Select Project", project_keys)

        if selected_project:
            selected_data = memory_data[selected_project]
            st.markdown(f"**Client:** {selected_data['client_name']}")
            st.markdown(f"**Project:** {selected_data['project_title']}")
            st.markdown(f"**📝 Summary:**\n\n{selected_data['summary']}")

# 5️⃣ Auto Next Steps
if "generated_summary" in st.session_state:
    with st.expander("📌 Suggested Next Steps (Auto Generated)", expanded=False):
        try:
            steps_prompt = f"""You are a proactive project manager. Based on the following client onboarding summary, suggest 3 clear, actionable next steps for the internal team:

Summary:
{st.session_state.generated_summary}

Respond in bullet points."""
            response = model.generate_content(steps_prompt)
            st.markdown(response.text)
        except:
            st.warning("Next steps could not be generated.")

# 6️⃣ Push to Jira (Simulated)
if "generated_summary" in st.session_state:
    with st.expander("🚀 Push to Jira (Simulated)", expanded=False):
        st.markdown("This is a demo of pushing to Jira. In production, this would trigger an API call.")
        if st.button("🔁 Simulate Push to Jira"):
            st.success("🎉 Summary successfully pushed to Jira!")

# Footer
st.divider()
st.markdown("Built with ❤️ by Rita Sharma · Powered by Gemini · [Demo Use Only]")
