'''This module contains the implementation of the chat page for the Iceland Travel AI Assistant.'''

# Import necessary libraries

# Streamlit Libraries
import streamlit as st
from streamlit_extras.let_it_rain import rain

# Standard Libraries
import time
import os

# OpenAI Libraries
import openai

if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-4o"

# Custom Libraries
from genai_scripts import GenAI_RAG as rag

# Load environment variables from the .env file
from dotenv import load_dotenv
load_dotenv()
client_openai = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Content for the Home page
def chat_page():
    """
    This function creates the chat page for the Iceland Travel AI Assistant.
    It initializes the Streamlit app, sets up the layout, and handles user interactions.
    """
 
    col1, col2, col3 = st.columns([2.5,3,2])
    with col2:  
        # Title
        st.title("GenAI Iceland Travel Guide")

    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Initial message fom the assistant
    initial_message = "Hello 👋. Ask me anything about travel to Iceland"
    with st.chat_message(name = "assistant"):
        st.write(initial_message)

    # Initialize session state for the chat history
    for message in st.session_state.messages:
        with st.chat_message(name=message["role"]):
                st.markdown(message["content"])

    # Chat input for user query
    query = st.chat_input("What is up?")

    # If the user submits a query
    if query:

        # Call the RAG model to generate a response
        retrieved_chunks, prompt = rag.generate_response_from_gpt4o(test = False, question = query, app = True)

        # Add user message to the chat
        with st.chat_message(name = "user"):
            st.markdown(query)
        # Add the user message to the session state
        st.session_state.messages.append({"role": "user", "content": query})

        # Add assistant message to the chat
        with st.chat_message(name = "assistant"):

            # Initialize a placeholder for the assistant message
            # This allows us to update the message in place
            message_placeholder = st.empty()
            content = ""

            # Generate the response using OpenAI's API
            # Use the stream=True parameter to get a streaming response
            for response in client_openai.chat.completions.create(
                model=st.session_state.openai_model,
                messages=[{"role": "system", "content": "You are an AI assistant restricted to answering questions only from the database."},
                        {"role": "user", "content": prompt}],
                stream=True,
            ):
                
                # Update the content with the new chunk of text
                content += getattr(response.choices[0].delta, "content", "") or ""
                time.sleep(0.02)
                message_placeholder.markdown(content + "|")

            # Add a rain animation if the content is a specific message
            if content == "I don't have that information at the moment. This is a work-in-progress app, so check back soon for more updates! Is there anything else I can help you with?":
                rain(
                    emoji="😔",
                    font_size=54,
                    falling_speed=2,
                    animation_length=1)
            # Show the final content without the trailing "|"
            message_placeholder.markdown(content)

        # Add the assistant message to the session state
        st.session_state.messages.append({"role": "assistant", "content": content})