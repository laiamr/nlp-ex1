# nlp-ex1
Exercise 1 for NLP UPF 2025 class<br>
Authors: Júlia Malet and Laia Marsó

This project has 2 files:

**utils.py** is a module for helper functions, it will be imported by the other file.

**Exercise 1.ipynb** is the main file. It's a Jupyter notebook file to more easily visualize slices of dataframes and plots.
It contains the code for English and then for Catalan.

Obtains song lyrics (first time from Genius API, then from text file if it exists), cleans them and tokenizes them.
Then checks most frequent elements and plots a token length and frequency scatterplot

**REQUIREMENTS**

This is a list of modules needed to install in order to correctly execute this project
- lyricsgenius: package to call the Genius API, to extract song lyrics directly without scraping
- spacy: package used to tokenize the text
- en_core_web_sm: English language model, to tokenize English text
- ca_core_news_sm: Catalan language model, to tokenize Catalan text
- pandas: to manage dataframes
- matplotlib: to visualize plots

System libraries:
- re: regular expressions module
- collections -> Counter: count instances of elements in a list
- os: deal with file management (open and save text files)
