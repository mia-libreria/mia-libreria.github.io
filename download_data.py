from functools import cache
from logging import Logger
import pandas as pd
import isbnlib as isb
import requests
from html2text import html2text
import re

#return the most probable isbn id given words
@cache
def get_id(words):
    #Use Google to get an ISBN from words from title and author's name.
    words = str(words)
    service_url = 'http://www.google.com/search?q=ISBN+'
    search_url = service_url + (words.replace(' ', '+'))

    req = requests.get(search_url)
    if(req.status_code != 200):
        print("Couldn't connect with the server")
        return -1
    
    # Define the regular expression pattern for an ISBN-13 with or without dashes
    pattern = r'\b97[89][-\s]?\d{1,5}[-\s]?\d{1,7}[-\s]?\d{1,6}[-\s]?\d\b'
    content = html2text(req.text)
   
    pos = content.find("ISBN-13")
    
    isbn_id = content[pos+9: pos+23]
    print(isbn_id)
    if(not isb.is_isbn13(str(id))):
        # Search for the pattern in the text
        match = re.search(pattern, content)
        print(match)
        if(match):
            isbn_id = match.group()
            print("Found with regex! ISBN =" + str(isbn_id))
        if(not isb.is_isbn13(str(isbn_id))):
            #print('isbn13 code not found trying with ibsnlib')
            #isbn_id = isb.isbn_from_words(words)
            if(not isb.is_isbn13(str(isbn_id))):
                return -1
        return isbn_id
        
    print('found the correct isbn_id')
    return isbn_id
    

#return the description given an isbn id
def get_description(id):
    return isb.desc(id)

#return the url of the cover given an isbn id
def get_cover(id):
    cover_urls = isb.cover(id)
    if(not cover_urls):
        return ""
    return cover_urls['thumbnail']
    
def download_data():        
    df = pd.read_csv('library.csv', delimiter=',')

    
    for index, row in df.iterrows():
        title = row['TITOLO']
        if(isb.is_isbn13(row['ISBDN-13'])):
            #print('skipped '+ str(title))
            continue
        isbn13 = get_id(title)
        if(isbn13 == -1): 
            print('isbn not found for '+ str(title))
            continue
        df.at[index, 'ISBDN-13'] = isbn13
        df.at[index, 'description'] = get_description(isbn13)
        df.at[index, 'cover'] = get_cover(isbn13)
        df.to_csv('library.csv')

    df.to_csv('library.csv')


def download_author(id):
    data = isb.meta(id, service='goob')
    print(data)
#download_data()

download_author('978-8804668237')