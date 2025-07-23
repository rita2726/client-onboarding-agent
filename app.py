import streamlit as st
import openai
from openai import OpenAI

st.title("🤖 Client Onboarding Agent (Demo)")

# Load API key securely from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Input fields
company_name = st.text_input("Company Name")
project_scope = st.text_area("Project Scope")
budget = st.selectbox("Estimated Budget", ["< $5,000", "$5,000 - $10,000", "> $10,000"])
timeline = st.text_input("Preferred Timeline")

if st.button("Generate Onboarding Summary"):
    with st.spinner("Creating onboarding plan..."):
        prompt = (
            f"You are a helpful AI onboarding agent. A new client from a company named '{company_name}' "
            f"has shared their project scope as: '{project_scope}'. Their estimated budget is '{budget}', "
            f"and their preferred timeline is '{timeline}'.\n\n"
            f"Generate a friendly, professional onboarding summary for the internal team."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert AI onboarding assistant."},
                    {"role": "user", "content": prompt},
                ]
            )
            st.success("Onboarding summary generated!")
            st.markdown("### 📝 Summary")
            st.markdown(response.choices[0].message.content)

        except Exception as e:
            st.error(f"Error: {e}")
