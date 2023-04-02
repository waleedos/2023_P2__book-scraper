import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL of the category page to scrape
category_url = 'https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'

# Open CSV file to write data to
csv_file = open('category_books.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)

# Write header row to CSV file
writer.writerow([
    'product_page_url',
    'universal_product_code',
    'title',
    'price_including_tax',
    'price_excluding_tax',
    'number_available',
    'product_description',
    'category',
    'review_rating',
    'image_url'
])

# Retrieve category page
response = requests.get(category_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all book links on category page
links = soup.select('h3 > a')

# Loop over book links
for link in links:
    book_url = urljoin(category_url, link['href'])
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get product data
    title = soup.find('h1').text.strip()

    price_excl_tax_element = soup.find('td', string='Price (excl. tax)')
    if price_excl_tax_element:
        price_excl_tax = price_excl_tax_element.find_next_sibling('td').text.strip()
    else:
        price_excl_tax = ''

    price_incl_tax_element = soup.find('td', string='Price (incl. tax)')
    if price_incl_tax_element:
        price_incl_tax = price_incl_tax_element.find_next_sibling('td').text.strip()
    else:
        price_incl_tax = ''

    upc_element = soup.find('td', string='UPC')
    if upc_element:
        upc = upc_element.find_next_sibling('td').text.strip()
    else:
        upc = ''

    num_available_element = soup.find('td', string='Availability')
    if num_available_element:
        num_available = num_available_element.find_next_sibling('td').text.strip()
    else:
        num_available = ''

    product_desc = soup.find('article', {'class': 'product_page'}).find_all('p')[3].text.strip()

    category = soup.find('ul', {'class': 'breadcrumb'}).find_all('li')[2].text.strip()

    review_rating_element = soup.find('div', {'class': 'col-sm-6 product_main'}).find('p', {'class': 'star-rating'})
    if review_rating_element:
        review_rating = review_rating_element.attrs['class'][1]
    else:
        review_rating = ''

    image_url_element = soup.find('div', {'class': 'item active'}).find('img')
    if image_url_element:
        image_url = urljoin(book_url, image_url_element.attrs['src'])
    else:
        image_url = ''

    # Write product data to CSV
    writer.writerow([
        book_url,
        upc,
        title,
        price_incl_tax,
        price_excl_tax,
        num_available,
        product_desc,
        category,
        review_rating,
        image_url
    ])

# Close CSV file
csv_file.close()

print('Scraping complete!')
