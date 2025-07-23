import streamlit as st
import google.generativeai as genai
import json
import os
import datetime

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
    st.markdown("Enter client project details below:")

    client_name = st.text_input("👤 Client Name")
    project_title = st.text_input("📌 Project Title")
    goals = st.text_area("🎯 Project Goals")
    stakeholders = st.text_area("👥 Stakeholders")
    deadline = st.text_input("🗓️ Timeline / Deadline")
    risks = st.text_area("⚠️ Known Risks / Concerns")
    questions = st.text_area("❓ Client Questions or Flags")
    submitted = st.button("Generate AI Summary")

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

# Show summary (always visible if available)
if "generated_summary" in st.session_state:
    with st.expander("📄 View AI Summary", expanded=True):
        st.markdown(st.session_state.generated_summary)

# 3️⃣ Multi-Project Memory Selector
if memory_data:
    with st.expander("🧠 Switch Between Saved Projects", expanded=False):
        project_keys = list(memory_data.keys())
        selected_project = st.selectbox("Select Project", project_keys)

        if selected_project:
            selected_data = memory_data[selected_project]
            st.markdown(f"**Client:** {selected_data['client_name']}")
            st.markdown(f"**Project:** {selected_data['project_title']}")
            st.markdown(f"**📝 Summary:**\n\n{selected_data['summary']}")

# 4️⃣ Auto Next Steps
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

# 5️⃣ Push to Jira (Simulated)
if "generated_summary" in st.session_state:
    with st.expander("🚀 Push to Jira (Simulated)", expanded=False):
        st.markdown("This is a demo of pushing to Jira. In production, this would trigger an API call.")

        if st.button("🔁 Simulate Push to Jira"):
            st.success("🎉 Summary successfully pushed to Jira!")

# Footer
st.divider()
st.markdown("Built with ❤️ by Rita Sharma · Powered by Gemini · [Demo Use Only]")
