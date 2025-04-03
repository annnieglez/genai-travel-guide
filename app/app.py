'''This is a Streamlit application for an Iceland Travel AI Assistant.'''

# Import necessary libraries

import streamlit as st
from genai_scripts import GenAI_RAG as rag

def main():

   # Set the page configuration
    st.set_page_config(page_title="Iceland Travel AI Assistant", layout="wide")

    # Centering the image and title

    col1, col2, col3 = st.columns([6.2,4,4])
    with col2:  
        # Logo
        st.image("./images/mg-trip-planner-logo.png", width=200)

    col1, col2, col3 = st.columns([2.5,3,2])
    with col2:  
        # Title
        st.title("Iceland Travel AI Assistant ✈️")

    # Input Section
    query = st.text_input("Ask me anything about travel to Iceland:")

    if st.button("Search"):
        if query:

            # Retrieve the answer using the RAG model
            st.write("Searching...")
            generated_answer = rag.generate_response_from_gpt4o(test = False, question = query, app = True)

            st.subheader("AI's Response:")
            st.markdown(f"**Answer:** {generated_answer}")

            # Provide links to additional resources
            st.markdown("[Learn More About Iceland](https://www.mgtripplanner.com/)")
        else:
            st.warning("Please enter a query before searching.")

    # Footer Section
    st.markdown("---")
    st.markdown("Created by [Annie Meneses Gonzalez](https://your-website-link.com).") 
    st.markdown("For more travel tips and guides, follow me on [Instagram](https://instagram.com/yourprofile).") 

if __name__ == "__main__":
    main()