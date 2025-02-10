##########################################
###          HELPER FUNCTIONS          ###
##########################################

from lyricsgenius import Genius
import json
import re
import os
import en_core_web_sm
import ca_core_news_sm
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# Token created by signing up to the Genius webside and creating an API Client (test)
GENIUS_TOKEN = "aQG9ku91tE-n1eZmmdX9tPoiXBKncDLiom-NZi_ctt-pHcdCucDWyyNO6czJzLuK"

def get_lyrics_data_from_artist(artistName: str, nTop: int = 5) -> list:
    '''
    Decide if we need to call the Genius API to collect the lyrics or 
    if there is already a json file with the raw lyrics available.

    artistName: the name of the artist or group from whom we obtain the lyrics
    nTop: max number of songs, default = 5
    Returns a list of lyrics 
    '''
    print("get_lyrics_data_from_artist - init")
    # Define file name (remove spaces in artist name)
    filename = re.sub(r'\s', '', artistName) + "_raw_lyrics.json"

    try:
        # Check if json file exists
        if os.path.isfile(filename):
            # Open json file and load text
            lyrics_list = load_raw_lyrics_from_json(filename)
        else:
            # File not found
            print("File not found. Call Genius API")
            #Open connection to Genius API - to extract song lyrics
            genius = open_genius_api()
            # Search by artist - return top list of song lyrics
            lyrics_list = get_top_lyrics_by_artist(genius, artistName, nTop) 
            # Save data into json file
            save_raw_lyrics_to_json(lyrics_list, filename)
        return lyrics_list
    except:
        raise Exception('''Cannot continue. Json file with raw lyrics is not found and Genius API returned error code. 
            No lyrics to process. Download json files and try again.''')
    finally:
        print("get_lyrics_data_from_artist - end")

def open_genius_api():
    '''
    Open connection to the Genius API (lyrics provider)
    Returns genius object
    '''
    print("open_genius_api - init")
    # Open Genius API
    genius = Genius(GENIUS_TOKEN, remove_section_headers=True, skip_non_songs=True)
    print("open_genius_api - end")
    return genius

def get_top_lyrics_by_artist(genius: Genius, artistName: str, nTop: int = 5) -> list:
    '''
    Get n top songs from artist and put the lyrics in a list ordered by popularity
    genius: the object to connect to the Genius API
    artistName: the name of the artist or group from whom we obtain the lyrics
    nTop: max number of songs, default = 5
    Returns list of song lyrics
    '''
    print("get_top_lyrics_by_artist - init")
    # Open Genius API
    open_genius_api()
    lyrics = []
    # Genius API: Extract nTop songs from given artistName
    artist_genius = genius.search_artist(artistName, max_songs=nTop)
    songs = artist_genius.songs
    # For each song of the artist, get lyrics and append to list
    for song in songs:
        if song is not None:
            lyrics.append(song.lyrics)
    print("get_top_lyrics_by_artist - end")
    return lyrics

def save_raw_lyrics_to_json(raw_lyrics: list, filename: str):
    '''
    Save raw data extracted directly from the Genius API into a json file.

    raw_lyrics: list of strings containing the raw text of the lyrics
    filename: name of the file
    '''
    print("save_raw_lyrics_to_json - init")
    # Open file in write mode and add raw_lyrics in json format
    with open(filename, 'w') as file:
        json.dump(raw_lyrics, file)
    print("save_raw_lyrics_to_json - end")

def load_raw_lyrics_from_json(filename: str):
    '''
    Load raw data from json file.

    filename: name of the file
    Returns list of strings containing the raw text of the lyrics
    '''
    print("load_raw_lyrics_from_json - init")
    # Open json file and load text
    with open(filename, 'r') as jfile:
        lyrics = json.load(jfile)
    print("load_raw_lyrics_from_json - end")
    return lyrics

def process_and_clean_lyrics(lyrics: list) -> str:
    '''
    Process list of song lyrics and returns a cleaner single string for all the lyrics
    Each lyric contains the text twice, full lyrics and then repetition, the separation between 
    the two is the element \\d{0,3}Embed
    E.g.: I have the power to make my evil take its course17Embed\\nWoe to you, o'er Earth and Sea
    E.g.: Fly to live, aces high8Embed\\n\\nThere goes the siren that warns of the air raid
    E.g.: És bonica i és tot el que tinc Embed\\nPotser és massa aviat

    lyrics: list of all lyrics to process
    Returns string of all processed lyrics concatenated
    '''
    print("process_and_clean_lyrics - init")
    all_lyrics_str = ''
    # Process each lyric from the list
    for lyric in lyrics:
        # Remove first part until \d{0,3}Embed, DOTALL makes the dot also match newline character
        txt = re.sub(r'^.*?\d{0,3}Embed', '', lyric, flags=re.DOTALL)
        # Convert all types of whitespace chars (like newlines) into a space
        txt = re.sub(r'\s', ' ', txt)
        # Lowercase all text
        txt = txt.lower()
        # Accumulate lyrics in the string
        all_lyrics_str += txt
    
    # Substitute 2 or more consecutive whitespace chars for just one space
    all_lyrics_str = re.sub(r'\s{2,}', ' ', all_lyrics_str)
    print("process_and_clean_lyrics - end")
    return all_lyrics_str
    
def tokenize_text(text: str, lang: str = 'en') -> list:
    '''
    Returns the tokenized input text.
    Tokenize text then remove punctuation and whitespace

    text: input string to tokenize
    lang: language of the input text ['en', 'ca']. Default = 'en'
    Returns list of tokens after removing punctuation and whitespace
    '''
    print("tokenize_text - init")
    # Prepare spacy language model to tokenize text
    if(lang == 'ca'):
        nlp = ca_core_news_sm.load()
    else:
        nlp = en_core_web_sm.load()

    # Tokenize text
    doc = nlp(text)
    # Create list of tokens, excluding punctuation and whitespace
    token_text = [token.text for token in doc 
                    if not token.is_punct and not token == ' ']
    print("tokenize_text - end")
    return token_text

def get_dataframe(token_text: list) -> pd.DataFrame:
    '''
    Create a pandas DataFrame from the list of tokens.

    token_text: list of tokens
    Returns DataFrame with 3 columns: Token, Frequency and Length (of the token)
    '''
    print("get_dataframe - init")
    # Count instances of each token
    freq_list = Counter(token_text)
    # Order by most frequent - without any argument, this function returns the complete list ordered by desc frequency
    freq_list = freq_list.most_common()

    # Create DataFrame from list of tuples, with column names
    df = pd.DataFrame(freq_list, columns=['Token', 'Frequency'])
    # Calculate length of each token and create a new column in the DF
    df['Length'] = df['Token'].apply(lambda row: len(row))
    # Remove any word that is longer than 20 characters (issue of formatting)
    df = df[df['Length']<20]
    print("get_dataframe - end")
    return df

def plot_length_frequency(length_coords: pd.Series, freq_coords: pd.Series, lang: str):
    '''
    Print the scatter plot of length (x-axis) and frequency (y-axis)

    length_coords: data for the x-axis (length of tokens)
    freq_coords: data for the y-axis (frequency of tokens)
    lang: language to display as the title of the plot
    '''
    print("plot_length_frequency - init")
    plt.scatter(length_coords, freq_coords)
    plt.title(lang)
    plt.xlabel("Length")
    plt.ylabel("Frequency")
    plt.show()
    print("plot_length_frequency - end")