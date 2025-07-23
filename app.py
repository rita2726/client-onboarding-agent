import streamlit as st
import datetime

st.set_page_config(page_title="Client Onboarding AI Agent", page_icon="🤖")

st.title("🤖 Client Onboarding AI Agent")

with st.form("onboarding_form"):
    st.subheader("📋 Fill Client Details")

    name = st.text_input("Client Name")
    email = st.text_input("Email Address")
    company = st.text_input("Company Name")
    industry = st.selectbox("Industry", ["Tech", "Finance", "Healthcare", "Other"])
    project_scope = st.text_area("Describe the Project Scope")
    urgency = st.select_slider("Urgency Level", ["Low", "Medium", "High"])
    submit = st.form_submit_button("Submit")

if submit:
    st.success("🎉 Agent Response:")
    st.markdown(f"""
    👋 Hello **{name}**,  
    Thanks for reaching out on behalf of **{company}** in the **{industry}** industry.  
    We'll review your project scope and get back to you within 24 hours based on your **{urgency}** urgency level.  
    📧 Confirmation sent to: `{email}`  
    🕐 Timestamp: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    """)

    st.info("✅ This is a Client Onboarding AI agent. Email was sent to the client.")
