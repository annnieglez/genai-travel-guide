'''The script includes functions to process and chunk the data into 
    manageable pieces. This script is responsible for generating and 
    storing the embeddings from the CSV and PDF files in the specified 
    folder. It uses OpenAI's API to generate the embeddings and stores 
    them in ChromaDB.'''

# Import necessary libraries

# Standard Libraries
import os  

# Data Handling Libraries
import pandas as pd 

# OpenAI Library
from openai import OpenAI 

# ChromaDB Library
import chromadb  

# Environment Management
from dotenv import load_dotenv 

# LangChain Libraries (for text processing and document loading)
from langchain.text_splitter import RecursiveCharacterTextSplitter  
from langchain_community.document_loaders import PyPDFLoader 

# Load environment variables from .env file
load_dotenv()  
api_key = os.getenv("OPENAI_API_KEY") 
user = OpenAI(api_key=api_key) 

# ChromaDB Setup
folder_db = "..\chroma_db" 
client = chromadb.PersistentClient(path=folder_db) 

# Optimize ChromaDB for faster vector search by setting indexing parameters
try:
    # New collection with optimized parameters
    collection = client.create_collection(
        name="csv_embeddings", 
        metadata={"index_type": "hnsw", "ef_construction": 200, "M": 16}  
    )
except chromadb.errors.UniqueConstraintError:
    # If the collection already exists, fetch the existing collection
    collection = client.get_collection(name="csv_embeddings")

# ==============================
# Chunks and Data Storage Functions
# ==============================

def process_and_chunk_csv_files(folder, chunks = {}, size = 10000, overlap = 100):
    """
    Process CSV files in a folder and chunk them into manageable pieces."
    
    Parameters:
        - folder (str): The path to the folder containing CSV files.

    Returns:
        - dict: A dictionary where keys are file names and values are lists of chunks.
    """
       
    # Automatically detect all CSV files in the folder
    filenames = [f for f in os.listdir(folder) if f.endswith('.csv')]
    
    for filename in filenames:
        # Construct the full file path
        file_path = os.path.join(folder, filename)
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Chunk the DataFrame and store the chunks in a dictionary
        chunks[filename] = chunk_dataframe(df, size=size, overlap=overlap)
    
    return chunks

def process_and_chunk_pdf_files(folder, chunks = {}, size = 10000, overlap = 100):
    """
    Process PDF files in a folder and chunk them into manageable pieces using LangChain.
    
    Parameters:
        - folder (str): The path to the folder containing PDF files.

    Returns:
        - dict: A dictionary where keys are file names and values are lists of chunks.
    """
    
    # Automatically detect all PDF files in the folder
    filenames = [f for f in os.listdir(folder) if f.endswith('.pdf')]
    
    for filename in filenames:
        # Construct the full file path
        file_path = os.path.join(folder, filename)
        
        # Use LangChain's PyPDFLoader to load and split the PDF
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()
        
        # Extract text chunks from the documents
        chunks[filename] = chunk_pages(pages, size=size, overlap=overlap)
    
    return chunks

def chunk_pages(pages, size, overlap):
    """
    Splits the pages into manageable chunks.

    Parameters:
        - pages (list): The list of pages from the pdf.
        - chunk_size (int): The maximum size of each chunk.

    Returns:
        - list: A list of text chunks.
    """

    # Use the RecursiveCharacterTextSplitter to split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,  
        chunk_overlap=overlap     
    )

    document_chunks = text_splitter.split_documents(pages)

    return [chunk.page_content for chunk in document_chunks]

def chunk_dataframe(dataframe, size, overlap):
    """
    Splits the DataFrame into manageable chunks.

    Parameters:
        - dataframe (pd.DataFrame): The DataFrame to be chunked.
        - chunk_size (int): The maximum size of each chunk.

    Returns:
        - list: A list of text chunks.
    """

    # Replace NaN values with an empty string
    dataframe = dataframe.fillna("")

    # Convert each row into a string without index values
    text_rows = dataframe.apply(lambda row: " ".join(row.astype(str)), axis=1).tolist()

    # Join all rows into a single text string
    text = "\n".join(text_rows)

    # Use the RecursiveCharacterTextSplitter to split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,  
        chunk_overlap=overlap      
    )

    return text_splitter.split_text(text)

def generate_embedding(text):
    """
    Generates an embedding for the given text using OpenAI's API."

    Parameters:
        - text (str): The text to be embedded.

    Returns:
        - list: The generated embedding.
    """

    # Check if the text is from the cvs or pdf file
    # and calculate the length accordingly.
    if hasattr(text, 'page_content'):
         len_text = len(text.page_content.split())
    else:
         len_text = len(text.split())

    # Check if the text length exceeds the maximum token limit for OpenAI's API
    if len_text > 8000: 
        raise ValueError("Chunk too large! Reduce chunk size before embedding.")   

    # Generate the embedding using OpenAI's API 
    response = user.embeddings.create(
        input=text,
        model="text-embedding-3-large"
    )

    return response.data[0].embedding

def store_chunks_in_chromadb(chunks, dataset_name):
    """
    Stores the generated chunks in ChromaDB.
    
    Parameters:
        - chunks (dict): A dictionary where keys are file names and values are lists of chunks.
        - dataset_name (str): The name of the dataset to be used as a prefix for chunk IDs."

    Returns:
        - None
    """

    # Iterate over files and their corresponding chunks
    for file_name, chunk_list in chunks.items():
        for i, chunk in enumerate(chunk_list):  # Iterate over the chunks for each file
            
            # Generate embedding for the chunk
            embedding = generate_embedding(chunk)

            # Store in ChromaDB
            collection.add(
                ids=[f"{dataset_name}_{file_name}_chunk_{i}"],  # Include file name for uniqueness
                embeddings=[embedding],
                metadatas=[{
                    "chunk_index": i,
                    "dataset": dataset_name,
                    "file_name": file_name,
                    "text": str(chunk)
                }]
            )

    print("Data stored successfully in ChromaDB!")