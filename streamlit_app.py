import streamlit as st
import google.generativeai as genai

# Initialize session state
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'context' not in st.session_state:
    st.session_state.context = ""

def initialize_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def get_gemini_response(model, question, user_type, context):
    user_type_prompts = {
        "Kid": "You are talking to a child. Use simple language and explanations suitable for children. Keep responses brief and engaging.",
        "Adult": "You are conversing with an adult. Provide detailed and comprehensive responses.",
        "Senior": "You are speaking with a senior citizen. Be respectful, patient, and use clear language. Consider potential health or technology-related concerns in your responses."
    }
    
    full_prompt = f"""
    {context}

    You are an AI assistant for Tempe Envision Center. Always be helpful, friendly, and informative. 
    {user_type_prompts.get(user_type, '')}
    
    If asked about information not provided in the context, politely state that you don't have that specific information 
    and offer to help with general inquiries or direct them to contact the center's staff for the most up-to-date information.

    Human: {question}
    AI Assistant:
    """
    response = model.generate_content(full_prompt)
    return response.text

# Streamlit app
st.title("Tempe Envision Center Assistant")

# Sidebar for context input (for demo purposes, normally this would be pre-set)
st.sidebar.title("Set Envision Center Information")
context_input = st.sidebar.text_area(
    "Enter information about the Envision center:",
    value="""
    Tempe Envision Center Information:
    - Location: 1600 E Apache Blvd, Tempe, AZ 85281
    - Hours: Monday-Friday 8am-5pm, Saturday Closed, Closed on Sundays
    - Contact: (480) 350-5400
    - Facilities: Computer Lab, Meeting Rooms, Classrooms, Workforce Development Center
    - Programs:
      * Adult Education: GED Classes, English Language Learning
      * Workforce Development: Job Search Assistance, Resume Writing Workshops
      * Youth Programs: After-school Tutoring, STEM Workshops
      * Community Services: Housing Assistance, Financial Literacy Classes
    - Services: 
      * Free Wi-Fi
      * Computer Access
      * Printing and Copying (fees may apply)
    """,
    height=300
)
if st.sidebar.button("Update Center Information"):
    st.session_state.context = context_input
    st.sidebar.success("Envision Center information updated!")

# API key input
api_key = st.text_input("Enter your Gemini API Key:", type="password")

if api_key:
    # Initialize the model
    model = initialize_gemini(api_key)

    # User type selection
    st.subheader("Select Your User Type:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Kid"):
            st.session_state.user_type = "Kid"
    with col2:
        if st.button("Adult"):
            st.session_state.user_type = "Adult"
    with col3:
        if st.button("Senior"):
            st.session_state.user_type = "Senior"

    # Display selected user type
    if st.session_state.user_type:
        st.write(f"Selected User Type: {st.session_state.user_type}")

    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("How can I help you with Tempe Envision Center?"):
        if st.session_state.user_type:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get and display Gemini response
            response = get_gemini_response(model, prompt, st.session_state.user_type, st.session_state.context)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(response)
        else:
            st.warning("Please select a user type before asking questions.")

else:
    st.warning("Please enter your Gemini API Key to start.")

# Instructions
st.sidebar.title("How to Use")
st.sidebar.markdown("""
1. Enter the Gemini API Key.
2. Select your user type (Kid, Adult, or Senior).
3. Ask questions about Tempe Envision Center in the chat interface.
4. The AI will provide information based on your user type and the center's details.
5. For real deployment, remove the 'Set Envision Center Information' section and pre-set the context.
""")