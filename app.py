import streamlit as st
import google.generativeai as genai
import json
import uuid

# Configure Gemini API Key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-pro")

# Project storage in session
if "project_data" not in st.session_state:
    st.session_state.project_data = {}

# App title
st.title("🤖 AI Client Project Onboarding Assistant")

# Tabs
tab1, tab2 = st.tabs(["📝 Intake Form", "📄 Generated Summary"])

# -------------------------
# 🧾 TAB 1: Intake Form
# -------------------------
with tab1:
    st.subheader("New Client Project Form")

    client_name = st.text_input("Client Name")
    project_title = st.text_input("Project Title")
    goals = st.text_area("Project Goals")
    stakeholders = st.text_area("Stakeholders")
    deadline = st.text_input("Timeline / Deadline")
    risks = st.text_area("Known Risks / Concerns")
    questions = st.text_area("Client Questions or Flags")

    submitted = st.button("✨ Generate Summary + Next Steps")

    if submitted:
        with st.spinner("Generating summary using Gemini..."):

            # Prompt for summary + next steps
            prompt = f"""
You are an experienced Project Manager. Based on the client's inputs below, generate:

1. A warm, confident internal onboarding summary.
2. 3–5 next steps for the delivery team.

Format:
### Summary
...

### Next Steps
- ...
- ...

Client Name: {client_name}
Project Title: {project_title}
Goals: {goals}
Stakeholders: {stakeholders}
Timeline: {deadline}
Risks: {risks}
Client Questions: {questions}
"""

            try:
                response = model.generate_content(prompt)
                full_output = response.text

                project_id = str(uuid.uuid4())[:8]
                st.session_state.project_data[project_id] = {
                    "title": project_title,
                    "summary": full_output
                }

                st.session_state.selected_project = project_id
                st.success("✅ Summary + Next Steps generated!")

            except Exception as e:
                st.error(f"Error: {e}")

# -------------------------
# 📄 TAB 2: Summary Viewer
# -------------------------
with tab2:
    st.subheader("📁 Project Summaries")

    if st.session_state.project_data:
        project_titles = {
            pid: data["title"] or f"Untitled Project ({pid})"
            for pid, data in st.session_state.project_data.items()
        }

        selected_pid = st.selectbox(
            "Select a project",
            options=list(project_titles.keys()),
            format_func=lambda pid: project_titles[pid],
            index=0 if "selected_project" not in st.session_state else list(project_titles.keys()).index(st.session_state.selected_project)
        )
        st.session_state.selected_project = selected_pid

        selected_summary = st.session_state.project_data[selected_pid]["summary"]
        st.markdown(selected_summary)

        # -------------------------
        # 🔁 Push to Jira Simulation
        # -------------------------
        if st.button("🚀 Push to Jira"):
            mock_ticket_id = f"AI-{str(uuid.uuid4())[:4].upper()}"
            st.success(f"✅ Ticket `{mock_ticket_id}` created for **{project_titles[selected_pid]}**.")
            st.info("🧪 This is a simulated Jira integration. Can be extended to push via API or n8n.")
    else:
        st.info("No summaries yet. Fill the form in Tab 1 to generate.")
