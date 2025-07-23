import streamlit as st
import openai

# Set your OpenAI key if running locally (optional)
# openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="AI Client Onboarding Agent", page_icon="🤖")
st.title("🤖 AI Client Onboarding Agent")
st.markdown("""
Welcome! Please enter your basic information and let our AI agent help you get started.
""")

# --- Input Form ---
with st.form("onboarding_form"):
    name = st.text_input("👤 Your Name")
    company = st.text_input("🏢 Company Name")
    email = st.text_input("📧 Email")
    website = st.text_input("🌐 Company Website")
    goals = st.text_area("🎯 What are your primary goals / pain points?")
    budget = st.selectbox("💰 Estimated Budget Range", ["< $5,000", "$5,000 - $20,000", "$20,000+"])
    submit = st.form_submit_button("🚀 Submit & Get AI Summary")

if submit:
    with st.spinner("🤖 Thinking..."):
        # --- Compose prompt ---
        prompt = f"""
        You are an AI onboarding agent. Based on the following client information, generate:
        1. A professional summary of the client's profile
        2. Suggested next steps
        3. A follow-up email draft to the client

        ---
        Name: {name}
        Company: {company}
        Email: {email}
        Website: {website}
        Goals: {goals}
        Budget: {budget}
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful business assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6
            )
            output = response.choices[0].message.content
            st.success("✅ AI Summary Ready!")
            st.markdown("---")
            st.markdown(output)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

    st.markdown("---")
    st.info("This is a demo version. For production, connect to your backend, CRM, or automation tools.")
