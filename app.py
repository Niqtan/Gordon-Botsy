import streamlit as st
import google.generativeai as genai
import warnings
import os
from dotenv import load_dotenv

load_dotenv()
warnings.filterwarnings("ignore")

# Streamlit page config
st.set_page_config(page_title="Recipe Chatbot 🍳", layout="centered")

# Set your API key
api_key = os.getenv('api_key')

# Main title
st.title("👩‍🍳 Recipe & Cooking Chatbot")
st.markdown("Ask me how to cook anything!")

# Initialize Gemini if API key is provided
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")

        # Initialize chat session
        if "chat_session" not in st.session_state:
            st.session_state.chat_session = model.start_chat(history=[])
            st.session_state.messages = []

        # Display previous messages
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Input field
        if prompt := st.chat_input("What recipe do you need help with?"):
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Get Gemini response
            response = st.session_state.chat_session.send_message(
                f"You are a cooking expert named Gordon Bot-sy. Only provide recipes and instructions clearly. "
                f":User  {prompt}"
            )

            # Extract and display only the recipe
            recipe_text = response.text.strip()
            st.chat_message("assistant").markdown(recipe_text)
            st.session_state.messages.append({"role": "assistant", "content": recipe_text})

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Please enter your Gemini API key in the sidebar.")
