import streamlit as st
import google.generativeai as genai
import warnings

warnings.filterwarnings("ignore")

# Streamlit page config
st.set_page_config(page_title="Recipe Chatbot 🍳", layout="centered")


api_key = "AIzaSyAsIwG5JrrXsT3TrxLRGwq8waxnuKqB8_8"

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
                f"You're a cooking expert. Give recipes and instructions clearly.\n\nUser: {prompt}"
            )

            st.chat_message("assistant").markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Please enter your Gemini API key in the sidebar.")