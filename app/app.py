'''This is a Streamlit application for an Iceland Travel AI Assistant.'''

# Import necessary libraries

# Streamlit Libraries
import streamlit as st
from streamlit_option_menu import option_menu

# Standard Libraries
import os

# Importing pages
import _pages.chat as chat_page
import _pages.about as about_page
import _pages.home as home_page

# OpenAI Libraries
import openai

# Load environment variables from the .env file
from dotenv import load_dotenv
load_dotenv()

def main():
    '''Main function to run the Streamlit app.'''

    # Set the app configuration
    st.set_page_config(page_title="Iceland Travel AI Assistant", layout="wide", page_icon="./images/mg-trip-planner-logo-no-name.png", initial_sidebar_state="collapsed")

    # Sidebar menu
    with st.sidebar:
        selected = option_menu(
            menu_title=None, 
            options=["Home", "Travel Assistant", "About"], 
            icons=['house', 'robot', 'info-circle'], 
            menu_icon="robot", 
            default_index=1,
            styles={"container": {"padding": "5!important", "background-color": "#fafafa"},
                    "icon": {"color": "#3F8A90", "font-size": "25px"},
                    "nav-link": {"font-size": "16px", "text-align": "left", "margin":"5px", "color": "#000000", "--hover-color": "#eee"},
                    "nav-link-selected": {"background-color": "#E29F41"}})
        with st.popover("\u26bf Please enter your OpenAI API Key"):
            default_openai_api_key = os.getenv("OPENAI_API_KEY")
            if default_openai_api_key is None:
                default_openai_api_key = ""
            openai_api_key = st.text_input("Enter your OpenAI API Key", 
                                           type="password", 
                                           placeholder="sk-...",
                                           value=default_openai_api_key,
                                           key="openai_api_key",
                                           )
            
        cols0 = st.columns(2)
        with cols0[1]:
            st.button("Clear chat", on_click=lambda: st.session_state.messages.clear(), type="primary")

    # Main content based on selected menu item

    # Home    
    if selected == "Home":
        home_page.home_page()

    # Travel Assistant
    if selected == "Travel Assistant":
        # Check if the OpenAI API key is provided
        print("OpenAI API Key:", openai_api_key)
        missing_api_key = openai_api_key == "" or openai_api_key is None or "sk-" not in openai_api_key
        if missing_api_key:
            st.warning("Please enter your OpenAI API Key in the sidebar to continue...")
        else:
            chat_page.chat_page(openai_api_key)

    # About
    if selected == "About":
        about_page.about_page()

if __name__ == "__main__":
    main()

