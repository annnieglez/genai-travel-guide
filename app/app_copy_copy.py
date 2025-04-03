'''This is a Streamlit application for an Iceland Travel AI Assistant.'''

# Import necessary libraries

# Streamlit Libraries
import streamlit as st
from streamlit_option_menu import option_menu

# Importing pages
import _pages.chat as chat_page
import _pages.about as about_page
import _pages.home as home_page

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

    # Main content based on selected menu item

    # Home    
    if selected == "Home":
        home_page.home_page()

    # Travel Assistant
    if selected == "Travel Assistant":
        chat_page.chat_page()

    # About
    if selected == "About":
        about_page.about_page()

if __name__ == "__main__":
    main()

