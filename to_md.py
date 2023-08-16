import csv
import chardet
from unidecode import unidecode

def generate_library_md(books_per_row, books_per_page):

    # Read CSV file
    with open('library.csv', 'r', encoding='utf-8-sig') as f:  
        reader = csv.DictReader(f)
        books = list(reader)


    markdown = "---\n\nlayout: page\n\n---\n\n"

    

        # Generate Markdown for each book
    for book in books:

                markdown += "> "  
                markdown += f"**{book['TITOLO']}**\n"
                markdown += f"*{book['AUTORE']}*\n"
                
                if book['cover']:
                    book['cover_url'] = book['cover']
                else:
                    book['cover_url'] = 'data/placeholder.webp'
                
                markdown += "![Book Cover](" + str(book['cover_url']) + ")\n"

    # Return Markdown string
    return unidecode(markdown.replace(u"\u2019", "'"))


md = generate_library_md(3, 21)
with open("book_library.markdown", 'w') as f:
    f.write(md)