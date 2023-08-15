import csv
from bs4 import BeautifulSoup

def generate_library_html(books_per_row, books_per_page):
    # Read the CSV file with correct encoding
    with open('library2.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        books = list(reader)

    # Calculate the number of rows and pages based on the parameters
    num_rows = (len(books) + books_per_row - 1) // books_per_row
    
    # Create the HTML page
    soup = BeautifulSoup('<html><head></head><body></body></html>', 'html.parser')
    body = soup.body
    head = soup.head

    search = soup.new_tag('input', id='search', type='text', placeholder='Search') 
    results_div = soup.new_tag('div', id='results')

    body.append(search)
    body.append(results_div)
    
    script = soup.new_tag('script')

    script.string = """
    function searchBooks() {
      // Get search value
      var query = document.getElementById('search').value.toLowerCase();
      
      // Get all books
      var books = document.getElementsByClassName('book');
      

      
      // Loop through books and hide non-matches
      for (var i = 0; i < books.length; i++) {
        var author = books[i].querySelector('.author').innerText.toLowerCase();
        var title = books[i].innerText.toLowerCase();
        var authorMatch = author.includes(query);
        var titleMatch = title.includes(query)
        if (titleMatch || authorMatch) {
          books[i].style.display = 'block';
        } else {
          books[i].style.display = 'none'; 
        }
      }
    }
    """

    body.append(script)
    search['oninput'] = "searchBooks()"

    # Add CSS styles
    style = soup.new_tag('style')
    style.string = """
    body {
      font-family: Arial, sans-serif; 
      background-color: #f7f7f7;
      padding: 20px;
    }

    .row {
      display: flex;
      justify-content: center;
      align-items: flex-start;
      margin-bottom: 20px;
    }

    .book {
      background-color: white;
      width: calc((100% - 40px) / ${books_per_row}); 
      padding: 20px;
      border-radius: 5px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
      margin-right: 20px;
      width: calc((100% - 40px) / """ + str(books_per_row) + """);
      flex-shrink: 0;
      display: flex;
      flex-wrap: wrap;
    }

    .book:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }

    .book .cover {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 200px;
    }

    .book .cover img {
      max-height: 100%;
      max-width: 100%;
    }

    .book .title {
      margin-top: 10px;
      font-size: 18px;
      font-weight: bold;
    }

    .book .author {
      margin-top: 5px;
      font-size: 14px;
      color: #666;
    }

    .book .description {
      display: none;
      margin-top: 10px;
      font-size: 14px;
      color: #666;
    }

    .book:hover .description {
      display: block;
    }
    .book-container {
      display: grid;
      grid-template-columns: 1fr 2fr;
      margin-bottom: 20px;
    }

    .cover-col {
      text-align: center; 
    }

  .details-col {
    padding-left: 20px;
  }
    .nav {
      margin-top: 20px;
    }
    """
    head.append(style)

    # Create a div for each page
    for book in books:
       
                book_div = soup.new_tag('div')
                # Calculate the range of rows for this page

      

                # Create a div for each book
                #book_div = soup.new_tag('div', **{'class': 'book'})
               
                book_div = soup.new_tag('div', **{'class': 'book-container'})
                cover_div = soup.new_tag('div', **{'class': 'cover-col'})
                details_div = soup.new_tag('div', **{'class': 'details-col'})

                book_div.append(cover_div)  
                book_div.append(details_div)
                # Add the cover thumbnail or a placeholder image
                cover_div = soup.new_tag('div', **{'class': 'cover'})
                book_div.append(cover_div)

                if book['cover']:
                    img = soup.new_tag('img', src=book['cover'])
                else:
                    img = soup.new_tag('img', src='data/placeholder.webp')  
                cover_div.append(img)

                # Add the title and author
                title_div = soup.new_tag('div', **{'class': 'title'})
                title_div.string = book['TITOLO']
                book_div.append(title_div)

                author_div = soup.new_tag('div', **{'class': 'author'})
                author_div.string = book['AUTORE'] 
                details_div.string = 'ISBDN-13: ' + book['ISBDN-13'] + '\nPosizione: ' + book['pos.'] + '\nNote: ' + book['NOTE']
                book_div.append(author_div)
                book_div.append(details_div)

                # Add the description
                if book['description']:
                    desc_div = soup.new_tag('div', **{'class': 'description'})
                   
                    desc_div.string = book['description']
                    book_div.append(desc_div)
                book_div['class'] = 'book'
                body.append(book_div)
                body.append(soup.new_tag('br'))
                book_container = soup.new_tag('div')
                book_container.append(book_div)
                body.append(book_container)
                    
    

    

    body.append(book_div)
   
   


    
    for book_div in soup.find_all('div', {'data-index': True}): 
        book_div['style'] = 'border: 1px solid #ddd; padding: 10px; margin: 10px;'

    for desc_div in soup.find_all('div', {'class': 'description'}):
        desc_div['style'] = 'background-color: #f5f5f5; padding: 10px; border: 1px solid #ddd;' 

    for link in soup.find_all('a'):
        link['style'] = 'color: blue; text-decoration: underline;'

    body['style'] = 'text-align: left; max-width: 800px; margin: 0 auto;'

    title = soup.new_tag('title')
    title.string = 'Book Descriptions'
    soup.head.append(title)     


    return str(soup)

# Example usage
books_per_row = 3
books_per_page = 14
html = generate_library_html(books_per_row, books_per_page)

# Save the HTML page
with open('library.html', 'w', encoding='utf-8') as f:
    f.write(html)