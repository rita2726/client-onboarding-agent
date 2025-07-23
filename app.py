import streamlit as st
import openai
import os

# Set up OpenAI API Key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Client Onboarding Agent", page_icon="🤖")
st.title("🤖 AI-Powered Client Onboarding Agent")

st.markdown("Please fill in the client details below:")

# Input fields
company_name = st.text_input("🧾 Company Name")
project_scope = st.text_area("📋 Project Scope")
budget = st.selectbox("💰 Estimated Budget", ["< $5,000", "$5,000–$10,000", "$10,000+", "Not specified"])
timeline = st.text_input("⏱️ Preferred Timeline (e.g., 2 months, ASAP, etc.)")

# Tabs for output
tab1, tab2 = st.tabs(["📨 Onboarding Summary", "⚠️ Risk Flags / Client Questions"])

# Tab 1: Onboarding Summary
with tab1:
    if st.button("📝 Generate Summary"):
        with st.spinner("Crafting onboarding email..."):
            prompt = f"""
            You are an AI client onboarding assistant. Create a professional, friendly onboarding email for a new client.

            Company: {company_name}
            Project Scope: {project_scope}
            Budget: {budget}
            Timeline: {timeline}

            Write it in a warm but confident tone. Use emojis for modern formatting. Add a 3-point next steps list to suggest how the internal team should proceed.
            """

            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert client onboarding agent who writes professional onboarding summaries for internal teams."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            onboarding_summary = response.choices[0].message.content
            st.subheader("📨 Generated Summary")
            st.markdown(onboarding_summary)

            st.download_button("📥 Download Summary", onboarding_summary, file_name="onboarding_summary.txt")

# Tab 2: Risk Flags / Questions
with tab2:
    if st.button("🔍 Analyze Risks & Questions"):
        with st.spinner("Analyzing potential red flags and questions..."):
            risk_prompt = f"""
            You are an AI onboarding risk analyzer.

            Based on the following details, identify:
            1. Potential project red flags or risks (e.g., unclear scope, tight budget, missing timeline).
            2. Smart clarifying questions the team should ask the client.

            Company: {company_name}
            Project Scope: {project_scope}
            Budget: {budget}
            Timeline: {timeline}

            Format the response into two bullet sections.
            """

            risk_response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a senior project risk analyst."},
                    {"role": "user", "content": risk_prompt}
                ],
                temperature=0.6
            )

            risk_output = risk_response.choices[0].message.content
            st.subheader("⚠️ Risk Flags & Client Questions")
            st.markdown(risk_output)

            st.download_button("📥 Download Risk Summary", risk_output, file_name="risk_flags_and_questions.txt")

