'''This script implements a Retrieval-Augmented Generation (RAG) 
    system using ChromaDB and OpenAI's GPT-4o model.'''

# Import necessary libraries

# Standard Libraries
import pickle 
import os

# External Libraries
import chromadb 
import openai  
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
client_openai = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Custom Libraries
from genai_scripts import data_storage as ds  

#  ChromaDB setup
folder_db = "../chroma_db"
client = chromadb.PersistentClient(path=folder_db)
collection = client.get_collection(name="csv_embeddings")

# Cached embeddings (for faster retrieval)
cache_file = "../chroma_db/query_embeddings_cache.pkl"
try:
  with open(cache_file, "rb") as f:
          query_cache = pickle.load(f)
except FileNotFoundError:
    query_cache = {}

# ==============================
# GenAi Functions
# ==============================

def retrieve_relevant_chunks(query, top_k=10):
    """
    Retrieve the most relevant chunks from ChromaDB based on query

    Parameters:
      - query (str): The query string to search for in the database.
      - top_k (int): The number of top results to return. Default is 10.

    Returns:
      - list: A list of the most relevant chunks from the database.
    """

    # Check if the query is already cached
    if query in query_cache:
        # If the query is cached, use the cached embedding
        query_embedding = query_cache[query]
    else:
        # If not cached, generate a new embedding and cache it
        query_embedding = ds.generate_embedding(query)
        query_cache[query] = query_embedding

        # Save the cache to file
        with open(cache_file, "wb") as f:
            pickle.dump(query_cache, f)

    # Query the ChromaDB collection for the most relevant chunks
    results = collection.query(
        query_embeddings=[query_embedding],  
        n_results=top_k 
    )

    # Extract text from results
    retrieved_chunks = [meta["text"] for meta in results["metadatas"][0] if "text" in meta]

    return retrieved_chunks

def generate_response_from_gpt4o(test = False, question = None, app = False):
    """
    Generate a response from GPT-4o based on user input and retrieved chunks from ChromaDB.

    Parameters:
        - test (bool): Flag to indicate if the function is being run in test mode.
        - question (str): The user's question.
        - app (bool): Flag to indicate if the function is being run in app mode.

    Returns:
        If test is True:
            - str: The generated response from GPT-4o.
        If app is True:
            - prompt (str): The generated prompt for GPT-4o.
        If test and app are False:
            - None: The function prints the response in real-time.
    """

    # Check if the function is being run in test mode or app mode
    # If test is True, use the provided question instead of user input
    if test == False and app == False:
        # Get user input
        query = input("Enter your query: ") 
    else:
        query = question
        print(f"Query: {query}")

    # Check for specific queries to generate custom responses
    if "hello" in query.lower():
        prompt = '''Always respond with:
                    Hello! I'm your travel chatbot! Here's a fun joke: Why don’t skeletons fight each other? They don’t have the guts! 😄'''
    elif "who are you" in query.lower():
        prompt = '''Always respond with:
                    I am a travel chatbot! I can help you find great places to visit, give you recommendations, and more!'''
    elif "what is your name" in query.lower():
        prompt = '''Always respond with:
                    Hmm, I don’t have a name... I know, it's a bit sad! What’s your name? Maybe you could name me! 😊'''
    else:
        # Retrieve relevant chunks from ChromaDB based on the query
        retrieved_chunks = retrieve_relevant_chunks(query)

        # Format the retrieved chunks for the prompt
        context = "\n\n".join(retrieved_chunks)  # Format retrieved chunks

        # Create the prompt for GPT-4o
        prompt = f"""
        You are an AI assistant answering user questions based **only on the retrieved database information**.
      
        {context}

        If the information is not in the retrieved information, respond with: 
        *"I don't have that information at the moment. This is a work-in-progress app, so check back soon for more updates! Is there anything else I can help you with?"*

        When answering, follow these structured guidelines:

        ## **Answering Guidelines**:
        - **Provide links when available** (e.g., restaurant websites, tour bookings, car rentals).
        - **Always include addresses** for hotels and restaurants if available.
        - **Mention opening hours** if available for restaurants.
        - **Give an overview** of places, towns, or activities when relevant.
        - **Budget-Specific Requests**:  
            - If the query asks for budget-friendly options, show only cheap/moderate choices.
            - If the query is general, provide options across different price ranges.

        ## **Category-Specific Responses**:
        - **Restaurants**: Name, type of cuisine, price range (cheap, moderate, expensive), address (if available), opening hour (if available)s, and website (if available).
        - **Hotels**: Name, location, price category (if available), and booking link (if available).
        - **Activities & Tours**: Overview of the experience, location (if available), tour reviews (e.g., 2, 3.5, 4 stars) (if available), and booking link (if available).
        - **Transportation & Car Rentals**: Overview, price category (if available), rental locations, and relevant links.
        - **Itineraries**: Provide key highlights, duration, and locations covered.
        - **General Information & News**: Summarize concisely while ensuring relevance to the query.

        Now, using **only the provided database information**, answer the following query:

        {query}
        """

    # Check if the function is being run in test mode or app mode
    # If test and app are False , stream the response
    # If test is True, generate the response without streaming
    # If app is True, return the retrieved chunks and the prompt
    if test == False and app == False:
        # Generate the response using GPT-4o
        response = client_openai.chat.completions.create(
          model="gpt-4o",
          messages=[{"role": "system", "content": "You are an AI assistant restricted to answering questions only from the database."},
                    {"role": "user", "content": prompt}],
          temperature=0.7,
          stream=True
          )
        
        # Print the response in real-time
        for chunk in response:
            content = getattr(chunk.choices[0].delta, "content", None)
            if content:
                print(content, end="", flush=True)
    if test == True:
        # Generate the response using GPT-4o
        response = client_openai.chat.completions.create(
          model="gpt-4o",
          messages=[{"role": "system", "content": "You are an AI assistant restricted to answering questions only from the database."},
                    {"role": "user", "content": prompt}],
          temperature=0.7
          )
        return response.choices[0].message.content
    if app == True:
        return prompt


def llm_as_judge(question):
    """
    Evaluate the quality of the AI's answer using GPT-4o as a judge.

    Parameters:
        - question (str): The user's question.
        - retrieved_chunks (str): The context retrieved from the database.
        - rag_answer (str): The AI's generated answer.

    Returns:
        - str: The evaluation result from the judge.
    """

    # Retrieve relevant chunks from ChromaDB based on the question
    retrieved_chunks = retrieve_relevant_chunks(question)

    # Format the retrieved chunks for the prompt
    rag_answer = generate_response_from_gpt4o(True, question)

    # Create the judge prompt
    judge_prompt = f"""
    You are an expert evaluator. You will assess the answer quality of an AI system.

    **Context from the database:**
    {retrieved_chunks}

    **User's Question:**
    {question}

    **AI's Answer:**
    {rag_answer}

    Evaluate the answer based on:
    - **Correctness** (Does it match the database info?)
    - **Completeness** (Does it include all relevant details?)
    - **Conciseness** (Is it clear and to the point?)

    Provide a score (1-10) based on accuracy, completeness, and conciseness.
    The explanation should follow the following structure and be separated with proper line breaks between each section::

    **Score:** [Score]

    **Explanation:**
    - **Correctness:** [Evaluation of correctness]
    - **Completeness:** [Evaluation of completeness]
    - **Conciseness:** [Evaluation of conciseness]

    **Final Note:** [Conclude with any necessary explanation of errors, if present]

    Now, please evaluate the response.
    """

    # Generate the evaluation using GPT-4o
    response = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a strict and fair AI judge evaluating another AI's response."},
                  {"role": "user", "content": judge_prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content
