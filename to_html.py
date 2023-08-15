import csv
from bs4 import BeautifulSoup

def generate_library_html(books_per_row, books_per_page):
    # Read the CSV file with correct encoding
    with open('library.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        books = list(reader)

    # Calculate the number of rows and pages based on the parameters
    num_rows = (len(books) + books_per_row - 1) // books_per_row
    num_pages = (num_rows + books_per_page - 1) // books_per_page

    # Create the HTML page
    soup = BeautifulSoup('<html><head></head><body></body></html>', 'html.parser')
    body = soup.body
    head = soup.head

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
      padding: 20px;
      border-radius: 5px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
      margin-right: 20px;
      width: calc((100% - 40px) / """ + str(books_per_row) + """);
      flex-shrink: 0;
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

    .nav {
      margin-top: 20px;
    }
    """
    head.append(style)

    # Create a div for each page
    for page in range(num_pages):
        page_div = soup.new_tag('div', id=f'page{page+1}', **{'class': 'page'})
        body.append(page_div)

        # Calculate the range of rows for this page
        start_row = page * books_per_page
        end_row = min(start_row + books_per_page, num_rows)

        # Add the rows for this page
        for row in range(start_row, end_row):
            row_div = soup.new_tag('div', **{'class': 'row'})
            page_div.append(row_div)

            # Calculate the range of books for this row
            start_index = row * books_per_row
            end_index = min(start_index + books_per_row, len(books))

            # Add the books for this row
            for i in range(start_index, end_index):
                book = books[i]

                # Create a div for each book
                book_div = soup.new_tag('div', **{'class': 'book'})
                row_div.append(book_div)

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
                author_div.string = book['AUTORE'] + '\nISBDN-13: ' + str(book['ISBDN-13']) + '\nPosizione: ' + str(book['pos.']) + '\nnote: ' + book['NOTE']
                book_div.append(author_div)

                # Add the description
                if book['description']:
                    desc_div = soup.new_tag('div', **{'class': 'description'})
                   
                    desc_div.string = book['description']
                    book_div.append(desc_div)

    # Add navigation links after the pages
    nav = soup.new_tag('div', **{'class': 'nav'})
    body.append(nav)

    script = soup.new_tag('script')
    script.string = """
    function showPage(pageNumber) {
      // Hide all pages
      var pages = document.getElementsByClassName('page');
      for (var i = 0; i < pages.length; i++) {
        pages[i].style.display = 'none';
      }
      
      // Show the selected page
      var page = document.getElementById('page' + pageNumber);
      if (page) {
        page.style.display = 'block';
      }
    }

    // Show the first page initially
    showPage(1);
    """
    body.append(script)

    for page in range(num_pages):
        a = soup.new_tag('a', href=f'javascript:showPage({page+1})')
        a.string = f'[{page+1}]'
        nav.append(a)
        nav.append(' ')
    
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
books_per_page = 21
html = generate_library_html(books_per_row, books_per_page)

# Save the HTML page
with open('library.html', 'w', encoding='utf-8') as f:
    f.write(html)