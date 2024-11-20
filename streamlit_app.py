import streamlit as st
import openai
import os

# Use the API key from the GitHub Actions secret (e.g., 'KANNAN')
API_KEY = os.getenv(KANNAN)

if not API_KEY:
    st.error("No API key found. Please ensure the 'KANNAN' secret is set correctly in GitHub Actions.")
else:
    # Set the OpenAI API key
    openai.api_key = API_KEY

    # Show title and description
    st.title("💬 Chatbot")
    st.write(
        "This is a chatbot powered by OpenAI's models. You can ask it anything and get responses!"
    )

    # Sidebar for model selection
    st.sidebar.title("Settings")
    selected_model = st.sidebar.selectbox(
        "Select a model",
        options=["gpt-3.5-turbo", "gpt-4"],
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
    if prompt := st.chat_input("Ask me anything:"):
        # Add user input to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using OpenAI
        try:
            response = openai.ChatCompletion.create(
                model=selected_model,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )

            # Add assistant response to chat history
            assistant_message = response.choices[0].message["content"]
            with st.chat_message("assistant"):
                st.markdown(assistant_message)
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        except Exception as e:
            st.error(f"An error occurred: {e}")
