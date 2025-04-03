'''About Page for Iceland Travel AI Assistant'''

# Import necessary libraries
import streamlit as st

# Content for the About page
def about_page():
    """
    This function creates the About page for the Iceland Travel AI Assistant.
    It provides information about the app, its purpose, and how to use it.
    """

    st.title("About This App")

    st.write("""
    This application is part of my **Data Science and Machine Learning bootcamp project** focused on **Generative AI**. I chose travel and Iceland as the topic because I absolutely love to travel and Iceland is my favorite country! My goal is to help other travelers **get instant AI-powered answers** for their Iceland adventures.  
    """)

    st.markdown("### 🌍 Why Use This App?")
    st.write("""
    - **Instant AI-powered answers** for your Iceland travel questions.
    - **Discover the best destinations, activities, and hidden gems.**
    - **Get tips** on budget travel, road trips, and must-see locations.
    - **Built with Generative AI & my personal travel experience.**
    """)

    # About the Creator
    st.markdown("### 👩🏻‍💻 About Me")
    st.write("""
    I'm **Annie Meneses Gonzalez**, a passionate traveler. I've visited **Iceland multiple times**, exploring its **glaciers, volcanoes, waterfalls, and hidden landscapes**.  
    This app combines my love for **AI, travel, and helping others** explore Iceland effortlessly! 
    """)

    # Video Section with Context
    st.markdown("### ✨ Sharing One of My Favorite Places: Vestrahorn")
    st.write("""
    Vestrahorn is one of **Iceland’s most breathtaking landscapes**, with dramatic black sand beaches, towering peaks, and 
    a surreal atmosphere. It’s a must-visit for photographers and nature lovers alike.  
    Here’s a short clip from my own travels. Hope it inspires you!  
    """)

    col1, col2, col3 = st.columns([2, 4, 2])
    with col2:  
        # Video of Vestrahorn
        video_file = open("./images/iceland.mov", "rb")
        video_bytes = video_file.read()
        st.video(video_bytes)

    st.write("\n")  

    # Footer Section
    st.markdown("---")
    st.markdown("Created with ❤️ by [Annie Meneses Gonzalez](https://www.linkedin.com/in/annie-meneses-gonzalez-57bb9b145/)") 
    #st.markdown("For more travel tips and guides, follow me on [Instagram](https://www.instagram.com/mgtripplanner/).") 