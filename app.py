import streamlit as st
import google.generativeai as genai

# Configure Gemini API Key (from Streamlit secrets)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Load the Gemini model
model = genai.GenerativeModel("gemini-1.5-pro") 

# Title
st.title("📝 AI Project Intake Summary")

# Tabs
tab1, tab2 = st.tabs(["Project Form", "Generated Summary"])

# Input form
with tab1:
    st.subheader("🧾 New Client Project Intake Form")

    client_name = st.text_input("Client Name")
    project_title = st.text_input("Project Title")
    goals = st.text_area("Project Goals")
    stakeholders = st.text_area("Stakeholders")
    deadline = st.text_input("Timeline / Deadline")
    risks = st.text_area("Known Risks / Concerns")
    questions = st.text_area("Client Questions or Flags")
    submitted = st.button("Generate Summary")

    if submitted:
        with st.spinner("Generating summary using Gemini..."):

            # Prompt Template
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
                st.success("✅ Summary generated. Check the next tab!")
            except Exception as e:
                st.error(f"Failed to generate summary: {e}")

# Summary tab
with tab2:
    st.subheader("📄 Onboarding Summary")
    if "generated_summary" in st.session_state:
        st.markdown(st.session_state.generated_summary)
    else:
        st.info("Fill the form and click Generate Summary to see the output here.")
