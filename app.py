import streamlit as st
import google.generativeai as genai

# Configure Gemini API Key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Load the Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

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
                st.session_state.risks = risks
                st.success("✅ Summary generated. Check the next tab!")
            except Exception as e:
                st.error(f"Failed to generate summary: {e}")

# Summary tab
with tab2:
    st.subheader("📄 Onboarding Summary")

    if "generated_summary" in st.session_state:
        st.markdown(st.session_state.generated_summary)

        # 📌 Auto-Next Steps Generator
        st.divider()
        st.subheader("📌 Suggested Next Steps")
        if st.button("Generate Next Steps"):
            with st.spinner("Thinking..."):
                try:
                    combined_prompt = f"""
You are a senior project manager. Based on the following project summary and risks, generate 3 clear, practical next steps a PM should take.

SUMMARY:
{st.session_state.generated_summary}

RISKS:
{st.session_state.risks}
"""

                    response = model.generate_content(combined_prompt)
                    next_steps = response.text.strip()
                    st.success("Here are your suggested next steps:")
                    st.markdown(next_steps)
                except Exception as e:
                    st.error(f"Could not generate next steps: {e}")
    else:
        st.info("Fill the form and click Generate Summary to see the output here.")
