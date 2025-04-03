'''This file groups functions for data cleaning in dataframes, such as 
    formatting columns to a consistent format. Also, it includes functions 
    to clean text data, remove timestamps, and create PDFs from JSON files.
    It also includes functions to scrape data from websites and Wikipedia 
    and create PDF file with the extracted information.'''

# Import necessary libraries

# Standard Libraries
import json
import re

# ReportLab for PDF generation
from reportlab.lib.pagesizes import letter  
from reportlab.lib.styles import getSampleStyleSheet  
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer  

# Web scraping and HTTP requests
import requests 
from bs4 import BeautifulSoup  

# Selenium for web automation and interaction
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options 
from webdriver_manager.chrome import ChromeDriverManager 

# Time module for managing delays
import time  

# ==============================
# Data Cleaning Functions
# ==============================

def convert_to_str(data_frame, columns):
    """
    Convert column to string

    Parameters:
        - data_frame (pd.DataFrame): The input DataFrame whose columns need to be formatted.

    Returns:
        - pd.DataFrame: DataFrame with input columns converted to str.
    """

    # If a single column is provided, convert it to a list
    if isinstance(columns, str):
        columns = [columns]

    # Iterate through the columns and convert them to string
    for col in columns:
        data_frame[col] = data_frame[col].astype(object)

    return data_frame

def convert_to_int(data_frame, columns):
    """
    Convert column to int

    Parameters:
        - data_frame (pd.DataFrame): The input DataFrame whose columns need to be formatted.

    Returns:
        - pd.DataFrame: DataFrame with input columns converted to str.
    """

    # If a single column is provided, convert it to a list
    if isinstance(columns, str):
        columns = [columns]

    # Iterate through the columns and convert them to int
    for col in columns:
        data_frame[col] = data_frame[col].astype(int)

    return data_frame

def drop_rows_with_nan(data_frame, columns):
    """
    Drops rows from the DataFrame where the specified column(s) have NaN values.

    Parameters:
        - data_frame (pd.DataFrame): The input DataFrame.
        - columns (str or list): Column name or list of column names to check for NaN values.

    Returns:
        - pd.DataFrame: A new DataFrame with the rows removed.
    """

    # Ensure columns is a list
    if isinstance(columns, str):
        columns = [columns]

    # Drop rows where any of the specified columns have NaN values
    data_frame = data_frame.dropna(subset=columns)

    return data_frame

def drop_col(data_frame, columns):
    """
    Drops specified columns from a DataFrame.
    
    Parameters:
        - data_frame (pd.DataFrame): The input DataFrame from which columns will be dropped.
        - columns (list or str): A list of column names or a single column name to be dropped.
    
    Returns:
        - pd.DataFrame: The DataFrame with the specified columns removed.
    """

    # Check for columns that do not exist in the DataFrame
    missing_cols = [col for col in columns if col not in data_frame.columns]

    # If there are missing columns, print a message and exclude them from the drop list
    if missing_cols:
        print(f"Warning: The following columns were not found and will be skipped: {', '.join(missing_cols)}")
        columns = [col for col in columns if col in data_frame.columns]  # Keep only existing columns
    
    # Drop the existing columns
    data_frame = data_frame.drop(columns, axis=1)

    return data_frame

def snake(data_frame):
    """
    Converts column names to snake_case (lowercase with underscores).
    
    Parameters:
        - data_frame (pd.DataFrame): The input DataFrame whose columns need to be formatted.

    Returns:
        - pd.DataFrame: DataFrame with column names in snake_case.
    """

    # Convert column names to snake_case
    data_frame.columns = [column.lower().replace(" ", "_").replace(")", "").replace("(", "") for column in data_frame.columns]

    return data_frame

def column_name(data_frame, columns, word_to_remove):
    """
    Formats columns name.

    Parameters:
        - data_frame (pd.DataFrame): The input DataFrame.
        - columns (list): List of column names to modify.
        - word_to_remove (str): The word to remove from the column names.

    Returns:
        - pd.DataFrame: The DataFrame with the updated column name.
    """

    for column in columns:
        # If the column exists in the DataFrame, remove the word from the column name
        if column in data_frame.columns:
            new_column = column.replace(word_to_remove, '')
            data_frame = data_frame.rename(columns={column: new_column})

    return data_frame

def drop_columns_with_prefix(dataframe, prefix):
    """
    Drops columns from a DataFrame whose names start with the given prefix.

    Parameters:
        - df (pd.DataFrame): The DataFrame to modify.
        - prefix (str): The prefix to match column names.

    Returns:
        - pd.DataFrame: A new DataFrame with the specified columns removed.
    """

    # Copy the DataFrame to avoid modifying the original
    df = dataframe.copy()

    # Get the list of columns to drop
    columns_to_drop = [col for col in df.columns if col.startswith(prefix)]
    df = drop_col(df, columns_to_drop)

    return df

def columns_with_missing_data(df):
    """
    Identifies columns in a DataFrame with more than 50% missing data.

    Parameters:
        - df (pd.DataFrame): The DataFrame to check for missing data.

    Returns:
        - list: A list of column names with more than 50% missing data.
    """
    
    # List to store columns with more than 50% missing data
    columns_with_missing = []
    
    # Iterate over each column
    for col in df.columns:
        # Calculate the percentage of missing values for the column
        missing_percentage = df[col].isnull().mean() * 100
        
        # If the missing percentage is greater than 50, add the column to the list
        if missing_percentage > 50:
            columns_with_missing.append(col)
    
    return columns_with_missing

def clean_text(text):
    """
    Remove newlines and excessive spaces from the text.

    Parameters:
        - text (str): The input text to clean.

    Returns:
        - str: The cleaned text.
    """

    if text is not None:
        return " ".join(text.split())
    else:
        return "No text available."

def remove_timestamps(subtitle):
    """
    Remove timestamps from subtitles using regex.
    
    Parameters:
        - subtitle (list): List of subtitle strings with timestamps.

    Returns:
        - cleaned_subtitles (str): Cleaned subtitle string without timestamp.
    """

    # Step 1: Remove the timestamp lines (anything matching the timecode format)
    cleaned_subtitles = re.sub(r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', '', subtitle)
    cleaned_subtitles = re.sub(r'\d+\n\d{2}:\d{2}:\d{1},\d{3} --> \d{2}:\d{2}:\d{1},\d{3}', ' ', cleaned_subtitles)
    cleaned_subtitles = re.sub(r'\d+\n\d{2}:\d{2}:\d{1},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', ' ', cleaned_subtitles)
    cleaned_subtitles = re.sub(r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{1},\d{3}', ' ', cleaned_subtitles)
    cleaned_subtitles = re.sub(r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:[a-zA-Z]+:[a-zA-Z]+,[a-zA-Z]+\n', ' ', cleaned_subtitles)
    cleaned_subtitles = re.sub(r'\d+\n\d{2}:\d{2}:\d{1},\d{3} --> \d{2}:[a-zA-Z]+:[a-zA-Z]+,[a-zA-Z]+\n', ' ', cleaned_subtitles)
    cleaned_subtitles = re.sub(r'\[Music\]', '', cleaned_subtitles)
    cleaned_subtitles = re.sub(r'\[Applause\]', '', cleaned_subtitles)

    # Step 2: Remove empty lines and extra newlines
    cleaned_subtitles = re.sub(r'\n+', ' ', cleaned_subtitles)

    # Step 3: Remove any remaining blank spaces or unnecessary characters
    cleaned_subtitles = cleaned_subtitles.strip()

    # Remove excessive spaces from the subtitles
    cleaned_subtitles = re.sub(r'\s{2,}', ' ', cleaned_subtitles)

    return cleaned_subtitles

def clean_text_text(text):
    """
    Clean the input text by removing unwanted characters and formatting.

    Parameters:
        - text (str): The input text to clean.

    Returns:
        - str: The cleaned text.
    """
    # Remove unwanted symbols
    text = re.sub(r'[\x7f]+', '', text)

    # Remove emojis and other non-text characters
    text = re.sub(r'[^\w\s,.\'\"!?-]', '', text)

    # Remove all URLs
    text = re.sub(r'http[s]?://\S+', '', text)

    # Remove timestamps (e.g., 0:00 - Iceland Intro)
    text = re.sub(r'\d{1,2}:\d{2} - [\w\s\(\)\&\.-]+', '', text)
    text = re.sub(r'\d{1,2}:\d{2}', '', text)

    # Optional: Remove unnecessary extra spaces and fix formatting
    text = re.sub(r'\n+', '\n', text)  
    text = re.sub(r'^\s*|\s*$', '', text)

    return text

def process_json_to_pdf(json_file, output_pdf):
    """
    Extract relevant data from JSON and save as a formatted PDF.
    
    Parameters:
        - json_file (str): Path to the input JSON file.
        - output_pdf (str): Path to save the output PDF file.

    Returns:
        - None: The function saves the PDF file and prints a success message.
    """

    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
        # Check if the JSON file name includes the word "youtube"
        if "youtube" in json_file.lower():
            print("Extracting data from the Youtube JSON files.")

            # Extract relevant data
            processed_videos = []
            for video in data:  

                # Extract information from the video
                title = clean_text(video.get("title", "Untitled"))
                text = clean_text_text(video.get("text", ""))
                subtitles_list = video.get("subtitles", [])
                
                # Check if subtitles_list is not empty and remove timestamps
                if subtitles_list != []:
                    subtitles = remove_timestamps(subtitles_list[0].get("srt", ""))
                else:
                    subtitles = []

                # Store processed video data
                processed_videos.append({
                    "title": title,
                    "text": text,
                    "subtitles": subtitles
                })

            # Create PDF from processed video data
            create_pdf(processed_videos, output_pdf, videos=True)

        # Check if the JSON file name includes the word "website"
        elif "website" in json_file.lower():
            print("Extracting data from the websites JSON files.")

            # Extract relevant data
            processed_websites = []
            for website in data:  
                
                # Extract information from the website
                metadata = website.get("metadata", [])
                
                # Check if metadata is not empty and extract title and description
                if metadata != []:
                    title = metadata.get("title", "Untitled")
                    description = metadata.get("description", "No description available.")
                else:
                    title = 'Untitled'
                    description = 'No description available.'

                # Extract text from the website
                text = clean_text(website.get("text", "No text available."))
                
                # Store processed website data
                processed_websites.append({
                    "title": title,
                    "description": description,
                    "text": text
                })         

            # Create PDF from processed website data
            create_pdf(processed_websites, output_pdf, websites=True)

def remove_wikipedia_references(text):
    """
    Removes Wikipedia-style references like [49], [5], or [100] from the given text.

    Parameters:
        - text (str): The text containing references.

    Returns:
        - cleaned_text (str): The cleaned text without references.
    """

    # Remove Wikipedia-style references (e.g., [1], [2], etc.)
    cleaned_text = re.sub(r'\[\d+\]', '', text)
    return cleaned_text

def scrape_wikipedia_to_pdf(url, output_pdf):
    """
    Scrapes all the text from a Wikipedia page and saves it as a PDF.

    Parameters:
        - url (str): The Wikipedia page URL to scrape.
        - output_pdf (str): Name of the output PDF file.

    Returns:
        - None: The function saves the PDF file and prints a success message.
    """

    print(f'Scraping Wikipedia page... {url}')

    # Extract relevant data
    processed_websites = []

    # Check if the URL is a valid Wikipedia page
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract the title
    title = soup.find("h1", {"id": "firstHeading"}).text.strip()
    
    # Extract all paragraph text from the main content
    content_div = soup.find("div", {"id": "mw-content-text"})

    paragraphs = content_div.find_all("p")
    content = "\n".join([p.text.strip() for p in paragraphs if p.text.strip()])
    content = remove_wikipedia_references(content)

    if not content:
        print("No content found on the page.")
        return

    # Store processed website data
    processed_websites.append({
        "title": title,
        "content": content
    })       

    # Create PDF from processed website data
    create_pdf(processed_websites, output_pdf, wikipedia=True)

def scrape_mgtripplanner(url, output_pdf):
    """
    Uses Selenium to scrape all the main content from the given URL.
    
    Parameters:
        - Extracts headers, paragraphs, and lists
        - Cleans text by removing extra spaces and references
    
    Returns:
        - None: The function saves the PDF file and prints a success message.
    """

    print(f"Scraping page... {url}")

    # Set up Selenium options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    # Launch the browser
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the page
    driver.get(url)
    time.sleep(15)  # Wait for the page to fully load

    # Extract page source and close the driver
    page_source = driver.page_source
    driver.quit()

    # Parse with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    extracted_text = ""

    # Find the title area 
    content_div = soup.find('div', {'class': 'content-wrapper'}) 

    if content_div:
        for element in content_div.find_all(['h1']):
            if element.name in ['h1']:
                extracted_text += f"\n\n{element.text.upper()}\n"

    # Find the main content area 
    content_div = soup.find('div', {'class': 'entry-content'}) 

    # Iterate through all relevant elements
    if content_div:
        for element in content_div.find_all(['h2', 'h3', 'h4', 'p', 'ul', 'ol']):
            if element.name in ['h2', 'h3', 'h4']:
                extracted_text += f"\n\n{element.text.upper()}\n"
            elif element.name == 'p':
                extracted_text += f"\n{element.text}\n"
            elif element.name in ['ul', 'ol']:
                for li in element.find_all('li'):
                    extracted_text += f" - {li.text}\n"

    # Remove extra spaces
    cleaned_text = extracted_text.strip()

    # Save the cleaned text to pass to the pdf function
    processed_data = []
    processed_data.append({"text": cleaned_text})
    create_pdf(processed_data, output_pdf, website_scrapped = True)

def create_pdf(processed_data, output_filename, videos=False, websites=False, wikipedia=False, website_scrapped = False):
    """
    Create a PDF from processed data.
    
    Parameters:
        - processed_data (list): List of dictionaries containing data.
        - output_filename (str): Path to save the output PDF file.
        
    Returns:
        - None: The function saves the PDF file and prints a success message.
    """

    # Create a PDF document
    doc = SimpleDocTemplate(output_filename, pagesize=letter)

    # Create a list to hold the elements of the document
    elements = []

    # Get the default style sheet
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    text_style = styles["BodyText"]
    subtitle_style = styles["Italic"]
    description_style = styles["Italic"]
    content_style = styles["Italic"]

    # Covert videos, websites, and Wikipedia data to pdf
    if videos == True:

        # Loop through each processed video and add content to the PDF
        for video in processed_data:
            title = video["title"]
            text = video["text"]
            subtitles = video["subtitles"]

            # Add title
            elements.append(Paragraph(title, title_style))
            elements.append(Spacer(1, 12))

            # Add text
            elements.append(Paragraph(text, text_style))
            elements.append(Spacer(1, 12))

            # Add subtitles
            if subtitles!= []:
                elements.append(Paragraph(subtitles, subtitle_style))
                elements.append(Spacer(1, 24))

    elif websites == True:

        # Loop through each processed website and add content to the PDF
        for website in processed_data:
            title = website["title"]
            description = website["description"]
            text = website["text"]

            # Add title
            elements.append(Paragraph(title, title_style))
            elements.append(Spacer(1, 12))

            # Add description
            if description != 'No description available.' and description != None:
                elements.append(Paragraph(description, description_style))
                elements.append(Spacer(1, 12))

            # Add text
            if text != '' and text != None:
                elements.append(Paragraph(text, text_style))
                elements.append(Spacer(1, 24))

    elif wikipedia == True:

        title = processed_data[0]["title"]
        content = processed_data[0]["content"]

        # Add title
        if title != '':
            elements.append(Paragraph(title, title_style))
            elements.append(Spacer(1, 12))
        
        # Add content
        if content != '':
            elements.append(Paragraph(content, content_style))
            elements.append(Spacer(1, 12))     

    elif website_scrapped == True:

        elements.append(Paragraph(processed_data[0]["text"], text_style))
        elements.append(Spacer(1, 12))
        
    if elements != []: 
        # Build the PDF
        doc.build(elements)
        print(f"PDF created: {output_filename}")


