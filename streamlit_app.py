import streamlit as st
import google.generativeai as genai

def initialize_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def get_gemini_response(model, question):
    response = model.generate_content(question)
    return response.text

# Streamlit app
st.title("Gemini AI Q&A App")

# API key input
api_key = st.secrets["APIKEY"]
#text_input("Enter your Gemini API Key:", type="password")

if api_key:
    # Initialize the model
    model = initialize_gemini(api_key)

    # Store the model in session state
    if 'model' not in st.session_state:
        st.session_state['model'] = model

    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get and display Gemini response
        response = get_gemini_response(st.session_state['model'], prompt)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)

else:
    st.warning("Please enter your Gemini API Key to start.")

# Instructions
st.sidebar.title("Instructions")
st.sidebar.markdown("""
1. Enter your Gemini API Key in the text box above.
2. Once entered, you can start asking questions in the chat interface.
3. The app will use the Gemini API to generate responses.
4. Your conversation history will be displayed in the chat.
5. Refresh the page to start a new conversation.

Note: Your API key is not stored and will need to be re-entered if you refresh the page.
""")