import csv
import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/how-music-works_979/index.html"

# Obtenir le contenu de la page
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extraire les informations nécessaires
product_page_url = url
upc = soup.find('th', string='UPC').find_next_sibling('td').string
title = soup.find('h1').string
price_including_tax = soup.find('th', string='Price (incl. tax)').find_next_sibling('td').string
price_excluding_tax = soup.find('th', string='Price (excl. tax)').find_next_sibling('td').string
number_available = soup.find('th', string='Availability').find_next_sibling('td').string
product_description = soup.find('div', {'id': 'product_description'}).find_next('p').string
category = soup.find('ul', {'class': 'breadcrumb'}).find_all('a')[2].string
review_rating = soup.find('p', {'class': 'star-rating'})['class'][1]
image_url = soup.find('div', {'class': 'item active'}).img['src']
image_url = image_url.replace('../..', 'https://books.toscrape.com')

# Écrire les données dans un fichier CSV
with open('book_data.csv', mode='w', newline='') as csvfile:
    fieldnames = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available',
                  'product_description', 'category', 'review_rating', 'image_url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'product_page_url': product_page_url, 'upc': upc, 'title': title,
                     'price_including_tax': price_including_tax, 'price_excluding_tax': price_excluding_tax,
                     'number_available': number_available, 'product_description': product_description,
                     'category': category, 'review_rating': review_rating, 'image_url': image_url})
