import streamlit as st
import openai
import os

# Fetch the API key from the environment
api_key = st.secrets["kannan"]

if not api_key:
    st.error("The secret 'kannan' is not set or missing. Please ensure it is configured correctly in your environment.")
else:
    # Set the OpenAI API key
    openai.api_key = api_key
    st.success("The secret 'KANNAN' is set successfully.")

    # Example: Streamlit app with OpenAI ChatCompletion
    st.title("💬 Chatbot with Secure API Key")
    st.write("This chatbot uses OpenAI's GPT models to generate responses.")

    # Sidebar for model selection
    st.sidebar.title("Settings")
    selected_model = st.sidebar.selectbox(
        "Select a model",
        options=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        index=0,
    )

    # Chat input
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input box for the user query
    if prompt := st.chat_input("Ask me anything:"):
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

            # Display assistant's response
            assistant_message = response.choices[0].message["content"]
            with st.chat_message("assistant"):
                st.markdown(assistant_message)
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        except Exception as e:
            st.error(f"An error occurred: {e}")
