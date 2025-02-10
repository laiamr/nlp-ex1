# nlp-ex1
Exercise 1 for NLP UPF 2025 class<br>
Authors: Júlia Malet and Laia Marsó

**CODE**<br>
**utils.py** is a module for helper functions, it will be imported by the other file.

**Exercise 1.ipynb** is the main file. It's a Jupyter notebook file to more easily visualize slices of dataframes and plots.
It contains the code for English and then for Catalan.<br>
Obtains song lyrics (first time from Genius API, then from text file if it exists), cleans them and tokenizes them.
Then checks most frequent elements and plots a token length and frequency scatterplot

**DATA**<br>
**IronMaiden_raw_lyrics.json** contains raw lyrics data for English (Iron Maiden songs)<br>
**ElsPets_raw_lyrics.json** contains raw lyrics data for Catalan (Els Pets songs)

**WARNING**<br>
We use Genius Client API to download song lyrics from Genius.com. However, the Client API does not seem to work for other people, even locally (only for the programmer). That is the reason we provide the json files with the raw data. They have the same format as what was downloaded from the web, no processing has been done on them yet.

**REQUIREMENTS**<br>
This is a list of modules needed to install in order to correctly execute this project
- lyricsgenius: package to call the Genius API, to download song lyrics from the web Genius.com
- en_core_web_sm: English language model, to tokenize English text
- ca_core_news_sm: Catalan language model, to tokenize Catalan text
- pandas: to manage dataframes
- matplotlib: to visualize plots

System libraries:
- re: regular expressions module
- collections -> Counter: count instances of elements in a list
- os: deal with file management (open and save text files)
- json: load lyrics data from json files
