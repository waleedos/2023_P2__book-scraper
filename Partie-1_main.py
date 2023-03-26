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

# Afficher les informations
print("product_page_url:", product_page_url)
print("upc:", upc)
print("title:", title)
print("price_including_tax:", price_including_tax)
print("price_excluding_tax:", price_excluding_tax)
print("number_available:", number_available)
print("product_description:", product_description)
print("category:", category)
print("review_rating:", review_rating)
print("image_url:", image_url)