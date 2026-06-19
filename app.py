import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load API key configuration
load_dotenv()

# Initialize the Gemini Client
client = genai.Client()

# Set up the Web Page Title and Design layout
st.set_page_config(page_title="IdeaHive AI Playbook Generator", page_icon="🚀", layout="centered")

st.title("🚀 IdeaHive AI Startup Playbook Generator")
st.write("Type your startup or project idea below to instantly generate a custom validation playbook blueprint!")

# Create a text input box for your user
user_idea = st.text_input("Enter your startup idea:", placeholder="e.g., A platform for local grocery delivery tracking...")

# Create an interactive "Generate" button
if st.button("Generate My Playbook"):
    if not user_idea.strip():
        st.warning("Please enter a valid startup idea first!")
    else:
        with st.spinner("Engineering your validation playbook... Please wait..."):
            # Insert the user's specific idea dynamically into the engineer prompt
            prompt = f"""
            You are an expert Startup Validation Engineer. 
            Provide a detailed, step-by-step landing page validation playbook blueprint 
            specifically tailored for this startup idea: "{user_idea}".
            List the exact low-friction landing page tools and audience-building 
            software stacks required to run the test efficiently.
            """
            
            try:
                # Query the Gemini model
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
                # Display the results beautifully on the webpage interface
                st.success("✨ Done! Here is your custom blueprint:")
                st.markdown("---")
                st.markdown(response.text)
                st.markdown("---")
                
            except Exception as e:
                st.error(f"❌ Core engine connection failed: {e}")