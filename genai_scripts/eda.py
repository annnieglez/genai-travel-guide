""" This file contains functions for exploratory data analysis (EDA) on the chunks of text data."""

# Import necessary libraries

# standard libraries
import os

# Visualization Libraries
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from matplotlib import font_manager

# Load tokenizer for GPT model
import tiktoken
encoding = tiktoken.encoding_for_model('gpt-4o-mini')

# Custom Libraries
from genai_scripts import data_storage as ds

# ==============================
# Directory Setup
# ==============================

# Define the directory name for saving images
OUTPUT_DIR = "../images"

# Check if the directory exists, if not, create it
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# ==============================
# Plot Styling & Customization
# ==============================

# Set a Minimalist Style
sns.set_style("whitegrid")

# Customize Matplotlib settings for a modern look
mpl.rcParams.update({
    'axes.edgecolor': 'grey',       
    'axes.labelcolor': 'black',     
    'xtick.color': 'black',         
    'ytick.color': 'black',         
    'text.color': 'black'           
})

# General color palette for plots
custom_colors = ["#8F2C78", "#1F4E79"]

# ==============================
# Font Configuration
# ==============================

# Path to the custom font file
FONT_PATH = '../genai_scripts/fonts/Montserrat-Regular.ttf'

# Add the font to matplotlib's font manager
font_manager.fontManager.addfont(FONT_PATH)

# Set the font family to Montserrat
plt.rcParams['font.family'] = 'Montserrat'

# ==============================
# EDA Functions
# ==============================

def plot_combined_chunk_size_distribution(chunks_dict, key_word='', color = 1):
    """
    Plots the distribution of chunk sizes for all chunks in the given dictionary.

    Parameters:
        - chunks_dict (dict): A dictionary where keys are file names and values are lists of chunks.

    Returns:
        - None: Displays a histogram of chunk sizes.
    """

    # Flatten the list of chunk lengths from all files in the dictionary
    # For PDF chunks
    all_chunk_lengths = [
        len(chunk.page_content) if hasattr(chunk, 'page_content') else len(chunk)  
        for chunks in chunks_dict.values() for chunk in chunks
    ] 
    # For CSV chunks
    all_chunk_token_lengths = [
        len(encoding.encode(chunk.page_content)) if hasattr(chunk, 'page_content') else len(encoding.encode(chunk))
        for chunks in chunks_dict.values() for chunk in chunks
    ]

    # Create side-by-side plots
    fig, axs = plt.subplots(1, 2, figsize=(16, 6))  # 1 row, 2 columns

    # Plot chunk size distribution (characters) on the first subplot
    axs[0].hist(all_chunk_lengths, bins=50, edgecolor='black', alpha=0.7, color=custom_colors[color])
    axs[0].set_xlabel("Chunk Length (Characters)")
    axs[0].set_ylabel("Frequency")
    axs[0].set_title(f"Chunk Size Distribution (Characters) {key_word.replace(' - ', ' ').replace(':', '').title().replace('Csv', 'CSV').replace('Pdf', 'PDF')}")
    axs[0].grid(linestyle='--', axis='both', alpha=0.3)
    axs[0].set_xlim(left=0) 

    # Plot chunk size distribution (tokens) on the second subplot
    axs[1].hist(all_chunk_token_lengths, bins=40, edgecolor='black', alpha=0.7, color=custom_colors[color])
    axs[1].set_xlabel("Chunk Length (Tokens)")
    axs[1].set_ylabel("Frequency")
    axs[1].set_title(f"Chunk Size Distribution (Tokens) {key_word.replace(' - ', ' ').replace(':', '').title().replace('Csv', 'CSV').replace('Pdf', 'PDF')}")
    axs[1].grid(linestyle='--', axis='both', alpha=0.3)
    axs[1].set_xlim(left=0) 

    # Token limit line for OpenAI API
    axs[1].axvline(x=8000, color='red', linestyle='--', linewidth=2, label='Threshold: 8192')

    # Adjust layout to avoid overlapping labels
    plt.tight_layout()

    # Save the figure
    plt.savefig(os.path.join(OUTPUT_DIR, f"chunk_size_distribution_{key_word.replace(' - ', ' ').replace(':', '').replace(' ', '_')}.png"), 
                bbox_inches='tight', 
                facecolor='none', 
                transparent=True)

    # Show the plot
    plt.show()

def plot_chunk_size_analysis(folder, chunk_sizes, overlaps):
    """
    Analyzes and visualizes the chunk size distribution for CSV and PDF files in the specified folder.
    
    Parameters:
        - folder (str): The folder containing the CSV and PDF files.
        - chunk_sizes (list): A list of chunk sizes to analyze.
        - overlaps (list): A list of overlap sizes to analyze.
        
    Returns:
        - None: Displays the chunk size distribution plots.
    """

    # Iterate through each combination of chunk size and overlap 
    for size in chunk_sizes:
        for overlap in overlaps:
            print(f"\nProcessing chunk size: {size}, overlap: {overlap}")

            # Process and chunk CSV files
            chunks_dict_csv = ds.process_and_chunk_csv_files(folder, size=size, overlap=overlap)

            # Process and chunk PDF files
            chunks_dict_pdf = ds.process_and_chunk_pdf_files(folder, size=size, overlap=overlap)

            # Plot the chunk size distribution for CSV files
            plot_combined_chunk_size_distribution(chunks_dict_csv, f'CSV files - chunk size: {size} - overlap: {overlap}', 0)

            # Plot the chunk size distribution for PDF files
            plot_combined_chunk_size_distribution(chunks_dict_pdf, f'PDF files - chunk size: {size} - overlap: {overlap}', 1)
    
    print("Chunk size analysis completed.")