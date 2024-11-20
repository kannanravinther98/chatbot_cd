import streamlit as st
import openai
import os

# Load environment variables from a .env file (if using for local development)

# Embed the OpenAI API key securely
API_KEY =kannan  # Replace with your key in .env or environment variable

# Allow user to override the key if it's not set via environment variables
if not API_KEY:
    st.warning("No API key found in environment. Please enter your API key below.")
    API_KEY = st.text_input("OpenAI API Key", type="password")
else:
    st.success("Using the API key from environment.")

if not API_KEY:
    st.info("Please provide a valid OpenAI API key to continue.", icon="🗝️")
else:
    # Set the OpenAI API key
    openai.api_key = API_KEY

    # Show title and description
    st.title("💬 Chatbot with Multiple Models")
    st.write(
        "This is a simple chatbot powered by OpenAI's models. You can select the model "
        "you want to use and chat interactively. To use this app, ensure you have a valid API key."
    )

    # Sidebar for model selection
    st.sidebar.title("Settings")
    selected_model = st.sidebar.selectbox(
        "Select a model",
        options=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        index=0,
    )

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input field
    if prompt := st.chat_input("What would you like to ask?"):
        # Add user's input to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the selected OpenAI model
        try:
            response = openai.ChatCompletion.create(
                model=selected_model,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )

            # Extract and display assistant's response
            assistant_message = response.choices[0].message["content"]
            with st.chat_message("assistant"):
                st.markdown(assistant_message)
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        except openai.error.OpenAIError as e:
            st.error(f"An error occurred: {e}")
