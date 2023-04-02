import requests
import csv
from bs4 import BeautifulSoup

# URL de la page produit
url = 'https://books.toscrape.com/catalogue/the-black-maria_991/index.html'

# Obtenir le contenu de la page en utilisant requests
response = requests.get(url)
content = response.content

# Analyser le contenu de la page avec BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# Extraire les informations souhaitées
product_page_url = url
upc_element = soup.find('td', string='UPC')
upc = upc_element.find_next_sibling('td').text if upc_element else ''
title = soup.find('h1').text
price_including_tax_element = soup.find('td', string='Price (incl. tax)')
price_including_tax = price_including_tax_element.find_next_sibling('td').text if price_including_tax_element else ''
price_excluding_tax_element = soup.find('td', string='Price (excl. tax)')
price_excluding_tax = price_excluding_tax_element.find_next_sibling('td').text if price_excluding_tax_element else ''
number_available_element = soup.find('td', string='Availability')
number_available = number_available_element.find_next_sibling('td').text if number_available_element else ''
product_description_element = soup.find('div', {'id': 'product_description'})
product_description = product_description_element.find_next('p').text if product_description_element else ''
category_element = soup.find('ul', {'class': 'breadcrumb'})
category = category_element.find_all('li')[2].text.strip() if category_element else ''
review_rating_element = soup.find('p', {'class': 'star-rating'})
review_rating = review_rating_element['class'][1] if review_rating_element else ''
image_url_element = soup.find('img')
image_url = 'https://books.toscrape.com' + image_url_element['src'][5:] if image_url_element else ''

# Écrire les informations extraites dans un fichier CSV avec des en-têtes de colonnes correspondants
with open('produit.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['product_page_url', 'universal_product_code (upc)', 'title', 'price_including_tax',
                  'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating',
                  'image_url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'product_page_url': product_page_url,
                     'universal_product_code (upc)': upc,
                     'title': title,
                     'price_including_tax': price_including_tax,
                     'price_excluding_tax': price_excluding_tax,
                     'number_available': number_available,
                     'product_description': product_description,
                     'category': category,
                     'review_rating': review_rating,
                     'image_url': image_url})

print('Les informations ont été écrites dans le fichier produit.csv')
