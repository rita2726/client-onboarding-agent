import streamlit as st
import google.generativeai as genai
import os

# Configure Gemini API key
genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")

st.subheader("🔍 Debug: List Available Gemini Models")

if st.button("List Available Models"):
    try:
        models = genai.list_models()
        for model in models:
            st.success(f"{model.name} — {model.supported_generation_methods}")
    except Exception as e:
        st.error(f"❌ Error fetching models: {e}")


# Set Gemini API Key (use environment variable or secrets)
genai.configure(api_key=os.getenv("GEMINI_API_KEY", st.secrets.get("GEMINI_API_KEY")))

# Create Gemini model
model = genai.GenerativeModel("gemini-pro")

# Streamlit UI
st.title("📨 AI Client Onboarding Summary Generator (Gemini)")

with st.form("input_form"):
    client_name = st.text_input("Client Name", placeholder="e.g. Acme Corp")
    project_scope = st.text_area("Project Scope", placeholder="e.g. Redesign their e-commerce platform...")
    budget = st.text_input("Budget", placeholder="e.g. Under $5,000")
    timeline = st.text_input("Timeline", placeholder="e.g. 3 months")

    submitted = st.form_submit_button("Generate Summary")

if submitted:
    with st.spinner("Generating summary..."):
        prompt = f"""
You are a Project Manager at a top consulting agency. Write a warm, confident onboarding summary for the internal team after a new client fills in a project intake form.

Use the following details:
- Company: {client_name}
- Project Scope: {project_scope}
- Budget: {budget}
- Timeline: {timeline}

Structure the message in a professional, friendly tone with a clear subject line, intro, project breakdown, and suggested next steps.
"""

        response = model.generate_content(prompt)
        st.subheader("📨 Generated Summary")
        st.markdown(response.text)
