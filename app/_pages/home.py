'''Home Page for Iceland Travel AI Assistant'''

# Import necessary libraries
import streamlit as st

# Content for the About page
def home_page():
    """
    This function creates the home page for the Iceland Travel AI Assistant application.
    It includes a welcome message, an overview of the project, and some questions ideas.
    """

    # Custom CSS for background image & text styling
    st.markdown(
        """
        <style>
            .main {
                background: url('https://images.unsplash.com/photo-1536001461167-3bf3d8b1fcb8') no-repeat center center fixed;
                background-size: cover;
            }
            .title {
                text-align: center;
                font-size: 3em;
                font-weight: bold;
                color: white;
                text-shadow: 2px 2px 4px #000000;
            }
            .subtitle {
                text-align: center;
                font-size: 1.5em;
                color: white;
                text-shadow: 1px 1px 3px #000000;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Centering the image and title
    col1, col2, col3 = st.columns([6.2,4,4])
    with col2:  
        # Logo
        st.image("./images/mg-trip-planner-logo.png", width=200)

    # Hero Section
    st.markdown('<div class="title">Welcome to the Iceland Travel AI Assistant! </div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your AI-powered guide for exploring Iceland’s beauty.</div>', unsafe_allow_html=True)

    st.write("\n") 

    st.markdown("## 🌍 Overview")
    st.write("""
    This project is an AI-powered chatbot that provides real-time travel advice about Iceland. 
    It utilizes **Retrieval-Augmented Generation (RAG)** by storing document embeddings in **ChromaDB** 
    and retrieving relevant information to generate responses using a **Large Language Model (LLM)**.
    """)

    st.header("🚀 Features")
    st.write("""
    - **ChromaDB for Embeddings**: Stores and retrieves document embeddings (OpenAI's `text-embedding-3-large`) for relevant travel insights.
    - **Streamlit**: Provides a user-friendly interface for travelers to ask questions.
    - **AI-Powered Responses**: Uses an LLM (OpenAI's `gpt-4o`) to generate accurate and meaningful travel answers.
    - **Performance Evaluation**: Responses were tested using an LLM as a judge, with a **9/10** accuracy rating being the most common score.
    """)

    st.header("📚 Data Sources")
    st.write("""
    The data used for this project includes:
    - **Travel Guides**: Publicly available travel guides about Iceland.
    - **Tourism Websites**: Information from Icelandic tourism websites.
    - **MG Trip PLanner**: Iceland on a budget information.
    - **Custom Data**: Curated datasets collected via paid APIs (not included in the repository due to privacy concerns).
    """)

    st.markdown("## ✨ Explore Iceland’s Wonders")
    st.write("Here are some must-visit destinations you can ask the AI about:")
    st.write("""
    1. One of Iceland's most famous waterfalls, where you can walk behind the cascade.
    2. A uniquely shaped mountain, often seen in photographs and films.
    3. A stunning glacier in Vatnajökull National Park, perfect for ice hikes.
    4. A geothermal area with bubbling mud pots and steaming fumaroles.
    5. A picturesque village known for its colorful houses and stunning landscapes.
    """)

    st.write("\n")

    # Footer with GitHub link
    st.markdown("---")
    st.markdown(
        "**📌 Want to explore the code?** Check out the project on [GitHub](https://github.com/annnieglez/genai-travel-guide).",
        unsafe_allow_html=True,
    )
